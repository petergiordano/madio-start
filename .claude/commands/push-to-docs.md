# Push to Google Docs Command

Sync local markdown files to Google Docs for Claude Project integration.

## Usage

### Sync all configured files
```bash
cd .claude/scripts
python3 sync_to_docs.py --config sync_config.json
```

### Sync specific file
```bash
/push-to-docs --file methodology_framework.md 1ABC...xyz
```

### Use custom config
```bash
/push-to-docs --config my_sync_config.json
```

### Skip markdown cleanup (if needed)
```bash
/push-to-docs --no-clean  # Skip cleaning escaped markdown characters
```

## Setup Required

### 1. Install dependencies
```bash
cd .claude/scripts
pip install -r requirements.txt
```

### 2. Get Google credentials
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create project or select existing
3. Enable Google Docs API **and Google Drive API**
4. Create OAuth2 credentials (Desktop application)
5. Download `credentials.json` to `.claude/scripts/`

### 3. Configure sync mapping
Create `sync_config.json` in `.claude/scripts/`:
```json
{
  "_google_drive_folder": {
    "name": "",
    "id": "",
    "description": "Google Drive folder for documents. Leave name empty for root folder."
  },
  "../../project_system_instructions.md": "CREATE_NEW_DOCUMENT",
  "../../orchestrator.md": "CREATE_NEW_DOCUMENT",
  "../../methodology_framework.md": "CREATE_NEW_DOCUMENT"
}
```

**✨ NEW: Google Drive Folder Organization**
- Configure `_google_drive_folder.name` to organize documents in specific folders
- Script automatically creates folders if they don't exist
- Leave name empty for root folder (My Drive)
- Interactive prompts guide folder selection

**✨ NEW: Automatic Document Creation**
- Use `CREATE_NEW_DOCUMENT` placeholder for new files
- Script automatically creates Google Docs and updates config
- No manual Google Doc ID copying required!

### 4. First-time authentication
Run `/push-to-docs` - browser will open for Google OAuth consent.

**⚠️ Important**: If you previously used this script, delete `token.pickle` to re-authenticate with new Google Drive permissions.

## How it works

1. **NEW**: Configures Google Drive folder organization (interactive prompts)
2. Reads local `.md` files
3. **NEW**: Auto-creates Google Docs for `CREATE_NEW_DOCUMENT` placeholders
4. **NEW**: Places documents in specified Google Drive folders
5. **NEW**: Automatically cleans escaped markdown characters from Google Docs exports
6. Completely replaces Google Doc content
7. Auto-updates config file with new Google Doc IDs and folder settings
8. Preserves document ID for Claude Project
9. All Google Docs auto-update in Claude Project knowledge

### ✨ New: Automatic Markdown Cleanup

The sync now automatically fixes escaped markdown characters from Google Docs exports:

**Before (Escaped):**
```
\# Header
\- List item
\*emphasis\*
\1. Numbered list
```

**After (Cleaned):**
```
# Header
- List item
*emphasis*
1. Numbered list
```

This solves the common issue where Google Docs "Download as Markdown" adds backslashes before markdown syntax.

## Command Implementation

```python
import subprocess
import sys
import os

def run_sync():
    script_path = os.path.join('.claude', 'scripts', 'sync_to_docs.py')
    if not os.path.exists(script_path):
        print("❌ Sync script not found. Run setup first.")
        return
    
    # Pass through all arguments
    args = ['python', script_path] + sys.argv[1:]
    subprocess.run(args)

if __name__ == "__main__":
    run_sync()
```

## Workflow Integration

### MADIO Development Cycle
1. Create local `.md` files (or let Claude edit via MCP filesystem)
2. Run `/push-to-docs` to configure Google Drive folders (first time only)
3. Auto-create Google Docs and sync content to organized folders
4. Configuration automatically updates with new Google Doc IDs and folder settings
5. Claude Project automatically picks up changes
6. Continuous framework evolution with seamless document management

### File Watching (Optional)
Auto-sync on file changes:
```bash
# Install watcher
npm install -g chokidar-cli

# Watch and auto-sync
chokidar "*.md" -c "/push-to-docs"
```

## Troubleshooting

### Authentication Issues
- Ensure `credentials.json` is in `.claude/scripts/`
- Delete `token.pickle` and re-authenticate if needed
- Check Google Cloud Console for API quotas

### Sync Failures
- Verify Google Doc IDs in `sync_config.json`
- Ensure you have edit access to all Google Docs
- Check file permissions for local markdown files
- **NEW**: Ensure Google Drive API is enabled in Google Cloud Console
- **NEW**: Verify folder permissions if using custom folders

### Performance
- Large documents may take longer to sync
- Rate limiting applies to Google Docs API
- Consider batch operations for multiple files
