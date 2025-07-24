# Push to Google Docs Command

Sync local AI system documents to Google Docs for Claude Project integration.

## Primary Usage (Recommended)

### Sync all AI system documents
```bash
# Default sync (uses "MADIO Docs" folder)
/push-to-docs

# Sync to specific folder
/push-to-docs "My Project Docs"

# Use environment variable
export DESTINATION_GOOGLE_DRIVE_FOLDER="Team Shared Docs"
/push-to-docs

# Use nested folder paths
/push-to-docs "@AI Agent Projects/My New Project"

# Use Google Drive folder ID directly
/push-to-docs --folder-id=1ABC123def456
```

**What this does:**
1. Scans `synced_docs/` directory for AI system documents
2. Uses specified folder, last used folder, or root folder as default
3. Creates folder automatically if it doesn't exist
4. Syncs all documents to Google Docs
5. Updates document mappings automatically
6. Saves folder preference for future runs

**Folder Selection Behavior:**
- **Interactive terminals**: Prompts for folder name (suggests last used)
- **Non-interactive (Claude Code CLI)**: Uses argument → env var → last used → root folder
- **Special value**: Use "root" or "ROOT" to sync to My Drive root
- **Preference**: Last used folder saved to `.claude/.madio_drive_folder`

## Advanced Usage (Direct Script Access)

### Sync with specific folder (non-interactive)
```bash
cd .claude/scripts
python3 sync_to_docs.py --directory synced_docs --folder "MADIO Docs"
```

### Sync to root folder (non-interactive)
```bash
cd .claude/scripts
python3 sync_to_docs.py --directory synced_docs
```

### Traditional config mode
```bash
cd .claude/scripts
python3 sync_to_docs.py --config sync_config.json
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

### 3a. Configure sync mapping (traditional mode)
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

### 3b. NEW: Set up directory sync (flexible mode)
Create a `synced_docs/` directory in your project root and add AI system documents:
```bash
mkdir synced_docs
echo "# My Document" > synced_docs/example.md
```

**No configuration needed!** The script automatically:
- Discovers all AI system documents in the directory
- Creates Google Docs for new AI system documents
- Saves document→doc mappings in `.synced_docs_mapping.json`
- Organizes documents in Google Drive folders (with prompts)

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

### Traditional Config Mode
1. Reads configuration from `sync_config.json`
2. **NEW**: Configures Google Drive folder organization (interactive prompts)
3. Reads local AI system documents from configured paths
4. **NEW**: Auto-creates Google Docs for `CREATE_NEW_DOCUMENT` placeholders
5. **NEW**: Places documents in specified Google Drive folders
6. **NEW**: Automatically cleans escaped markdown characters from Google Docs exports
7. Completely replaces Google Doc content
8. Auto-updates config file with new Google Doc IDs and folder settings
9. Preserves document ID for Claude Project
10. All Google Docs auto-update in Claude Project knowledge

### NEW: Directory Mode
1. **NEW**: Scans specified directory for all AI system documents (recursive)
2. **NEW**: Loads existing document→doc mappings from `.synced_docs_mapping.json`
3. **NEW**: Auto-creates Google Docs for new AI system documents found
4. **NEW**: Configures Google Drive folder organization (interactive prompts)
5. **NEW**: Places documents in specified Google Drive folders
6. **NEW**: Automatically cleans escaped markdown characters
7. Completely replaces Google Doc content with local document content
8. **NEW**: Updates `.synced_docs_mapping.json` with new document IDs
9. Preserves document IDs for Claude Project integration
10. All Google Docs auto-update in Claude Project knowledge

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

# Function to read last used folder from preference file
get_last_folder() {
    local pref_file=".claude/.madio_drive_folder"
    if [ -f "$pref_file" ]; then
        cat "$pref_file"
    else
        echo ""
    fi
}

# Function to save folder preference
save_folder_preference() {
    local folder="$1"
    local pref_file=".claude/.madio_drive_folder"
    echo "$folder" > "$pref_file"
}

# Check for --folder-id argument
FOLDER_ID=""
FOLDER_ARG=""
for arg in "$@"; do
    case $arg in
        --folder-id=*)
            FOLDER_ID="${arg#*=}"
            shift
            ;;
        *)
            FOLDER_ARG="$arg"
            ;;
    esac
done

# Check if running in non-interactive environment
if [ ! -t 0 ] || [ ! -t 1 ]; then
    echo "⚠️  Non-interactive environment detected (Claude Code CLI)"
    
    if [ -n "$FOLDER_ID" ]; then
        echo "📂 Using folder ID: ${FOLDER_ID:0:15}..."
        cd .claude/scripts
        python3 sync_to_docs.py --directory ../../synced_docs --folder-id "$FOLDER_ID"
    else
        # Check priority: argument → env var → last used → root
        LAST_FOLDER=$(get_last_folder)
        FOLDER_NAME="$FOLDER_ARG"
        
        if [ -z "$FOLDER_NAME" ]; then
            FOLDER_NAME="$DESTINATION_GOOGLE_DRIVE_FOLDER"
        fi
        
        if [ -z "$FOLDER_NAME" ] && [ -n "$LAST_FOLDER" ]; then
            FOLDER_NAME="$LAST_FOLDER"
        fi
        
        if [ -n "$FOLDER_NAME" ]; then
            echo "📂 Using folder: \"$FOLDER_NAME\""
            
            # Save preference if this was explicitly chosen
            if [ -n "$FOLDER_ARG" ] || [ -n "$DESTINATION_GOOGLE_DRIVE_FOLDER" ]; then
                save_folder_preference "$FOLDER_NAME"
            fi
            
            cd .claude/scripts
            python3 sync_to_docs.py --directory ../../synced_docs --folder "$FOLDER_NAME"
        else
            echo "📂 Using root folder (My Drive)"
            cd .claude/scripts
            python3 sync_to_docs.py --directory ../../synced_docs
        fi
        
        echo ""
        echo "💡 Tip: To use a different folder:"
        echo "   • Pass as argument: /push-to-docs \"My Folder\""
        echo "   • Use folder ID: /push-to-docs --folder-id=1ABC123def456"
        echo "   • Set environment variable: export DESTINATION_GOOGLE_DRIVE_FOLDER=\"My Folder\""
        echo ""
    fi
else
    # Interactive environment - prompt user
    if [ -n "$FOLDER_ID" ]; then
        echo "📂 Using folder ID: ${FOLDER_ID:0:15}..."
        cd .claude/scripts
        python3 sync_to_docs.py --directory ../../synced_docs --folder-id "$FOLDER_ID"
    else
        # Get last used folder and prepare prompt
        LAST_FOLDER=$(get_last_folder)
        
        # Determine default suggestion priority: argument → env var → last used
        DEFAULT_FOLDER="$FOLDER_ARG"
        if [ -z "$DEFAULT_FOLDER" ]; then
            DEFAULT_FOLDER="$DESTINATION_GOOGLE_DRIVE_FOLDER"
        fi
        if [ -z "$DEFAULT_FOLDER" ]; then
            DEFAULT_FOLDER="$LAST_FOLDER"
        fi
        
        # Display interactive prompt
        echo "📁 Google Drive Folder Selection"
        echo "Enter folder name for your Google Docs:"
        echo "- Press Enter for root folder (My Drive)"
        echo "- Enter a name like \"Project Docs\" for a specific folder"
        echo "- Use paths like \"Projects/MADIO/Docs\" for nested folders"
        echo ""
        
        if [ -n "$LAST_FOLDER" ]; then
            echo "Last used: $LAST_FOLDER"
        fi
        
        if [ -n "$DEFAULT_FOLDER" ]; then
            read -p "Your choice [$DEFAULT_FOLDER]: " FOLDER_NAME
            # Use default if empty
            FOLDER_NAME="${FOLDER_NAME:-$DEFAULT_FOLDER}"
        else
            read -p "Your choice: " FOLDER_NAME
        fi
        
        echo ""
        
        # Handle the user's choice
        if [ -z "$FOLDER_NAME" ] || [ "$FOLDER_NAME" = "root" ] || [ "$FOLDER_NAME" = "ROOT" ]; then
            echo "📂 Using root folder (My Drive)"
            # Save empty preference for root folder
            save_folder_preference ""
            cd .claude/scripts
            python3 sync_to_docs.py --directory ../../synced_docs
        else
            echo "📂 Using folder: \"$FOLDER_NAME\""
            # Save folder preference
            save_folder_preference "$FOLDER_NAME"
            cd .claude/scripts
            python3 sync_to_docs.py --directory ../../synced_docs --folder "$FOLDER_NAME"
        fi
    fi
fi
```
