# Push to Google Docs Command

Sync local markdown files to Google Docs for Claude Project integration.

## Usage

### Sync all configured files
```bash
/push-to-docs
```

### Sync specific file
```bash
/push-to-docs --file methodology_framework.md 1ABC...xyz
```

### Use custom config
```bash
/push-to-docs --config my_sync_config.json
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
3. Enable Google Docs API
4. Create OAuth2 credentials (Desktop application)
5. Download `credentials.json` to `.claude/scripts/`

### 3. Configure sync mapping
Create `sync_config.json` in project root:
```json
{
  "project_system_instructions.md": "1ABC...xyz",
  "orchestrator.md": "1DEF...xyz",
  "methodology_framework.md": "1GHI...xyz"
}
```

### 4. First-time authentication
Run `/push-to-docs` - browser will open for Google OAuth consent.

## How it works

1. Reads local `.md` files
2. Completely replaces Google Doc content
3. Preserves document ID for Claude Project
4. All Google Docs auto-update in Claude Project knowledge

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
1. Claude edits local `.md` files via MCP filesystem
2. Run `/push-to-docs` to sync to Google Docs
3. Claude Project automatically picks up changes
4. Continuous framework evolution

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

### Performance
- Large documents may take longer to sync
- Rate limiting applies to Google Docs API
- Consider batch operations for multiple files
