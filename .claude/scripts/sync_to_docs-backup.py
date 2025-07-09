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

# Scopes required for Google Docs API
SCOPES = ['https://www.googleapis.com/auth/documents']

class GoogleDocsSync:
    def __init__(self, credentials_file='credentials.json', token_file='token.pickle'):
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
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
        print("✅ Google Docs authentication successful")
    
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
            if doc_length > 0:
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
        
        success_count = 0
        total_count = 0
        
        for file_path, doc_id in config.items():
            # Skip configuration comments
            if file_path.startswith('_'):
                continue
                
            if doc_id == "REPLACE_WITH_GOOGLE_DOC_ID":
                print(f"⚠️  Skipping {file_path} - no Google Doc ID configured")
                continue
            
            if not os.path.exists(file_path):
                print(f"⚠️  File not found: {file_path}")
                continue
            
            total_count += 1
            if self.sync_file(file_path, doc_id, clean_escapes):
                success_count += 1
        
        print(f"\n📊 Sync complete: {success_count}/{total_count} files synced successfully")
        return success_count == total_count


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
