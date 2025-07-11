#!/usr/bin/env python3
"""
Google Docs Sync Script for MADIO Framework
Syncs local markdown files to Google Docs for Claude Project integration
"""

import json
import os
import sys
import argparse
import glob
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Import tqdm for progress bars (with fallback if not available)
try:
    from tqdm import tqdm
    TQDM_AVAILABLE = True
except ImportError:
    TQDM_AVAILABLE = False
    # Fallback: simple progress indicator
    def tqdm(iterable, desc="Processing", total=None, unit="file"):
        for i, item in enumerate(iterable):
            if total:
                print(f"\r{desc}: {i+1}/{total} {unit}s", end="", flush=True)
            else:
                print(f"\r{desc}: {i+1} {unit}s", end="", flush=True)
            yield item
        print()  # New line after completion

# Scopes required for Google Docs and Drive APIs
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

# Placeholder for new documents in config - this might be deprecated if registry stores None for new docs
NEW_DOC_PLACEHOLDER = "CREATE_NEW_DOCUMENT"

# Import the new registry management functions
try:
    from . import madio_registry # Relative import if in the same package
    from .madio_registry import calculate_sha256_hash
except ImportError:
    import madio_registry # Direct import if run as script or in PYTHONPATH
    from madio_registry import calculate_sha256_hash


def find_project_root():
    """Find project root by looking for .claude directory"""
    current = Path.cwd().resolve()
    while current != current.parent:
        if (current / '.claude').exists():
            return current
        current = current.parent
    raise Exception("Project root not found - no .claude directory located in parent directories")

def resolve_from_root(path):
    """Resolve path relative to project root regardless of execution context"""
    if not path:
        return path
    
    path = str(path)
    project_root = find_project_root()
    
    # If path is already absolute, return as-is
    if os.path.isabs(path):
        return path
    
    # Remove leading ./ if present
    path = path.lstrip('./')
    
    # Remove leading ../ patterns and resolve from project root
    while path.startswith('../'):
        path = path[3:]
    
    return str(project_root / path)

def resolve_script_file(filename):
    """Resolve a file path relative to the script directory"""
    project_root = find_project_root()
    return str(project_root / '.claude' / 'scripts' / filename)

def handle_http_error(error, operation="operation"):
    """Provide specific error messages and guidance for HTTP errors"""
    error_code = getattr(error, 'resp', {}).get('status')
    
    if error_code == 401:
        print(f"❌ Authentication failed during {operation}")
        print("🔧 Solutions:")
        print("   • Delete token.pickle and re-authenticate: rm .claude/scripts/token.pickle")
        print("   • Verify credentials.json is valid")
        print("   • Check if OAuth consent screen is configured")
        print("   • Run: /madio-doctor for comprehensive diagnostics")
        return "auth_failed"
    
    elif error_code == 403:
        print(f"❌ Access forbidden during {operation}")
        print("🔧 Solutions:")
        print("   • Check if Google Docs API is enabled in Google Cloud Console")
        print("   • Check if Google Drive API is enabled in Google Cloud Console")
        print("   • Verify document/folder permissions")
        print("   • Ensure OAuth app has proper scopes")
        return "access_forbidden"
    
    elif error_code == 404:
        print(f"❌ Resource not found during {operation}")
        print("🔧 Solutions:")
        print("   • Verify Google Document ID is correct")
        print("   • Check if document was moved or deleted")
        print("   • Ensure you have access to the document")
        return "not_found"
    
    elif error_code == 429:
        print(f"❌ Rate limit exceeded during {operation}")
        print("🔧 Solutions:")
        print("   • Wait a few minutes before retrying")
        print("   • Reduce number of concurrent operations")
        print("   • Script will automatically retry with exponential backoff")
        return "rate_limited"
    
    elif error_code and error_code >= 500:
        print(f"❌ Google server error during {operation} (HTTP {error_code})")
        print("🔧 Solutions:")
        print("   • This is a temporary Google server issue")
        print("   • Wait a few minutes and try again")
        print("   • Check Google Cloud Status page for outages")
        return "server_error"
    
    else:
        print(f"❌ HTTP error during {operation}: {error}")
        print("🔧 Solutions:")
        print("   • Check internet connection")
        print("   • Verify Google Cloud Console configuration")
        print("   • Run: /madio-doctor for troubleshooting")
        return "unknown_http_error"

def handle_auth_error(error, operation="authentication"):
    """Handle authentication-specific errors with detailed guidance"""
    error_msg = str(error).lower()
    
    if "credentials" in error_msg or "client_secrets" in error_msg:
        print(f"❌ Credentials file error during {operation}")
        print("🔧 Solutions:")
        print("   • Verify credentials.json exists in .claude/scripts/")
        print("   • Re-download credentials.json from Google Cloud Console")
        print("   • Check file permissions: chmod 600 .claude/scripts/credentials.json")
        print("   • See complete setup guide: SYNC_SETUP.md")
        
    elif "consent" in error_msg or "oauth" in error_msg:
        print(f"❌ OAuth consent error during {operation}")
        print("🔧 Solutions:")
        print("   • Complete OAuth consent flow in browser")
        print("   • Check if your Google account is added as test user")
        print("   • Verify OAuth consent screen is configured")
        
    elif "scope" in error_msg:
        print(f"❌ OAuth scope error during {operation}")
        print("🔧 Solutions:")
        print("   • Credentials may have insufficient permissions")
        print("   • Re-create OAuth credentials with Docs + Drive APIs")
        print("   • Delete token.pickle and re-authenticate")
        
    else:
        print(f"❌ Authentication error during {operation}: {error}")
        print("🔧 Solutions:")
        print("   • Delete token.pickle: rm .claude/scripts/token.pickle")
        print("   • Re-run sync to re-authenticate")
        print("   • Check SYNC_SETUP.md for complete instructions")

def retry_on_rate_limit(func, max_retries=3, base_delay=1):
    """Retry function with exponential backoff on rate limit errors"""
    import time
    
    for attempt in range(max_retries):
        try:
            return func()
        except HttpError as error:
            if getattr(error, 'resp', {}).get('status') == 429:
                if attempt < max_retries - 1:
                    delay = base_delay * (2 ** attempt)
                    print(f"⏳ Rate limited. Retrying in {delay} seconds... (attempt {attempt + 1}/{max_retries})")
                    time.sleep(delay)
                    continue
                else:
                    print("❌ Max retry attempts reached for rate limiting")
                    raise
            else:
                raise
    
    return None

class GoogleDocsSync:
    def __init__(self, credentials_file='credentials.json', token_file='token.pickle'):
        # Resolve file paths relative to script directory
        self.credentials_file = resolve_script_file(credentials_file) if not os.path.isabs(credentials_file) else credentials_file
        self.token_file = resolve_script_file(token_file) if not os.path.isabs(token_file) else token_file
        self.service = None
        self.drive_service = None
        self.target_folder_id = None
        self.cli_args = None # Placeholder for args
        # self.authenticate() # Authentication will be called after args are set
    
    def set_cli_args(self, args):
        self.cli_args = args

    def authenticate(self):
        """Authenticate with Google Docs API with enhanced error handling"""
        creds = None
        
        try:
            # Check if token file exists
            if os.path.exists(self.token_file):
                try:
                    creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
                except Exception as e:
                    print(f"⚠️ Invalid token file, will re-authenticate: {e}")
                    # Remove invalid token file
                    os.remove(self.token_file)
                    creds = None
            
            # If no valid credentials, get new ones
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    try:
                        print("🔄 Refreshing expired authentication token...")
                        creds.refresh(Request())
                    except Exception as e:
                        print(f"⚠️ Token refresh failed, will re-authenticate: {e}")
                        creds = None
                
                if not creds:
                    if not os.path.exists(self.credentials_file):
                        print(f"❌ Credentials file not found: {self.credentials_file}")
                        print("🔧 Solutions:")
                        print("   • Download credentials.json from Google Cloud Console")
                        print("   • Place it at: .claude/scripts/credentials.json")
                        print("   • Set permissions: chmod 600 .claude/scripts/credentials.json")
                        print("   • See complete setup guide: SYNC_SETUP.md")
                        sys.exit(1)
                    
                    try:
                        print("🔐 Starting OAuth authentication flow...")
                        flow = InstalledAppFlow.from_client_secrets_file(
                            self.credentials_file, SCOPES)
                        creds = flow.run_local_server(port=0)
                        print("✅ OAuth authentication completed")
                    except Exception as e:
                        handle_auth_error(e, "OAuth flow")
                        sys.exit(1)
                
                # Save credentials for next run
                try:
                    with open(self.token_file, 'w') as token:
                        token.write(creds.to_json())
                except IOError as e:
                    print(f"⚠️ Warning: Could not save token file: {e}")
                    print("   Authentication will be required again next time")
            
            # Build API services
            try:
                self.service = build('docs', 'v1', credentials=creds)
                self.drive_service = build('drive', 'v3', credentials=creds)
                print("✅ Google Docs and Drive authentication successful")
            except Exception as e:
                handle_auth_error(e, "API service creation")
                sys.exit(1)
                
        except Exception as e:
            print(f"❌ Unexpected authentication error: {e}")
            print("🔧 Solutions:")
            print("   • Delete token.pickle: rm .claude/scripts/token.pickle")
            print("   • Verify credentials.json is valid")
            print("   • Run: /madio-doctor for comprehensive diagnostics")
            sys.exit(1)
    
    def find_folder_by_name(self, folder_name):
        """Search for a folder by name in Google Drive"""
        try:
            print(f"🔍 Searching for folder: \"{folder_name}\"...")
            
            # Search for folders with the specified name
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            results = self.drive_service.files().list(
                q=query,
                fields='files(id, name, parents)'
            ).execute()
            
            folders = results.get('files', [])
            
            if not folders:
                print(f"❌ Folder \"{folder_name}\" not found")
                return None
            elif len(folders) == 1:
                folder_id = folders[0]['id']
                print(f"✅ Found folder \"{folder_name}\" (ID: {folder_id[:15]}...)")
                return folder_id
            else:
                # Multiple folders found - use the first one but warn
                folder_id = folders[0]['id']
                print(f"⚠️  Multiple folders named \"{folder_name}\" found. Using first one (ID: {folder_id[:15]}...)")
                return folder_id
                
        except HttpError as error:
            error_type = handle_http_error(error, f"searching for folder '{folder_name}'")
            return None
        except Exception as e:
            print(f"❌ Unexpected error searching for folder \"{folder_name}\": {e}")
            print("🔧 Solutions:")
            print("   • Check internet connection")
            print("   • Verify Google Drive API is enabled")
            print("   • Run: /madio-doctor for troubleshooting")
            return None
    
    def create_folder(self, folder_name):
        """Create a new folder in Google Drive"""
        try:
            print(f"📁 Creating folder: \"{folder_name}\"...")
            
            folder_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            
            folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            
            folder_id = folder.get('id')
            print(f"✅ Created folder \"{folder_name}\" (ID: {folder_id[:15]}...)")
            return folder_id
            
        except HttpError as error:
            error_type = handle_http_error(error, f"creating folder '{folder_name}'")
            return None
        except Exception as e:
            print(f"❌ Unexpected error creating folder \"{folder_name}\": {e}")
            print("🔧 Solutions:")
            print("   • Check internet connection")
            print("   • Verify Google Drive API is enabled")
            print("   • Check if you have permission to create folders")
            print("   • Run: /madio-doctor for troubleshooting")
            return None
    
    def prompt_for_folder(self): # Removed cli_args from parameters, will use self.cli_args
        """Prompt user for Google Drive folder selection with terminal detection"""
        
        # Determine if an interactive session is intended and possible
        interactive_session_intended = self.cli_args and self.cli_args.interactive_session
        # The 'force_interactive' via --interactive can be a fallback if needed, or removed if --interactive-session is sufficient
        force_interactive_flag = self.cli_args and self.cli_args.interactive

        can_be_interactive = sys.stdin.isatty() and sys.stdout.isatty()
        dev_tty_input = None

        if interactive_session_intended and not can_be_interactive:
            # Try to use /dev/tty if stdin is not a TTY but interaction is desired
            if os.name == 'posix': # Posix check for /dev/tty
                try:
                    dev_tty_input_stream = open('/dev/tty', 'r')
                    # Test if we can actually read. This might still fail in some restricted environments.
                    # A simple test could be trying to read with a timeout, but input() will block.
                    # For now, we'll assume if open succeeds, we can try using it.
                    # We need a way to use this stream for input() or an alternative.
                    # Standard input() uses sys.stdin. We might need a custom input function.
                    # This is a simplification; robustly handling /dev/tty for input() is complex.
                    # Let's make a custom input function for this case.

                    def get_input_from_tty(prompt_message):
                        sys.stdout.write(prompt_message) # Write prompt to current stdout
                        sys.stdout.flush()
                        try:
                            return dev_tty_input_stream.readline().strip()
                        finally:
                            # Do not close dev_tty_input_stream here if you plan to reuse it.
                            # It should be closed when the script exits or when done with all prompts.
                            # For simplicity in this change, let's assume one-time use or it's closed later.
                            pass # dev_tty_input_stream.close() should be handled carefully

                    print("    Attempting direct TTY interaction for folder prompt...")
                    dev_tty_input = get_input_from_tty # Assign custom input function

                except Exception as e:
                    print(f"   ⚠️ Could not open /dev/tty for direct input: {e}")
                    dev_tty_input = None # Fallback

        actual_input_func = dev_tty_input if dev_tty_input else input

        if not (can_be_interactive or dev_tty_input): # If not a TTY and /dev/tty failed or wasn't attempted/intended
            if interactive_session_intended: # User wanted interaction but we couldn't provide it
                print("\n📁 Google Drive Folder Configuration")
                print("   ⚠️  Interactive session intended, but standard input is not a TTY and direct TTY access failed.")
                print("   📂 Defaulting to root folder (My Drive).")
                print("   💡 To specify a folder, please use the command-line arguments:")
                print("      --folder \"Your Desired Folder Name\"")
                print("      OR --folder-id \"your_folder_id_here\"")
            else: # Genuinely non-interactive (e.g. CI/CD)
                print("\n📁 Google Drive Folder Configuration")
                print("   ℹ️  Non-interactive environment detected (e.g., CI/CD or script).")
                print("   📂 Using root folder (My Drive) by default.")
                print("   💡 Tip: Use --folder 'Your Folder Name' or --folder-id 'your_folder_id' to specify a folder.")
            return None

        # Proceed with interactive prompting
        print("\n📁 Google Drive Folder Configuration")
        print("   Choose a Google Drive folder for your MADIO documents.")
        print("   - Press Enter to use the root 'My Drive' folder.")
        print("   - Type a folder name (e.g., 'My AI Project Docs').")
        print("   - If the folder doesn't exist, you'll be asked to create it.")
        
        while True:
            try:
                # Use actual_input_func which could be input() or one reading from /dev/tty
                folder_name = actual_input_func("Enter folder name (or press Enter for root 'My Drive'): ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\n📂 Using root folder (My Drive). User cancelled prompt.")
                return None
            
            if not folder_name:
                print("📂 Using root folder (My Drive)")
                return None
            
            # Search for the folder
            folder_id = self.find_folder_by_name(folder_name)
            
            if folder_id:
                return {'name': folder_name, 'id': folder_id}
            else:
                # Folder not found, ask to create
                print(f"\n❓ Folder \"{folder_name}\" not found in Google Drive.")
                # Use actual_input_func here as well
                create_choice = actual_input_func(f"Create folder \"{folder_name}\" in Google Drive? (y/N): ").strip().lower()
                
                if create_choice == 'y': # Standardize to 'y' for yes
                    folder_id = self.create_folder(folder_name)
                    if folder_id:
                        return {'name': folder_name, 'id': folder_id}
                    else:
                        print("❌ Failed to create folder. Please try again.")
                        continue
                else:
                    print("📂 Using root folder (My Drive)")
                    return None
    
    def discover_markdown_files(self, directory_path, include_pattern=None, exclude_pattern=None):
        """Discover all markdown files in the specified directory with optional pattern filtering"""
        if not os.path.exists(directory_path):
            print(f"❌ Directory not found: {directory_path}")
            return []
        
        if not os.path.isdir(directory_path):
            print(f"❌ Path is not a directory: {directory_path}")
            return []
        
        print(f"🔍 Discovering markdown files in: {directory_path}")
        if include_pattern:
            print(f"   📋 Include pattern: {include_pattern}")
        if exclude_pattern:
            print(f"   🚫 Exclude pattern: {exclude_pattern}")
        
        # Use glob to find all .md files recursively
        if include_pattern:
            # Use custom pattern if provided
            pattern = os.path.join(directory_path, "**", include_pattern)
        else:
            # Default to all .md files
            pattern = os.path.join(directory_path, "**", "*.md")
            
        markdown_files = glob.glob(pattern, recursive=True)
        
        # Filter out hidden files and directories with progress indicator
        filtered_files = []
        if TQDM_AVAILABLE and len(markdown_files) > 5:
            # Use progress bar for large file lists
            for file_path in tqdm(markdown_files, desc="📂 Filtering files", unit="file"):
                if self._should_include_file(file_path, directory_path, exclude_pattern):
                    filtered_files.append(file_path)
        else:
            # Simple processing for small file lists
            for file_path in markdown_files:
                if self._should_include_file(file_path, directory_path, exclude_pattern):
                    filtered_files.append(file_path)
        
        print(f"📄 Found {len(filtered_files)} markdown files")
        if len(filtered_files) <= 10:
            # Show individual files for small lists
            for file_path in filtered_files:
                print(f"   • {os.path.relpath(file_path, os.getcwd())}")
        else:
            # Summary for large lists
            print(f"   • Files ready for processing ({len(filtered_files)} total)")
        
        return filtered_files
    
    def _should_include_file(self, file_path, directory_path, exclude_pattern=None):
        """Check if a file should be included based on filters"""
        relative_path = os.path.relpath(file_path, directory_path)
        
        # Skip files in hidden directories or hidden files
        if any(part.startswith('.') for part in relative_path.split(os.sep)):
            return False
        
        # Apply exclude pattern if provided
        if exclude_pattern:
            import fnmatch
            filename = os.path.basename(file_path)
            if fnmatch.fnmatch(filename, exclude_pattern):
                return False
        
        return True
    
    def load_directory_mapping(self, mapping_file='.synced_docs_mapping.json'):
        """Load the persistent mapping of files to Google Doc IDs"""
        if os.path.exists(mapping_file):
            try:
                with open(mapping_file, 'r') as f:
                    mapping = json.load(f)
                print(f"📋 Loaded directory mapping from {mapping_file}")
                return mapping
            except (json.JSONDecodeError, IOError) as e:
                print(f"⚠️  Error loading directory mapping: {e}")
                return {}
        else:
            print(f"📋 No existing directory mapping found, starting fresh")
            return {}
    
    def save_directory_mapping(self, mapping, mapping_file='.synced_docs_mapping.json'):
        """Save the persistent mapping of files to Google Doc IDs"""
        try:
            with open(mapping_file, 'w') as f:
                json.dump(mapping, f, indent=2)
            print(f"💾 Saved directory mapping to {mapping_file}")
            return True
        except IOError as e:
            print(f"❌ Error saving directory mapping: {e}")
            return False
    
    def create_directory_config(self, directory_path, mapping_file='.synced_docs_mapping.json', include_pattern=None, exclude_pattern=None):
        """Create a temporary config from directory discovery"""
        markdown_files = self.discover_markdown_files(directory_path, include_pattern, exclude_pattern)
        if not markdown_files:
            return {}
        
        # Load existing mappings
        existing_mapping = self.load_directory_mapping(mapping_file)
        
        # Create config with discovered files
        config = {}
        updated_mapping = existing_mapping.copy()
        
        for file_path in markdown_files:
            # Use relative path as key for consistency
            relative_path = os.path.relpath(file_path, os.getcwd())
            
            # Check if we already have a doc ID for this file
            if relative_path in existing_mapping:
                doc_id = existing_mapping[relative_path]
                print(f"📄 Using existing Doc ID for {relative_path}: {doc_id[:8]}...")
            else:
                # New file, use placeholder for auto-creation
                doc_id = NEW_DOC_PLACEHOLDER
                print(f"📄 Will create new Doc for {relative_path}")
                updated_mapping[relative_path] = doc_id
            
            config[relative_path] = doc_id
        
        # Save updated mapping if there were changes
        if updated_mapping != existing_mapping:
            self.save_directory_mapping(updated_mapping, mapping_file)
        
        return config
    
    def read_markdown_file(self, file_path):
        """Read markdown file content"""
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
            return None
        except Exception as e:
            print(f"❌ Error reading file {file_path}: {e}")
            return None
    
    def clean_escaped_markdown(self, content):
        """
        Clean escaped markdown characters from Google Docs export
        
        Google Docs "Download as Markdown" feature escapes markdown syntax,
        resulting in content like:
        - \\# Header → # Header
        - \\- List item → - List item 
        - \\*emphasis\\* → *emphasis*
        - \\1. Numbered → 1. Numbered
        - \\+1-2 → +1-2
        - project\\_system\\_instructions → project_system_instructions
        
        This function gracefully handles both escaped and non-escaped content.
        """
        import re
        
        if not content:
            return content
            
        # First, check if content appears to be escaped (heuristic)
        escaped_indicators = [
            r'\\#',          # Escaped headers
            r'\\-\s',        # Escaped lists  
            r'\\\*.*\\\*',   # Escaped emphasis
            r'\\\d+\.',      # Escaped numbered lists
            r'\\>',          # Escaped blockquotes
            r'\\\[.*\\\]',   # Escaped links
            r'\\\+',         # Escaped plus signs
            r'\\\_',         # Escaped underscores in text
            r'\\\s*$',       # Trailing standalone backslashes
        ]
        
        # Count potential escaped markdown patterns
        escape_count = 0
        for indicator in escaped_indicators:
            if re.search(indicator, content):
                escape_count += 1
        
        # If no escaped patterns detected, return original content
        if escape_count == 0:
            return content
            
        # Report detection
        print(f"   🔍 Detected {escape_count} types of escaped markdown patterns")
        
        # Pattern to match escaped markdown characters
        # Matches: \# \* \- \+ \. \1 \2 etc.
        # Ordered by specificity to avoid conflicts
        patterns = [
            # Headers: \# \## \### etc. (handle escaped consecutive hashes)
            (r'\\(#{1,6})', r'\1'),
            
            # Lists: \- \* \+ at start of line or after whitespace
            (r'(^|\s)\\([-*+])\s', r'\1\2 '),
            
            # Numbered lists: \1. \2. etc. (both at start of line and mid-text)
            (r'(^|\s)\\(\d+)\.', r'\1\2.'),
            (r'\\(\d+)\.', r'\1.'),  # Catch remaining escaped numbers with dots
            
            # Escaped plus signs: \+1-2 → +1-2
            (r'\\(\+)', r'\1'),
            
            # Escaped underscores in text: project\_system\_instructions → project_system_instructions
            (r'\\(_)', r'\1'),
            
            # Emphasis: \*text\* \_text\_ (but not legitimate double backslashes)
            (r'(?<!\\)\\([*_])', r'\1'),
            
            # Inline code: \`code\`
            (r'(?<!\\)\\(`)', r'\1'),
            
            # Links: \[text\]\(url\) (but preserve legitimate escapes)
            (r'(?<!\\)\\([\[\]])', r'\1'),
            (r'(?<!\\)\\([()])', r'\1'),
            
            # Horizontal rules: \--- \***
            (r'(?<!\\)\\([-*]{3,})', r'\1'),
            
            # Blockquotes: \> 
            (r'(^|\s)\\(>)\s', r'\1\2 '),
            
            # Trailing standalone backslashes (common in Google Docs exports)
            (r'\\\s*$', r''),
            
            # Escaped periods in general text (not just numbered lists)
            (r'(?<!\\)\\(\.)', r'\1'),
        ]
        
        cleaned_content = content
        changes_made = 0
        
        for pattern, replacement in patterns:
            before_length = len(cleaned_content)
            cleaned_content = re.sub(pattern, replacement, cleaned_content, flags=re.MULTILINE)
            after_length = len(cleaned_content)
            
            if before_length != after_length:
                changes_made += 1
        
        # Report cleanup results
        if changes_made > 0:
            print(f"   🧹 Cleaned {changes_made} types of escaped markdown characters")
        else:
            print(f"   ℹ️  No escaped markdown characters found to clean")
        
        return cleaned_content
    
    def update_google_doc(self, doc_id, content):
        """Update Google Doc with markdown content"""
        try:
            # Get document to check if it exists
            doc = self.service.documents().get(documentId=doc_id).execute()
            
            # Clear existing content
            doc_length = doc['body']['content'][-1]['endIndex'] - 1
            if doc_length > 1:  # Only delete if there's actual content beyond the initial position
                requests = [{
                    'deleteContentRange': {
                        'range': {
                            'startIndex': 1,
                            'endIndex': doc_length
                        }
                    }
                }]
                self.service.documents().batchUpdate(
                    documentId=doc_id, body={'requests': requests}).execute()
            
            # Insert new content
            requests = [{
                'insertText': {
                    'location': {'index': 1},
                    'text': content
                }
            }]
            
            result = self.service.documents().batchUpdate(
                documentId=doc_id, body={'requests': requests}).execute()
            
            # After successful update, fetch the new revision ID using Drive API
            gdoc_drive_metadata = None
            try:
                gdoc_drive_metadata = self.drive_service.files().get(fileId=doc_id, fields='id, name, version, headRevisionId, modifiedTime').execute()
                return {
                    "success": True,
                    "version": gdoc_drive_metadata.get('headRevisionId'),
                    "modified_time": gdoc_drive_metadata.get('modifiedTime')
                }
            except HttpError as drive_err:
                print(f"⚠️ Update to GDoc {doc_id} succeeded, but could not fetch new Drive metadata: {drive_err}")
                return {"success": True, "version": None, "modified_time": None} # Update succeeded but version unknown
            
        except HttpError as error:
            error_type = handle_http_error(error, f"updating Google Doc {doc_id[:15]}...")
            if error_type == "rate_limited":
                # Try with rate limiting retry
                # This retry logic needs to be adjusted if we want to return the version from the retry
                print("Rate limit on update, retry might not return version info correctly yet.")
                # For simplicity in this step, retry_on_rate_limit might need to be enhanced
                # or we accept that a rate-limited retry might not get the version immediately.
                # Let's assume for now retry returns a simple boolean.
                success = retry_on_rate_limit(lambda: self.update_google_doc(doc_id, content).get("success", False))
                return {"success": success, "version": None, "modified_time": None} # Version info lost in simple retry
            return {"success": False, "version": None, "modified_time": None}
        except Exception as e:
            print(f"❌ Unexpected error updating Google Doc {doc_id[:15]}...: {e}")
            print("🔧 Solutions:")
            print("   • Check internet connection")
            print("   • Verify document ID is correct")
            print("   • Ensure you have edit permissions")
            print("   • Run: /madio-doctor for troubleshooting")
            return False

    def move_document_to_folder(self, doc_id, folder_id):
        """Move a document to a specific folder in Google Drive"""
        try:
            print(f"📁 Moving document {doc_id[:8]}... to folder {folder_id[:8]}...")
            
            # Get the document's current parents
            file = self.drive_service.files().get(
                fileId=doc_id,
                fields='parents'
            ).execute()
            
            previous_parents = ",".join(file.get('parents', []))
            
            # Move the document to the target folder
            self.drive_service.files().update(
                fileId=doc_id,
                addParents=folder_id,
                removeParents=previous_parents,
                fields='id, parents'
            ).execute()
            
            print(f"✅ Document moved to folder successfully")
            return True
            
        except HttpError as error:
            print(f"❌ Error moving document to folder: {error}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error moving document to folder: {e}")
            return False

    def _download_gdoc_as_markdown(self, doc_id):
        """Downloads Google Doc content as markdown text."""
        try:
            print(f"📄 Downloading GDoc {doc_id} as markdown...")
            request = self.drive_service.files().export_media(fileId=doc_id, mimeType='text/markdown')
            response_bytes = request.execute()
            # Assuming UTF-8 encoding, which is typical for markdown from GDocs export
            markdown_content = response_bytes.decode('utf-8')
            # The exported markdown from Google often has escaped characters.
            # We might want to clean it here or let the user handle it.
            # For now, return as-is from export. Or use self.clean_escaped_markdown
            # cleaned_content = self.clean_escaped_markdown(markdown_content)
            # return cleaned_content
            return markdown_content
        except HttpError as error:
            handle_http_error(error, f"downloading GDoc {doc_id} as markdown")
            return None
        except Exception as e:
            print(f"❌ Unexpected error downloading GDoc {doc_id}: {e}")
            return None

    def create_google_doc(self, title):
        """Create a new Google Doc and return its ID."""
        try:
            print(f"➕ Creating new Google Doc with title: \"{title}\"...")
            document_body = {'title': title}
            doc = self.service.documents().create(body=document_body).execute() # This creates the doc
            doc_id = doc.get('documentId')
            print(f"✅ Successfully created Google Doc with ID: {doc_id}")

            # To get revision ID, we might need a drive.files.get call after creation
            # However, the document object returned by documents().create() might not have revision info directly.
            # Let's fetch it separately using drive_service to ensure we get it.
            gdoc_drive_metadata = None
            try:
                gdoc_drive_metadata = self.drive_service.files().get(fileId=doc_id, fields='id, name, version, headRevisionId, modifiedTime').execute()
            except HttpError as drive_err:
                print(f"⚠️ Could not fetch Drive metadata for new GDoc {doc_id}: {drive_err}")

            # Move to target folder if specified
            if self.target_folder_id:
                move_success = self.move_document_to_folder(doc_id, self.target_folder_id)
                if not move_success:
                    print(f"⚠️  Document created but failed to move to folder")
            
            return {
                "doc_id": doc_id,
                "version": gdoc_drive_metadata.get('headRevisionId') if gdoc_drive_metadata else None,
                "modified_time": gdoc_drive_metadata.get('modifiedTime') if gdoc_drive_metadata else None
            }
        except HttpError as error:
            error_type = handle_http_error(error, f"creating Google Doc '{title}'")
            if error_type == "rate_limited":
                # Try with rate limiting retry
                return retry_on_rate_limit(lambda: self.create_google_doc(title))
            return None
        except Exception as e:
            print(f"❌ Unexpected error creating Google Doc \"{title}\": {e}")
            print("🔧 Solutions:")
            print("   • Check internet connection")
            print("   • Verify Google Docs API is enabled")
            print("   • Check if you have permission to create documents")
            print("   • Run: /madio-doctor for troubleshooting")
            return None
    
    def get_doc_url(self, doc_id):
        """Generate Google Doc URL from document ID"""
        return f"https://docs.google.com/document/d/{doc_id}/edit"
    
    def sync_file(self, file_path, doc_id, clean_escapes=True, show_url=False):
        """Sync a single file to Google Docs"""
        print(f"📄 Syncing {file_path} to Google Doc {doc_id[:8]}...")
        
        content = self.read_markdown_file(file_path)
        if content is None:
            return False
        
        # Clean escaped markdown characters if requested
        if clean_escapes:
            content = self.clean_escaped_markdown(content)
        
        update_result = self.update_google_doc(doc_id, content) # Now returns a dict
        if update_result.get("success"):
            print(f"✅ Successfully synced {file_path}")
            if show_url:
                print(f"   🔗 View: {self.get_doc_url(doc_id)}")
        else:
            print(f"❌ Failed to sync {file_path}")
        
        return update_result # Return the whole dict
    
    def sync_all_files(self, clean_escapes=True, target_folder_override=None): # Removed old config/mapping args
        """Sync all files based on the document_registry.json."""
        
        registry_data = madio_registry.load_registry()
        doc_registry_map = registry_data.get("document_registry", {})
        sync_preferences = madio_registry.get_sync_preferences(registry_data)
        registry_updated = False

        # Handle folder configuration
        # Priority: command-line override -> registry preference -> prompt
        if target_folder_override:
            print(f"📁 Command-line folder override: \"{target_folder_override}\"")
            folder_id = self.find_folder_by_name(target_folder_override)
            if folder_id:
                self.target_folder_id = folder_id
                # Update registry if different or not set
                if sync_preferences.get("google_drive_folder", {}).get("name") != target_folder_override or \
                   sync_preferences.get("google_drive_folder", {}).get("id") != folder_id:
                    sync_preferences["google_drive_folder"] = {"name": target_folder_override, "id": folder_id}
                    madio_registry.update_sync_preferences(registry_data, sync_preferences)
                    registry_updated = True
            else:
                print(f"📁 Folder \"{target_folder_override}\" not found, creating...")
                folder_id = self.create_folder(target_folder_override)
                if folder_id:
                    self.target_folder_id = folder_id
                    sync_preferences["google_drive_folder"] = {"name": target_folder_override, "id": folder_id}
                    madio_registry.update_sync_preferences(registry_data, sync_preferences)
                    registry_updated = True
                else:
                    print(f"❌ Failed to create folder \"{target_folder_override}\", using root folder.")
                    self.target_folder_id = None # Default to root
        
        elif sync_preferences.get("google_drive_folder", {}).get("id"):
            folder_name = sync_preferences["google_drive_folder"]["name"]
            folder_id = sync_preferences["google_drive_folder"]["id"]
            print(f"📂 Using configured folder from registry: \"{folder_name}\" ({folder_id[:15]}...)")
            self.target_folder_id = folder_id
        else:
            # No folder configured in registry and no override - prompt user
            try:
                folder_info = self.prompt_for_folder()
                if folder_info:
                    print(f"📂 Selected folder: \"{folder_info['name']}\" ({folder_info['id'][:15]}...)")
                    self.target_folder_id = folder_info['id']
                    sync_preferences["google_drive_folder"] = {"name": folder_info['name'], "id": folder_info['id']}
                    madio_registry.update_sync_preferences(registry_data, sync_preferences)
                    registry_updated = True
                else:
                    print("📂 Using root folder (My Drive). No folder preference saved.")
                    self.target_folder_id = None
            except (EOFError, KeyboardInterrupt):
                print("\n📂 Using root folder (My Drive). User cancelled prompt.")
                self.target_folder_id = None

        success_count = 0
        total_count = 0
        synced_docs = []

        # Iterate over a copy of items if modifying the dict during iteration (not strictly needed here as we modify entries)
        # Items are (local_path_str, entry_data_dict)
        registry_items = list(doc_registry_map.items())

        if not registry_items:
            print("ℹ️ Document registry is empty. Nothing to sync.")
            if registry_updated: # Save if only folder prefs changed
                 madio_registry.save_registry(registry_data)
            return True

        print(f"🔄 Processing {len(registry_items)} document(s) from registry...")

        # Progress indicator
        if TQDM_AVAILABLE and len(registry_items) > 1: # Show progress if more than 1 file
            file_iterator = tqdm(registry_items, desc="🔄 Syncing files", unit="file")
        else:
            file_iterator = registry_items
        
        project_root = madio_registry.get_project_root()

        for local_path_str, entry_data in file_iterator:
            # Construct absolute local path from project root + relative path from registry
            absolute_local_path = project_root / local_path_str

            doc_id = entry_data.get("google_doc_id")
            status = entry_data.get("status", "unknown") # Phase 1: basic status

            # --- BUG-002: Basic Stale Mapping Detection START ---
            # 1. Check local file existence
            if not absolute_local_path.exists():
                entry_data["status"] = "error_local_missing"
                doc_registry_map[local_path_str] = entry_data
                registry_updated = True

                if self.cli_args and self.cli_args.interactive_session: # Check for interactive mode
                    print(f"❓ Stale mapping: Local file not found at {absolute_local_path}.")
                    choice = input("   Options: (R)emove from registry, (U)nlink GDoc & Remove, (S)kip this time, (A)bort sync? [S]: ").strip().lower()
                    if choice == 'r':
                        # To be fully implemented: remove_document_entry would be called when saving.
                        # For now, mark for deletion or handle directly.
                        # This implies deleting the GDoc is not an option here as local file is primary.
                        print(f"   Action: Marked {local_path_str} for removal from registry.")
                        # We'd need a way to signal this to the main loop or handle removal here.
                        # For Phase 2, let's simplify: remove means it won't be processed further by this run.
                        # Actual removal from registry file happens on save if we delete from doc_registry_map.
                        del doc_registry_map[local_path_str]
                        registry_updated = True # Ensure save happens
                        continue # Effectively removed for this run.
                    elif choice == 'u': # Unlink GDoc (if any) & Remove from registry
                        print(f"   Action: Marked {local_path_str} for unlinking GDoc and removal from registry.")
                        if entry_data.get("google_doc_id"):
                            print(f"   Note: Associated GDoc ID was {entry_data['google_doc_id']}. It will NOT be deleted from Drive by this action.")
                        del doc_registry_map[local_path_str]
                        registry_updated = True
                        continue
                    elif choice == 'a':
                        print("   Sync aborted by user.")
                        sys.exit(1)
                    else: # Default 's' (skip)
                        print(f"   Action: Skipping sync for {local_path_str} this time.")
                        continue
                else: # Non-interactive
                    print(f"⚠️ Stale mapping: Local file not found at {absolute_local_path}. Skipping sync (non-interactive).")
                    continue

            # 2. Check Google Doc accessibility if doc_id exists
            if doc_id and doc_id != NEW_DOC_PLACEHOLDER: # Only check if there's an existing ID
                try:
                    gdoc_metadata = self.drive_service.files().get(fileId=doc_id, fields='id, name, trashed, version, headRevisionId').execute()
                    entry_data["google_doc_version"] = gdoc_metadata.get('headRevisionId') or gdoc_metadata.get('version') # Store latest known version
                    entry_data["google_doc_last_known_good_at"] = datetime.datetime.utcnow().isoformat() + "Z"

                    if gdoc_metadata.get('trashed'):
                        entry_data["status"] = "error_gdoc_trashed"
                        doc_registry_map[local_path_str] = entry_data
                        registry_updated = True
                        if self.cli_args and self.cli_args.interactive_session:
                            print(f"❓ Stale mapping: Google Doc for {local_path_str} (ID: {doc_id}) is in trash.")
                            choice = input("   Options: (C)reate new GDoc & link, (U)nlink (keep local file as 'local_only'), (S)kip, (A)bort? [S]: ").strip().lower()
                            if choice == 'c':
                                print(f"   Action: Will attempt to create a new GDoc for {local_path_str}.")
                                entry_data["google_doc_id"] = None # Mark for creation
                                doc_id = None # Ensure needs_creation logic picks it up
                            elif choice == 'u':
                                print(f"   Action: Unlinking {local_path_str} from GDoc ID {entry_data['google_doc_id']}. Local file kept.")
                                entry_data["google_doc_id"] = None
                                entry_data["status"] = "local_only" # Now it's just a local file
                                doc_registry_map[local_path_str] = entry_data
                                registry_updated = True
                                continue # Skip actual content sync for this iteration
                            elif choice == 'a':
                                print("   Sync aborted by user.")
                                sys.exit(1)
                            else: # Skip
                                print(f"   Action: Skipping sync for {local_path_str} this time.")
                                continue
                        else: # Non-interactive
                            print(f"⚠️ Stale mapping: Google Doc for {local_path_str} (ID: {doc_id}) is in trash. Skipping (non-interactive).")
                            entry_data["google_doc_id"] = None # Unlink it
                            doc_registry_map[local_path_str] = entry_data
                            registry_updated = True
                            continue
                except HttpError as e:
                    if e.resp.status == 404:
                        entry_data["status"] = "error_gdoc_not_found"
                        doc_registry_map[local_path_str] = entry_data
                        registry_updated = True
                        if self.cli_args and self.cli_args.interactive_session:
                            print(f"❓ Stale mapping: Google Doc for {local_path_str} (ID: {doc_id}) not found (404).")
                            choice = input("   Options: (C)reate new GDoc & link, (U)nlink (mark local as 'local_only'), (S)kip, (A)bort? [S]: ").strip().lower()
                            if choice == 'c':
                                print(f"   Action: Will attempt to create a new GDoc for {local_path_str}.")
                                entry_data["google_doc_id"] = None
                                doc_id = None
                            elif choice == 'u':
                                print(f"   Action: Unlinking {local_path_str}. Local file kept.")
                                entry_data["google_doc_id"] = None
                                entry_data["status"] = "local_only"
                                doc_registry_map[local_path_str] = entry_data
                                registry_updated = True
                                continue
                            elif choice == 'a':
                                print("   Sync aborted by user.")
                                sys.exit(1)
                            else: # Skip
                                print(f"   Action: Skipping sync for {local_path_str} this time.")
                                continue
                        else: # Non-interactive
                            print(f"⚠️ Stale mapping: Google Doc for {local_path_str} (ID: {doc_id}) not found (404). Skipping (non-interactive).")
                            entry_data["google_doc_id"] = None # Unlink it
                            doc_registry_map[local_path_str] = entry_data
                            registry_updated = True
                            continue
                    else:
                        print(f"⚠️ Warning: HTTP error checking Google Doc {doc_id} for {local_path_str}: {e}. Will attempt sync if possible.")
                        entry_data["status"] = "warning_gdoc_check_failed"

            live_gdoc_version_for_conflict_check = entry_data.get("google_doc_version") # Version from metadata check
            # --- BUG-002: Basic Stale Mapping Detection END ---


            # --- CONFLICT RESOLUTION (Concurrent Modification) START ---
            # Pre-conditions for conflict check:
            # - Local file exists (checked by stale mapping)
            # - GDoc is accessible (i.e., not trashed/404, checked by stale mapping)
            # - Not a --force-new scenario (which bypasses existing GDoc considerations)
            # - Not a 'needs_creation' scenario (no existing GDoc to conflict with)

            is_potential_conflict_scenario = (
                absolute_local_path.exists() and
                entry_data.get("google_doc_id") and
                entry_data.get("google_doc_id") != NEW_DOC_PLACEHOLDER and
                not (self.cli_args and self.cli_args.force_new) and
                entry_data.get("status") not in ["error_gdoc_trashed", "error_gdoc_not_found"] # Ensure GDoc was accessible
            )

            if is_potential_conflict_scenario:
                stored_local_hash = entry_data.get("local_sha256_hash")
                current_local_hash_for_conflict = calculate_sha256_hash(str(absolute_local_path)) # Recalculate for safety, or use one from earlier if sure it's fresh.

                stored_gdoc_version = entry_data.get("google_doc_version_at_last_sync") # Need a field for this. For now, use current GDoc version as proxy for 'version at last sync'
                                                                                       # This requires a more robust version tracking than currently implemented.
                                                                                       # Let's assume 'google_doc_version' field holds the version *before* current live check.
                                                                                       # This part is tricky. The 'live_gdoc_version_for_conflict_check' is the current live version.
                                                                                       # We need to compare current local hash with stored hash (from last sync)
                                                                                       # AND current GDoc version with stored GDoc version (from last sync).

                # Simplified: if local hash changed from registry AND live GDoc version changed from registry's last known GDoc version.
                # This means we need to ensure 'local_sha256_hash' and 'google_doc_version' in registry are from *last successful sync*.

                # For this phase, let's assume entry_data.local_sha256_hash and entry_data.google_doc_version are from last successful sync.
                # And current_local_hash_for_conflict and live_gdoc_version_for_conflict_check are the current live states.

                local_has_changed = current_local_hash_for_conflict != stored_local_hash if stored_local_hash else False
                remote_has_changed = live_gdoc_version_for_conflict_check != entry_data.get("google_doc_version") if entry_data.get("google_doc_version") else False
                # A true conflict is if BOTH have changed independently.
                # If only local changed, it's a simple push. If only remote changed, it's a pull (or warning).

                if local_has_changed and remote_has_changed:
                    print(f"🔥 CONFLICT: File '{local_path_str}' has changed locally AND on Google Drive since last sync.")
                    entry_data["status"] = "conflict"
                    registry_updated = True # status changed

                    if self.cli_args and self.cli_args.interactive_session:
                        choice = input("   Options: (L)ocal overwrites GDoc, (G)Doc overwrites local, (S)kip sync for this file? [S]: ").strip().lower()
                        if choice == 'l':
                            print(f"   Action: Local content will overwrite Google Doc for '{local_path_str}'.")
                            # Allow sync_file to proceed. Hash/version will be updated by sync_file logic.
                            entry_data["status"] = "conflict_resolved_local_wins" # Temporary status
                        elif choice == 'g':
                            print(f"   Action: Google Doc content will overwrite local file for '{local_path_str}'.")
                            gdoc_content = self._download_gdoc_as_markdown(entry_data["google_doc_id"])
                            if gdoc_content is not None:
                                try:
                                    with open(absolute_local_path, 'w', encoding='utf-8') as f_local:
                                        f_local.write(gdoc_content)
                                    print(f"     Successfully updated local file '{local_path_str}' with GDoc content.")
                                    # Update registry based on this action
                                    entry_data["local_sha256_hash"] = calculate_sha256_hash(str(absolute_local_path))
                                    entry_data["google_doc_version"] = live_gdoc_version_for_conflict_check # Already live version
                                    entry_data["last_synced_at"] = datetime.datetime.utcnow().isoformat() + "Z"
                                    entry_data["google_doc_last_known_good_at"] = entry_data["last_synced_at"]
                                    entry_data["status"] = "active" # Synced by GDoc pull
                                    doc_registry_map[local_path_str] = entry_data
                                    registry_updated = True
                                    # Add to synced_docs for URL summary, as it's now "synced"
                                    synced_docs.append({
                                        'file': local_path_str, 'doc_id': entry_data["google_doc_id"],
                                        'url': self.get_doc_url(entry_data["google_doc_id"])
                                    })
                                    total_count +=1 # Count as processed
                                    success_count +=1 # Count as success
                                    continue # Skip the normal sync_file call for this iteration
                                except Exception as e_write:
                                    print(f"     Error writing GDoc content to local file {local_path_str}: {e_write}")
                                    entry_data["status"] = "conflict_resolution_failed"
                                    # Fall through to skip or let user decide again? For now, it's effectively skipped.
                            else:
                                print(f"     Could not download GDoc content for {local_path_str}. Skipping overwrite.")
                                entry_data["status"] = "conflict_resolution_failed"
                            # If GDoc download failed, effectively skip
                            continue # Skip normal sync_file call
                        else: # Skip
                            print(f"   Action: Skipping sync for '{local_path_str}' due to conflict.")
                            continue # Skip normal sync_file call
                    else: # Non-interactive
                        print(f"   Conflict detected for '{local_path_str}' (non-interactive). Skipping.")
                        continue # Skip normal sync_file call
            # --- CONFLICT RESOLUTION (Concurrent Modification) END ---


            # Determine if a new Google Doc needs to be created (could be true after stale checks or --force-new)
            if self.cli_args and self.cli_args.force_new:
                print(f"ℹ️  --force-new specified: Will create a new Google Doc for {local_path_str}, even if one is already mapped.")
                entry_data["google_doc_id"] = None # Unlink any existing GDoc ID for this run
                doc_id = None # Ensure it's treated as needing creation
                needs_creation = True
            else:
                # If doc_id is missing or is placeholder (or cleared due to stale check), needs creation
                needs_creation = not entry_data.get("google_doc_id") or entry_data.get("google_doc_id") == NEW_DOC_PLACEHOLDER

            if needs_creation:
                # This check is now after stale mapping detection which might clear a doc_id or if --force-new is used
                print(f"ℹ️  Entry for {local_path_str} needs Google Doc creation (or re-creation).")
                title = os.path.basename(local_path_str)
                if title.endswith(".md"):
                    title = title[:-3]

                # Calculate hash before creation, as it's a property of the local file
                current_local_hash = calculate_sha256_hash(str(absolute_local_path))
                entry_data["local_sha256_hash"] = current_local_hash
                entry_data["last_modified_local_at"] = datetime.datetime.utcnow().isoformat() + "Z" # Time of check/hash

                creation_result = self.create_google_doc(title) # Returns dict
                if creation_result and creation_result.get("doc_id"):
                    doc_id = creation_result["doc_id"]
                    entry_data["google_doc_id"] = doc_id
                    entry_data["google_doc_version"] = creation_result.get("version")
                    entry_data["google_doc_last_known_good_at"] = creation_result.get("modified_time") or (datetime.datetime.utcnow().isoformat() + "Z")
                    entry_data["status"] = "active"
                    # Align sync time with GDoc mod time on creation if available, else now
                    entry_data["last_synced_at"] = entry_data["google_doc_last_known_good_at"]

                    doc_registry_map[local_path_str] = entry_data
                    registry_updated = True
                    print(f"   🔄 Updated registry for {local_path_str} with new Doc ID: {doc_id[:15]}..., Version: {creation_result.get('version')}")
                else:
                    print(f"❌ Failed to create Google Doc for {local_path_str}. Skipping.")
                    entry_data["status"] = "creation_failed"
                    doc_registry_map[local_path_str] = entry_data
                    registry_updated = True
                    continue
            
            # Calculate and store/update local file hash before syncing content for existing docs
            # This is also done before creation now, but ensure it's always fresh if not created.
            if not needs_creation:
                current_local_hash = calculate_sha256_hash(str(absolute_local_path))
                # Only mark as modified if hash actually changed or wasn't there
                if entry_data.get("local_sha256_hash") != current_local_hash:
                    entry_data["local_sha256_hash"] = current_local_hash
                    entry_data["last_modified_local_at"] = datetime.datetime.utcnow().isoformat() + "Z"
                    registry_updated = True
                # If hash is same, last_modified_local_at should ideally reflect actual file mod time,
                # but for now, this simplified update is acceptable.
                doc_registry_map[local_path_str] = entry_data

            total_count += 1
            sync_result = self.sync_file(str(absolute_local_path), doc_id, clean_escapes, show_url=(total_count <= 5)) # Returns dict

            if sync_result.get("success"):
                success_count += 1
                entry_data["last_synced_at"] = datetime.datetime.utcnow().isoformat() + "Z"
                entry_data["google_doc_version"] = sync_result.get("version")
                entry_data["google_doc_last_known_good_at"] = sync_result.get("modified_time") or entry_data["last_synced_at"]
                entry_data["status"] = "active"
                doc_registry_map[local_path_str] = entry_data
                registry_updated = True
                synced_docs.append({
                    'file': local_path_str,
                    'doc_id': doc_id,
                    'url': self.get_doc_url(doc_id)
                })
            else:
                entry_data["status"] = "sync_failed"
                doc_registry_map[local_path_str] = entry_data
                registry_updated = True
        
        if registry_updated: # Save at the end of all operations
            madio_registry.save_registry(registry_data)
            print(f"\n💾 Document registry updated.")

        # Display Google Doc URLs
        if synced_docs:
            print(f"==================")
            for doc in synced_docs:
                filename = os.path.basename(doc['file'])
                print(f"📄 {filename}")
                print(f"   {doc['url']}")
            
            # Save URLs to file for easy reference
            try:
                # Ensure urls_file is in project root for easier access by user
                project_root = madio_registry.get_project_root()
                urls_file_path = project_root / "google_docs_urls.txt"
                with open(urls_file_path, 'w') as f:
                    f.write("Synced Google Docs URLs\n")
                    f.write("=======================\n\n")
                    for doc_info in synced_docs: # Corrected variable name
                        f.write(f"{doc_info['file']}: {doc_info['url']}\n")
                print(f"\n💾 URLs saved to: {urls_file_path}")
            except Exception as e:
                print(f"⚠️  Could not save URLs file: {e}")
        
        # Enhanced sync summary
        print(f"\n📊 Sync Summary")
        print(f"================")
        print(f"✅ Successfully synced: {success_count} file(s)")
        print(f"📂 Total files processed from registry: {total_count} file(s)")
        
        if total_count > 0:
            success_rate = (success_count / total_count) * 100
            print(f"📈 Success rate: {success_rate:.1f}%")
        
        failed_count = total_count - success_count
        if failed_count > 0:
            print(f"❌ Failed/skipped syncs: {failed_count} file(s)")
        
        if registry_updated: # Check if the main registry object was marked for update
            print(f"💾 Document registry was updated.")
        
        print(f"🔧 Sync mode: Document Registry") # Always using registry now
        print(f"📅 Sync completed: {datetime.datetime.utcnow().isoformat()}Z")
        
        # Determine overall success. True if all processed files synced successfully.
        # If total_count is 0 but registry_updated is true (e.g. only folder prefs changed), consider it a success.
        return (total_count == 0 and registry_updated) or (total_count > 0 and success_count == total_count)


def main():
    parser = argparse.ArgumentParser(description='Sync markdown files to Google Docs using MADIO Document Registry')
    # --file and --doc-id are for specific single file sync, less common now but can be kept for utility
    parser.add_argument('--file', help='Specific local file path (relative to project root) to sync.')
    parser.add_argument('--doc-id', help='Google Doc ID to sync the specific file to (optional, will use registry if available).')

    # --config, --directory, --mapping-file, --pattern, --exclude are now obsolete as primary mechanisms
    # They can be removed or kept if there's a specific utility for them outside normal flow.
    # For Phase 1, let's simplify and assume they are not used for the main sync_all_files path.
    # We will re-evaluate if `sync_file` needs them or if it also uses registry.

    parser.add_argument('--folder', help='Google Drive folder name for documents (e.g., "MADIO Docs"). Overrides registry preference for this run. Creates folder if needed.')
    # Add --folder-id for more precise folder specification
    parser.add_argument('--folder-id', help='Google Drive folder ID for documents. Overrides --folder and registry preference.')

    parser.add_argument('--no-clean', action='store_true', help='Skip cleaning escaped markdown characters.')
    parser.add_argument('--force-new', action='store_true', help='Force creation of new Google Docs for all files, even if mappings exist.')
    parser.add_argument('--credentials', default='credentials.json', help='Google credentials file')
    parser.add_argument('--token', default='token.pickle', help='Token file for authentication')
    # --interactive flag is kept for backward compatibility if scripts relied on it, but new logic uses --interactive-session
    parser.add_argument('--interactive', action='store_true', help='DEPRECATED: Force interactive mode. Use --interactive-session.')
    parser.add_argument('--interactive-session', action='store_true', help='Indicates that an interactive session is intended by the user.')
    
    args = parser.parse_args()
    
    try:
        sync = GoogleDocsSync(args.credentials, args.token)
        sync.set_cli_args(args) # Store args
        sync.authenticate() # Now authenticate
        
        if args.file: # Specific file sync mode
            if not args.doc_id:
                # Try to get doc_id from registry if not provided
                registry_data = madio_registry.load_registry()
                # Ensure args.file is relative to project root for registry lookup
                project_root = madio_registry.get_project_root()
                try:
                    # Convert args.file to be relative to project_root if it's not already
                    # This assumes args.file might be passed as absolute or relative to cwd
                    abs_file_path = Path(args.file).resolve()
                    relative_file_path_str = str(abs_file_path.relative_to(project_root))
                except ValueError: # Not under project root if this fails
                    print(f"❌ Error: File {args.file} is not under project root {project_root}.")
                    sys.exit(1)

                doc_entry = madio_registry.get_document_entry(registry_data, relative_file_path_str)
                if doc_entry and doc_entry.get("google_doc_id"):
                    args.doc_id = doc_entry["google_doc_id"]
                    print(f"ℹ️  Found Google Doc ID {args.doc_id} in registry for file {relative_file_path_str}.")
                else:
                    print(f"❌ --doc-id is required for --file mode if not in registry, or use '{NEW_DOC_PLACEHOLDER}' to create new.")
                    sys.exit(1)
            
            # Resolve file path from project root for sync_file function
            file_path_to_sync = str(madio_registry.get_project_root() / relative_file_path_str)
            clean_escapes = not args.no_clean
            # Note: sync_file does not currently handle folder preferences from registry.
            # This mode is more of a direct utility. For folder handling, use general sync.
            success = sync.sync_file(file_path_to_sync, args.doc_id, clean_escapes, show_url=True)
            sys.exit(0 if success else 1)
        
        else: # General sync all mode (uses registry)
            clean_escapes = not args.no_clean
            
            # Determine target_folder_override from --folder-id or --folder
            target_folder_name_override = None
            if args.folder_id: # --folder-id takes precedence
                # We need to find the folder name if only ID is given, or pass ID directly
                # For now, sync_all_files expects a name to search or create.
                # This part needs refinement if we want to pass ID directly to sync_all_files
                # Let's assume for now we pass the ID and let sync_all_files handle it,
                # OR we make sync_all_files accept folder_id directly.
                # The PRD implies user provides name, script finds/creates ID.
                # Let's adjust sync_all_files to handle target_folder_id_override.
                # For now, this path is complex. Let's simplify: if --folder-id, we can't easily get name.
                # The current sync_all_files is better suited to take folder name.
                # So, if args.folder_id is provided, we'd ideally convert it to a name or have sync_all_files use it.
                # This is a TODO: Handle --folder-id more gracefully if name is needed for find/create logic.
                # For Phase 1, --folder (name) is the primary override.
                print(f"ℹ️  --folder-id specified: {args.folder_id}. This will be used if possible, but name-based logic is primary for folder creation.")
                # We can pass the folder_id to target_folder_override and let sync_all_files decide.
                # However, sync_all_files currently uses find_folder_by_name.
                # This needs more thought. For now, let's prioritize --folder.
                if args.folder:
                    target_folder_name_override = args.folder
                else:
                    print("Warning: --folder-id used without --folder. Name based search/creation might be an issue. Please provide --folder as well for now if creating new.")
                    # Ideally, we'd fetch folder name using ID, or pass ID to create_google_doc.
                    # This is a simplification for Phase 1.
                    target_folder_name_override = None # No name to use for creation if not found by ID
                    sync.target_folder_id = args.folder_id # Directly set if ID is given
                    print(f"📂 Using explicit folder ID: {args.folder_id}. Document creation will use this folder.")

            elif args.folder:
                target_folder_name_override = args.folder
            
            success = sync.sync_all_files(
                clean_escapes=clean_escapes,
                target_folder_override=target_folder_name_override # Pass the name
            )
            sys.exit(0 if success else 1)
            
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
