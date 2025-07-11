# Push to Google Docs Command

Sync local AI system documents to Google Docs for Claude Project integration.

## Primary Usage (Recommended)

### Sync all AI system documents
```bash
/push-to-docs
```

**What this does:**
1. Reads the `.madio/document_registry.json` to identify documents to be synced.
2. **Prompts you to choose/confirm Google Drive folder** if not already set in `sync_preferences` within the registry, or if an override like `--folder "Name"` is used.
3. Creates the Google Drive folder if it doesn't exist.
4. For each relevant document in the registry:
    - Compares local file hash with stored hash.
    - Compares Google Doc version (if linked) with stored version.
    - Handles stale mappings (e.g., missing local file, inaccessible GDoc) potentially interactively.
    - Handles conflicts (local & remote changes) potentially interactively.
    - Syncs content from local to Google Doc (creating GDoc if new or re-linking).
5. Updates `.madio/document_registry.json` with latest hashes, GDoc IDs, versions, timestamps, and statuses.

**Expected interaction:**
```
📁 Google Drive Folder Selection
   Where should your Google Docs be created?
   
   1. Root folder (My Drive) - Press Enter
   2. Organized folder (recommended) - Enter folder name
   
Enter folder name or press Enter for root [recommended: "MADIO Docs"]: 
```

## Advanced Usage (Direct Script Access)

### Sync with specific folder (non-interactive)
```bash
cd .claude/scripts
python3 sync_to_docs.py --folder "MADIO Docs" # No --directory needed, uses registry
```

### Sync to root folder (non-interactive, if folder not set in registry)
```bash
cd .claude/scripts
python3 sync_to_docs.py # Uses registry, defaults to root if no pref
```

### Adding `--force-new` (Example)
```bash
/push-to-docs --force-new
# or
cd .claude/scripts
python3 sync_to_docs.py --force-new --folder "Optional Target Folder"
```

## Setup Required

Refer to the main `SYNC_SETUP.md` guide for initial Google Cloud credential setup and Python dependency installation. This command assumes that setup is complete and that your project's documents are managed via `.madio/document_registry.json`.

**If migrating from an older project:** Run `/madio-migrate-config` first.

## How it works

1.  The `/push-to-docs` command (this file, a bash script) primarily invokes the Python script `.claude/scripts/sync_to_docs.py`.
2.  `sync_to_docs.py` now performs the following:
    *   Loads the document list and their states from `.madio/document_registry.json`.
    *   Authenticates with Google using credentials in `.claude/scripts/credentials.json` and `token.pickle`.
    *   Determines the target Google Drive folder:
        *   Uses `--folder "Name"` or `--folder-id "ID"` if provided via command line.
        *   Else, uses folder specified in `sync_preferences` within the registry.
        *   Else (if no preference saved and no CLI override), prompts the user interactively (if possible) for a folder.
    *   For each document:
        *   Performs **stale mapping checks**: Verifies local file existence and Google Doc accessibility. Prompts for resolution if issues found (e.g., unlink, recreate GDoc).
        *   Performs **hash and version comparison**: Checks if local file content (SHA256 hash) or Google Doc version has changed since last sync.
        *   Handles **conflicts**: If both local and remote have changed, prompts user to choose which version wins (Local, GDoc, or Skip).
        *   **Syncs content**: If a new GDoc is needed (or `--force-new` is used), it creates one. Otherwise, it updates the existing GDoc with local content (if local is chosen or no conflict).
        *   **Updates registry**: Saves all changes (new GDoc IDs, updated hashes, versions, timestamps, statuses) back to `.madio/document_registry.json`.
    *   Optionally cleans escaped markdown characters from content before pushing to Google Docs.

### ✨ Automatic Markdown Cleanup (Still applies)

The sync process automatically fixes common escaped markdown characters that can result from Google Docs exports:

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

#### Traditional Config Mode
1. Configure file mappings in `sync_config.json`
2. Create local AI system documents (or let Claude edit via MCP filesystem)
3. Run `/push-to-docs` to configure Google Drive folders (first time only)
4. Auto-create Google Docs and sync content to organized folders
5. Configuration automatically updates with new Google Doc IDs and folder settings
6. Claude Project automatically picks up changes
7. Continuous framework evolution with seamless document management

#### NEW: Directory Mode (Recommended)
1. Create `synced_docs/` directory in project root
2. Add any AI system documents to the directory (organize however you like)
3. Run `python sync_to_docs.py --directory synced_docs`
4. Script discovers all documents automatically and creates Google Docs
5. Document→Doc mappings saved in `.synced_docs_mapping.json`
6. Add more documents anytime - they'll be auto-discovered and synced
7. Claude Project automatically picks up changes
8. Zero-configuration continuous sync workflow

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
- Check permissions for local AI system documents
- **NEW**: Ensure Google Drive API is enabled in Google Cloud Console
- **NEW**: Verify folder permissions if using custom folders

### Folder Selection Issues
- **Problem**: Interactive folder prompt doesn't wait for input in Claude Code CLI
- **Solution**: Use `--folder` argument to specify folder name directly
- **Example**: `python3 sync_to_docs.py --directory synced_docs --folder "MADIO Docs"`
- **Automatic**: Folder is created if it doesn't exist
- **Default**: If no folder specified, documents go to root folder (My Drive)

### Performance
- Large AI system documents may take longer to sync
- Rate limiting applies to Google Docs API
- Consider batch operations for multiple documents

## Implementation

```bash
#!/bin/bash

echo "🚀 MADIO Push to Google Docs"
echo "============================"
echo ""

# Check if synced_docs directory exists
if [ ! -d "synced_docs" ]; then
    echo "❌ No synced_docs/ directory found"
    echo ""
    echo "💡 Next steps:"
    echo "   1. Run /generate-ai-system to create AI system documents"
    echo "   2. Or run /madio-import-docs to import existing documents"
    echo "   3. Both commands will create the synced_docs/ directory"
    echo ""
    exit 1
fi

# Check if directory has any .md files
MD_COUNT=$(find synced_docs -name "*.md" -type f | wc -l)
if [ "$MD_COUNT" -eq 0 ]; then
    echo "❌ No AI system documents found in synced_docs/"
    echo ""
    echo "💡 Next steps:"
    echo "   1. Add your .md files to synced_docs/"
    echo "   2. Or run /madio-import-docs to import documents"
    echo ""
    exit 1
fi

echo "📁 Found $MD_COUNT AI system documents in synced_docs/"
echo ""

# Check if credentials exist
if [ ! -f ".claude/scripts/credentials.json" ]; then
    echo "❌ Google credentials not found"
    echo ""
    echo "🔧 Setup required:"
    echo "   1. Run /madio-enable-sync to set up Google credentials"
    echo "   2. Then run /push-to-docs again"
    echo ""
    exit 1
fi

echo "📁 Google Drive Folder Selection"
echo "   Where should your Google Docs be created?"
echo ""
echo "   1. Root folder (My Drive) - Press Enter"
echo "   2. Organized folder (recommended) - Enter folder name"
echo ""

# Check if running in non-interactive environment
if [ ! -t 0 ] || [ ! -t 1 ]; then
    echo "⚠️  Non-interactive environment detected (Claude Code CLI)"
    echo "📂 Using root folder (My Drive)"
    echo ""
    echo "💡 Tip: For organized folders, use:"
    echo "   python .claude/scripts/sync_to_docs.py --directory synced_docs --folder \"MADIO Docs\""
    echo ""
    
    # Run sync to root folder
    cd .claude/scripts
    python3 sync_to_docs.py --directory ../../synced_docs
else
    # Interactive environment - prompt user
    read -p "Enter folder name or press Enter for root [recommended: \"MADIO Docs\"]: " FOLDER_NAME
    
    echo ""
    # Capture additional arguments like --force-new
    OTHER_ARGS=""
    for arg in "$@"
    do
        if [[ "$arg" == "--force-new" ]]; then
            OTHER_ARGS="$OTHER_ARGS $arg"
        fi
        # Add other passthrough args here if needed
    done
    
    cd .claude/scripts # Change directory once
    if [ -z "$FOLDER_NAME" ]; then
        echo "📂 Using root folder (My Drive)"
        # Pass --interactive-session and other args
        python3 sync_to_docs.py --directory ../../synced_docs --interactive-session $OTHER_ARGS
    else
        echo "📂 Using folder: \"$FOLDER_NAME\""
        # Pass --interactive-session, folder name, and other args
        python3 sync_to_docs.py --directory ../../synced_docs --folder "$FOLDER_NAME" --interactive-session $OTHER_ARGS
    fi
fi
```
