#!/usr/bin/env python3
"""
Google Docs Sync Script for MADIO Framework
Syncs local markdown files to Google Docs for Claude Project integration
"""

import json
import os
import sys
import argparse
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes required for Google Docs and Drive APIs
SCOPES = ['https://www.googleapis.com/auth/documents', 'https://www.googleapis.com/auth/drive']

# Placeholder for new documents in config
NEW_DOC_PLACEHOLDER = "CREATE_NEW_DOCUMENT"

class GoogleDocsSync:
    def __init__(self, credentials_file='credentials.json', token_file='token.pickle'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.drive_service = None
        self.target_folder_id = None
        self.authenticate()
    
    def authenticate(self):
        """Authenticate with Google Docs API"""
        creds = None
        
        # Check if token file exists
        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, SCOPES)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    print(f"❌ Credentials file not found: {self.credentials_file}")
                    print("Please download credentials.json from Google Cloud Console")
                    sys.exit(1)
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())
        
        self.service = build('docs', 'v1', credentials=creds)
        self.drive_service = build('drive', 'v3', credentials=creds)
        print("✅ Google Docs and Drive authentication successful")
    
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
            print(f"❌ Error searching for folder \"{folder_name}\": {error}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error searching for folder \"{folder_name}\": {e}")
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
            print(f"❌ Error creating folder \"{folder_name}\": {error}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error creating folder \"{folder_name}\": {e}")
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
            print(f"❌ Error updating Google Doc {doc_id}: {error}")
            return False
        except Exception as e:
            print(f"❌ Unexpected error updating Google Doc {doc_id}: {e}")
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
            print(f"❌ Error creating Google Doc \"{title}\": {error}")
            return None
        except Exception as e:
            print(f"❌ Unexpected error creating Google Doc \"{title}\": {e}")
            return None
    
    def sync_file(self, file_path, doc_id, clean_escapes=True):
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
        else:
            print(f"❌ Failed to sync {file_path}")
        
        return success
    
    def sync_all_files(self, config_file='sync_config.json', clean_escapes=True):
        """Sync all files based on configuration"""
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
        
        # Create a copy of keys to iterate over, allowing modification of original dict
        for file_path in list(config.keys()):
            doc_id = config[file_path]

            # Skip configuration comments
            if file_path.startswith('_'):
                continue
            
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
                    config_updated = True
                    print(f"   🔄 Updated config for {file_path} with new Doc ID: {new_doc_id[:15]}...")
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
            if self.sync_file(file_path, doc_id, clean_escapes):
                success_count += 1
        
        if config_updated:
            print(f"\n💾 Updating configuration file: {config_file}...")
            try:
                with open(config_file, 'w') as f:
                    json.dump(config, f, indent=2)
                print(f"✅ Configuration file updated successfully.")
            except IOError as e:
                print(f"❌ Error writing updated configuration to {config_file}: {e}")
                print("   Please check file permissions and path.")
        
        print(f"\n📊 Sync complete: {success_count}/{total_count} files synced successfully")
        return success_count == total_count and not (total_count == 0 and config_updated) # Success if all synced or only config updated


def main():
    parser = argparse.ArgumentParser(description='Sync markdown files to Google Docs')
    parser.add_argument('--file', help='Specific file to sync')
    parser.add_argument('--doc-id', help='Google Doc ID (required with --file)')
    parser.add_argument('--config', default='sync_config.json', help='Config file path')
    parser.add_argument('--no-clean', action='store_true', help='Skip cleaning escaped markdown characters')
    parser.add_argument('--credentials', default='credentials.json', help='Google credentials file')
    parser.add_argument('--token', default='token.pickle', help='Token file for authentication')
    
    args = parser.parse_args()
    
    # Change to script directory for relative paths
    script_dir = Path(__file__).parent
    os.chdir(script_dir)
    
    try:
        sync = GoogleDocsSync(args.credentials, args.token)
        
        if args.file:
            if not args.doc_id:
                print("❌ --doc-id is required when using --file")
                sys.exit(1)
            
            # Go back to project root for file access
            os.chdir('../..')
            clean_escapes = not args.no_clean
            success = sync.sync_file(args.file, args.doc_id, clean_escapes)
            sys.exit(0 if success else 1)
        else:
            # Handle config file path - check if it's relative to script dir or project root
            config_path = args.config
            if not os.path.exists(config_path):
                # Try project root
                os.chdir('../..')
                if not os.path.exists(config_path):
                    # Try back in script directory
                    os.chdir('.claude/scripts')
                    if not os.path.exists(config_path):
                        print(f"❌ Config file not found: {config_path}")
                        sys.exit(1)
                    # Config found in script dir, but we need to be in project root for file access
                    os.chdir('../..')
                    config_path = f'.claude/scripts/{args.config}'
            
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
