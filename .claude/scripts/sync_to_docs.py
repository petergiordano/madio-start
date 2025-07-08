#!/usr/bin/env python3
"""
MADIO Google Docs Sync Tool
Syncs local markdown files to Google Docs for Claude Project integration
"""

import json
import os
import sys
from pathlib import Path
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.exceptions import RefreshError
import pickle

# Scopes required for Google Docs API
SCOPES = ['https://www.googleapis.com/auth/documents']

class GoogleDocsSyncer:
    def __init__(self, credentials_path=None):
        self.credentials_path = credentials_path or '.claude/scripts/credentials.json'
        self.token_path = '.claude/scripts/token.pickle'
        self.service = None
        
    def authenticate(self):
        """Authenticate with Google Docs API"""
        creds = None
        
        # Load existing token
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                creds = pickle.load(token)
        
        # If no valid credentials, get new ones
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except RefreshError:
                    os.remove(self.token_path)
                    return self.authenticate()
            else:
                if not os.path.exists(self.credentials_path):
                    print(f"❌ Credentials file not found: {self.credentials_path}")
                    print("Please download OAuth2 credentials from Google Cloud Console")
                    sys.exit(1)
                    
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, SCOPES)
                creds = flow.run_local_server(port=0)
            
            # Save credentials for next run
            with open(self.token_path, 'wb') as token:
                pickle.dump(creds, token)
        
        self.service = build('docs', 'v1', credentials=creds)
        return True
    
    def sync_file(self, md_file_path, doc_id):
        """Sync a single markdown file to Google Doc"""
        try:
            # Read markdown content
            with open(md_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Get document info
            doc = self.service.documents().get(documentId=doc_id).execute()
            doc_title = doc.get('title', 'Unknown')
            
            # Clear existing content and replace
            requests = [
                # Delete all content except the first character (required)
                {
                    'deleteContentRange': {
                        'range': {
                            'startIndex': 1,
                            'endIndex': len(doc.get('body', {}).get('content', [{}])[0].get('paragraph', {}).get('elements', [{}])[0].get('textRun', {}).get('content', '')) or 2
                        }
                    }
                },
                # Insert new content
                {
                    'insertText': {
                        'location': {'index': 1},
                        'text': content
                    }
                }
            ]
            
            # Execute the update
            self.service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
            print(f"✅ Synced {md_file_path} → {doc_title}")
            return True
            
        except FileNotFoundError:
            print(f"❌ File not found: {md_file_path}")
            return False
        except Exception as e:
            print(f"❌ Error syncing {md_file_path}: {str(e)}")
            return False
    
    def sync_all(self, config_file='sync_config.json'):
        """Sync all files defined in config"""
        if not os.path.exists(config_file):
            print(f"❌ Config file not found: {config_file}")
            print("Create sync_config.json with markdown files and Google Doc IDs")
            return False
        
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        success_count = 0
        total_count = len(config)
        
        for md_file, doc_id in config.items():
            if md_file.startswith('_'):  # Skip comment lines
                continue
            if self.sync_file(md_file, doc_id):
                success_count += 1
        
        print(f"\n📊 Sync complete: {success_count}/{total_count} files synced")
        return success_count == total_count

def main():
    """Main function to handle command line usage"""
    syncer = GoogleDocsSyncer()
    
    # Authenticate
    print("🔐 Authenticating with Google...")
    if not syncer.authenticate():
        print("❌ Authentication failed")
        sys.exit(1)
    
    print("✅ Authentication successful")
    
    # Handle command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == '--file' and len(sys.argv) == 4:
            # Sync specific file
            md_file = sys.argv[2]
            doc_id = sys.argv[3]
            syncer.sync_file(md_file, doc_id)
        elif sys.argv[1] == '--config' and len(sys.argv) == 3:
            # Use custom config file
            syncer.sync_all(sys.argv[2])
        else:
            print("Usage:")
            print("  python sync_to_docs.py                    # Sync all (default config)")
            print("  python sync_to_docs.py --file <file> <id> # Sync specific file")
            print("  python sync_to_docs.py --config <file>    # Use custom config")
    else:
        # Sync all with default config
        syncer.sync_all()

if __name__ == "__main__":
    main()
