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

# Placeholder for new documents in config
NEW_DOC_PLACEHOLDER = "CREATE_NEW_DOCUMENT"

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
        self.authenticate()
    
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
    
    def prompt_for_folder(self):
        """Prompt user for Google Drive folder selection"""
        print("\n📁 Google Drive Folder Configuration")
        print("   Choose where to create your Google Docs:")
        print("   • Press Enter for root folder (My Drive)")
        print("   • Enter folder name (e.g., 'MADIO Docs')")
        print("   • If folder doesn't exist, you'll be asked to create it")
        
        while True:
            folder_name = input("\nEnter Google Drive folder name (or press Enter for root): ").strip()
            
            if not folder_name:
                print("📂 Using root folder (My Drive)")
                return None
            
            # Search for the folder
            folder_id = self.find_folder_by_name(folder_name)
            
            if folder_id:
                return {'name': folder_name, 'id': folder_id}
            else:
                # Folder not found, ask to create
                print(f"\n❓ Folder \"{folder_name}\" not found.")
                create_choice = input("Create this folder? (y/N): ").strip().lower()
                
                if create_choice == 'y' or create_choice == 'yes':
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
            
            return True
            
        except HttpError as error:
            error_type = handle_http_error(error, f"updating Google Doc {doc_id[:15]}...")
            if error_type == "rate_limited":
                # Try with rate limiting retry
                def retry_update():
                    return self.update_google_doc(doc_id, content)
                return retry_on_rate_limit(lambda: False) != False  # Returns True if retry succeeds
            return False
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

    def create_google_doc(self, title):
        """Create a new Google Doc and return its ID."""
        try:
            print(f"➕ Creating new Google Doc with title: \"{title}\"...")
            document_body = {'title': title}
            doc = self.service.documents().create(body=document_body).execute()
            doc_id = doc.get('documentId')
            print(f"✅ Successfully created Google Doc with ID: {doc_id}")
            
            # Move to target folder if specified
            if self.target_folder_id:
                success = self.move_document_to_folder(doc_id, self.target_folder_id)
                if not success:
                    print(f"⚠️  Document created but failed to move to folder")
            
            return doc_id
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
        
        success = self.update_google_doc(doc_id, content)
        if success:
            print(f"✅ Successfully synced {file_path}")
            if show_url:
                print(f"   🔗 View: {self.get_doc_url(doc_id)}")
        else:
            print(f"❌ Failed to sync {file_path}")
        
        return success
    
    def sync_all_files(self, config_file='sync_config.json', clean_escapes=True, directory_path=None, mapping_file='.synced_docs_mapping.json', include_pattern=None, exclude_pattern=None):
        """Sync all files based on configuration or directory discovery"""
        config = {}
        config_updated = False
        
        if directory_path:
            # Directory mode - discover files and create temporary config
            print(f"🔍 Directory mode: scanning {directory_path} for markdown files")
            config = self.create_directory_config(directory_path, mapping_file, include_pattern, exclude_pattern)
            if not config:
                print(f"❌ No markdown files found in directory: {directory_path}")
                return False
        else:
            # Traditional config file mode
            if not os.path.exists(config_file):
                print(f"❌ Config file not found: {config_file}")
                return False
            
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
            except json.JSONDecodeError as e:
                print(f"❌ Invalid JSON in config file: {e}")
                return False
        
        # Handle folder configuration
        folder_config = config.get('_google_drive_folder', {})
        
        # Check if folder is already configured
        if folder_config.get('id'):
            folder_name = folder_config.get('name', 'configured folder')
            folder_id = folder_config.get('id')
            print(f"📂 Using configured folder: \"{folder_name}\" ({folder_id[:15]}...)")
            self.target_folder_id = folder_id
        elif folder_config.get('name'):
            # Folder name specified but no ID - search for it
            folder_name = folder_config.get('name')
            folder_id = self.find_folder_by_name(folder_name)
            if folder_id:
                print(f"📂 Found folder: \"{folder_name}\" ({folder_id[:15]}...)")
                self.target_folder_id = folder_id
                # Update config with found folder ID
                config['_google_drive_folder']['id'] = folder_id
                config_updated = True
            else:
                print(f"❌ Configured folder \"{folder_name}\" not found")
                return False
        else:
            # No folder configured - prompt user or use root
            try:
                folder_info = self.prompt_for_folder()
                if folder_info:
                    print(f"📂 Selected folder: \"{folder_info['name']}\" ({folder_info['id'][:15]}...)")
                    self.target_folder_id = folder_info['id']
                    # Update config with selected folder
                    config['_google_drive_folder'] = {
                        'name': folder_info['name'],
                        'id': folder_info['id'],
                        'description': "Google Drive folder for documents. Leave name empty for root folder."
                    }
                    config_updated = True
                else:
                    print("📂 Using root folder (My Drive)")
                    self.target_folder_id = None
            except (EOFError, KeyboardInterrupt):
                print("\n📂 Using root folder (My Drive)")
                self.target_folder_id = None
        
        success_count = 0
        total_count = 0
        mapping_updated = False
        synced_docs = []  # Track successfully synced documents
        
        # Create a copy of keys to iterate over, allowing modification of original dict
        config_files = [fp for fp in config.keys() if not fp.startswith('_')]
        
        # Progress indicator for sync operations
        if TQDM_AVAILABLE and len(config_files) > 3:
            file_iterator = tqdm(config_files, desc="🔄 Syncing files", unit="file")
        else:
            file_iterator = config_files
            if len(config_files) > 1:
                print(f"🔄 Syncing {len(config_files)} files...")
        
        for file_path in file_iterator:
            doc_id = config[file_path]
            
            if doc_id == NEW_DOC_PLACEHOLDER:
                print(f"ℹ️  Found placeholder for {file_path}. Attempting to create new Google Doc.")
                # Derive title from filename
                title = os.path.basename(file_path)
                # Potentially remove .md extension from title if desired
                if title.endswith(".md"):
                    title = title[:-3]
                
                new_doc_id = self.create_google_doc(title)
                
                if new_doc_id:
                    config[file_path] = new_doc_id
                    doc_id = new_doc_id  # Use the new ID for syncing this iteration
                    
                    # Update appropriate mapping
                    if directory_path:
                        # Update directory mapping
                        existing_mapping = self.load_directory_mapping(mapping_file)
                        existing_mapping[file_path] = new_doc_id
                        self.save_directory_mapping(existing_mapping, mapping_file)
                        mapping_updated = True
                    else:
                        # Update config file
                        config_updated = True
                    
                    print(f"   🔄 Updated mapping for {file_path} with new Doc ID: {new_doc_id[:15]}...")
                else:
                    print(f"❌ Failed to create Google Doc for {file_path}. Skipping sync for this file.")
                    continue  # Skip to the next file if creation failed
            
            elif doc_id == "REPLACE_WITH_GOOGLE_DOC_ID": # Legacy placeholder
                print(f"⚠️  Skipping {file_path} - uses legacy placeholder. Update to '{NEW_DOC_PLACEHOLDER}' to enable auto-creation.")
                continue

            if not os.path.exists(file_path):
                # This check should be after potential doc creation,
                # as a new file might not exist yet if config was prepared in advance.
                # However, for syncing content, the local file must exist.
                print(f"⚠️  Local file not found: {file_path}. Skipping sync for this file.")
                continue
            
            total_count += 1
            if self.sync_file(file_path, doc_id, clean_escapes, show_url=(total_count <= 5)):
                success_count += 1
                # Track successful syncs for URL summary
                synced_docs.append({
                    'file': file_path,
                    'doc_id': doc_id,
                    'url': self.get_doc_url(doc_id)
                })
        
        # Save updates based on mode
        if config_updated and not directory_path:
            print(f"\n💾 Updating configuration file: {config_file}...")
            try:
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=2)
                print(f"✅ Configuration file updated successfully.")
            except IOError as e:
                print(f"❌ Error writing updated configuration to {config_file}: {e}")
                print("   Please check file permissions and path.")
        
        # Display Google Doc URLs for successfully synced files
        if synced_docs:
            print(f"\n🔗 Google Doc URLs")
            print(f"==================")
            for doc in synced_docs:
                filename = os.path.basename(doc['file'])
                print(f"📄 {filename}")
                print(f"   {doc['url']}")
            
            # Save URLs to file for easy reference
            try:
                urls_file = "google_docs_urls.txt"
                with open(urls_file, 'w') as f:
                    f.write("Google Docs URLs\n")
                    f.write("================\n\n")
                    for doc in synced_docs:
                        f.write(f"{doc['file']}: {doc['url']}\n")
                print(f"\n💾 URLs saved to: {urls_file}")
            except Exception as e:
                print(f"⚠️  Could not save URLs file: {e}")
        
        # Enhanced sync summary with detailed statistics
        print(f"\n📊 Sync Summary")
        print(f"================")
        print(f"✅ Successfully synced: {success_count} files")
        print(f"📂 Total files processed: {total_count} files")
        
        if total_count > 0:
            success_rate = (success_count / total_count) * 100
            print(f"📈 Success rate: {success_rate:.1f}%")
        
        failed_count = total_count - success_count
        if failed_count > 0:
            print(f"❌ Failed syncs: {failed_count} files")
        
        if config_updated or mapping_updated:
            print(f"💾 Configuration updated: {'Yes' if config_updated or mapping_updated else 'No'}")
        
        if directory_path and mapping_updated:
            print(f"📋 Mapping file updated: {mapping_file}")
        
        # Show sync mode
        sync_mode = "Directory" if directory_path else "Config"
        print(f"🔧 Sync mode: {sync_mode}")
        
        print(f"📅 Sync completed: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        return success_count == total_count and not (total_count == 0 and config_updated) # Success if all synced or only config updated


def main():
    parser = argparse.ArgumentParser(description='Sync markdown files to Google Docs')
    parser.add_argument('--file', help='Specific file to sync')
    parser.add_argument('--doc-id', help='Google Doc ID (required with --file)')
    parser.add_argument('--config', default='sync_config.json', help='Config file path')
    parser.add_argument('--directory', help='Directory to scan for markdown files (e.g., synced_docs)')
    parser.add_argument('--mapping-file', default='.synced_docs_mapping.json', help='File to store directory-to-doc-ID mappings')
    parser.add_argument('--pattern', help='Glob pattern to include specific files (e.g., "tier3_*.md")')
    parser.add_argument('--exclude', help='Glob pattern to exclude files (e.g., "test_*.md")')
    parser.add_argument('--no-clean', action='store_true', help='Skip cleaning escaped markdown characters')
    parser.add_argument('--credentials', default='credentials.json', help='Google credentials file')
    parser.add_argument('--token', default='token.pickle', help='Token file for authentication')
    
    args = parser.parse_args()
    
    try:
        sync = GoogleDocsSync(args.credentials, args.token)
        
        if args.file:
            if not args.doc_id:
                print("❌ --doc-id is required when using --file")
                sys.exit(1)
            
            # Resolve file path from project root
            file_path = resolve_from_root(args.file)
            clean_escapes = not args.no_clean
            success = sync.sync_file(file_path, args.doc_id, clean_escapes)
            sys.exit(0 if success else 1)
        
        elif args.directory:
            # Directory mode - scan directory for markdown files
            # Resolve directory path from project root
            directory_path = resolve_from_root(args.directory)
            mapping_file = args.mapping_file
            
            clean_escapes = not args.no_clean
            success = sync.sync_all_files(
                config_file=args.config, 
                clean_escapes=clean_escapes,
                directory_path=directory_path,
                mapping_file=mapping_file,
                include_pattern=args.pattern,
                exclude_pattern=args.exclude
            )
            sys.exit(0 if success else 1)
        
        else:
            # Traditional config file mode
            # Resolve config file path - try script directory first, then project root
            config_path = args.config
            
            # If relative path, try script directory first
            if not os.path.isabs(config_path):
                script_config_path = resolve_script_file(config_path)
                if os.path.exists(script_config_path):
                    config_path = script_config_path
                else:
                    # Try relative to project root
                    root_config_path = resolve_from_root(config_path)
                    if os.path.exists(root_config_path):
                        config_path = root_config_path
                    else:
                        print(f"❌ Config file not found: {args.config}")
                        print(f"   Tried: {script_config_path}")
                        print(f"   Tried: {root_config_path}")
                        sys.exit(1)
            
            clean_escapes = not args.no_clean
            success = sync.sync_all_files(config_path, clean_escapes)
            sys.exit(0 if success else 1)
            
    except KeyboardInterrupt:
        print("\n❌ Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
