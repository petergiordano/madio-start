# Sync Status - Google Docs Sync Health Check

View the current status of your Google Docs synchronization, including synced files, pending changes, and document URLs.

## Command Purpose

This command provides a comprehensive view of your Google Docs sync status, helping you understand:
- Which files are currently synced
- When files were last synced
- Which files have pending changes
- Google Doc URLs for each synced file
- Overall sync health and configuration

## Usage

```bash
# Check sync status for default synced_docs directory
/sync-status

# Check status for custom directory
/sync-status --directory my_docs

# Check traditional config sync status
/sync-status --config

# Show detailed information
/sync-status --verbose
```

## Implementation

### Phase 1: Environment Detection

```bash
#!/bin/bash

echo "📊 Google Docs Sync Status"
echo "=========================="
echo ""

# Initialize variables
PROJECT_ROOT=$(pwd)
SYNC_MODE=""
DIRECTORY_PATH="synced_docs"
CONFIG_PATH=".claude/scripts/sync_config.json"
MAPPING_FILE=".synced_docs_mapping.json"
VERBOSE=false

# Parse arguments
for arg in "$@"; do
    case $arg in
        --directory=*)
            DIRECTORY_PATH="${arg#*=}"
            SYNC_MODE="directory"
            ;;
        --config)
            SYNC_MODE="config"
            ;;
        --verbose)
            VERBOSE=true
            ;;
        *)
            ;;
    esac
done

# Auto-detect sync mode if not specified
if [ -z "$SYNC_MODE" ]; then
    if [ -f "$MAPPING_FILE" ] && [ -d "$DIRECTORY_PATH" ]; then
        SYNC_MODE="directory"
    elif [ -f "$CONFIG_PATH" ]; then
        SYNC_MODE="config"
    else
        echo "❌ No sync configuration found"
        echo ""
        echo "To set up sync, run:"
        echo "   • /madio-enable-sync - Complete Google Docs sync setup"
        echo "   • /generate-ai-system - Generate AI system with sync option"
        exit 1
    fi
fi

echo "🔍 Sync Mode: $SYNC_MODE"
echo "📁 Location: $PROJECT_ROOT"
echo ""
```

### Phase 2: Check Sync Prerequisites

```bash
echo "🔧 Checking Prerequisites"
echo "-------------------------"

# Check for credentials
if [ -f ".claude/scripts/credentials.json" ]; then
    echo "✅ Google credentials found"
    CREDS_SIZE=$(ls -lh .claude/scripts/credentials.json | awk '{print $5}')
    CREDS_PERMS=$(ls -l .claude/scripts/credentials.json | awk '{print $1}')
    if [ "$VERBOSE" = true ]; then
        echo "   Size: $CREDS_SIZE"
        echo "   Permissions: $CREDS_PERMS"
    fi
else
    echo "❌ Google credentials missing"
    echo "   Run: /madio-enable-sync to set up"
fi

# Check for authentication token
if [ -f ".claude/scripts/token.pickle" ]; then
    echo "✅ Authentication token present"
    TOKEN_AGE=$(find .claude/scripts/token.pickle -mtime +0 | wc -l)
    if [ "$TOKEN_AGE" -gt 0 ]; then
        TOKEN_DAYS=$(find .claude/scripts/token.pickle -mtime +0 -exec stat -f "%Sm" -t "%Y-%m-%d" {} \; 2>/dev/null || echo "unknown")
        echo "   Last auth: $TOKEN_DAYS"
    fi
else
    echo "⚠️  No authentication token"
    echo "   Will authenticate on next sync"
fi

# Check Python environment
if [ -d ".claude/scripts/venv" ]; then
    echo "✅ Python environment ready"
else
    echo "❌ Python environment missing"
    echo "   Run: cd .claude/scripts && ./setup.sh"
fi

echo ""
```

### Phase 3: Analyze Sync Configuration

```bash
echo "📋 Sync Configuration"
echo "--------------------"

if [ "$SYNC_MODE" = "directory" ]; then
    # Directory mode analysis
    echo "Mode: Directory-based sync"
    echo "Directory: $DIRECTORY_PATH"
    
    if [ ! -d "$DIRECTORY_PATH" ]; then
        echo "❌ Directory not found: $DIRECTORY_PATH"
        exit 1
    fi
    
    # Count AI system documents
    TOTAL_MD_FILES=$(find "$DIRECTORY_PATH" -name "*.md" -type f | wc -l)
    echo "Markdown files found: $TOTAL_MD_FILES"
    
    # Load mapping file
    if [ -f "$MAPPING_FILE" ]; then
        # Count mapped files
        MAPPED_COUNT=$(grep -c '": "' "$MAPPING_FILE" 2>/dev/null || echo "0")
        echo "Files with Google Doc IDs: $MAPPED_COUNT"
        
        # Check for unmapped files
        UNMAPPED_COUNT=$((TOTAL_MD_FILES - MAPPED_COUNT))
        if [ "$UNMAPPED_COUNT" -gt 0 ]; then
            echo "⚠️  Unmapped files: $UNMAPPED_COUNT (will create new docs on sync)"
        fi
    else
        echo "⚠️  No mapping file found"
        echo "   All files will create new Google Docs on first sync"
    fi
    
elif [ "$SYNC_MODE" = "config" ]; then
    # Config mode analysis
    echo "Mode: Configuration-based sync"
    echo "Config: $CONFIG_PATH"
    
    if [ -f "$CONFIG_PATH" ]; then
        # Count configured files
        CONFIG_COUNT=$(grep -c '": "' "$CONFIG_PATH" 2>/dev/null || echo "0")
        # Subtract non-file entries (like _google_drive_folder)
        CONFIG_COUNT=$((CONFIG_COUNT - $(grep -c '": {' "$CONFIG_PATH" 2>/dev/null || echo "0")))
        echo "Files configured: $CONFIG_COUNT"
        
        # Check for CREATE_NEW_DOCUMENT placeholders
        PLACEHOLDER_COUNT=$(grep -c 'CREATE_NEW_DOCUMENT' "$CONFIG_PATH" 2>/dev/null || echo "0")
        if [ "$PLACEHOLDER_COUNT" -gt 0 ]; then
            echo "⚠️  Pending doc creation: $PLACEHOLDER_COUNT files"
        fi
        
        # Check folder configuration
        if grep -q '"_google_drive_folder"' "$CONFIG_PATH"; then
            FOLDER_NAME=$(grep -A2 '"_google_drive_folder"' "$CONFIG_PATH" | grep '"name"' | cut -d'"' -f4)
            FOLDER_ID=$(grep -A2 '"_google_drive_folder"' "$CONFIG_PATH" | grep '"id"' | cut -d'"' -f4)
            if [ ! -z "$FOLDER_NAME" ]; then
                echo "Google Drive folder: $FOLDER_NAME"
                if [ ! -z "$FOLDER_ID" ]; then
                    echo "   ID: ${FOLDER_ID:0:15}..."
                fi
            fi
        fi
    else
        echo "❌ Config file not found: $CONFIG_PATH"
    fi
fi

echo ""
```

### Phase 4: File Status Analysis

```bash
echo "📄 File Sync Status"
echo "------------------"

# Function to check if file needs sync
check_file_needs_sync() {
    local file_path=$1
    local last_sync_time=$2
    
    if [ -z "$last_sync_time" ] || [ "$last_sync_time" = "never" ]; then
        echo "never"
        return
    fi
    
    # Get file modification time
    if [ -f "$file_path" ]; then
        FILE_MOD_TIME=$(stat -f "%m" "$file_path" 2>/dev/null || stat -c "%Y" "$file_path" 2>/dev/null)
        if [ "$FILE_MOD_TIME" -gt "$last_sync_time" ]; then
            echo "pending"
        else
            echo "synced"
        fi
    else
        echo "missing"
    fi
}

# Create sync status tracking
declare -A SYNC_STATUS
declare -A DOC_IDS
declare -A LAST_SYNC
NEEDS_SYNC_COUNT=0
SYNCED_COUNT=0
MISSING_COUNT=0

if [ "$SYNC_MODE" = "directory" ]; then
    # Analyze directory mode files
    if [ -f "$MAPPING_FILE" ]; then
        # Parse mapping file with Python for accuracy
        python3 -c "
import json
import os
from datetime import datetime

try:
    with open('$MAPPING_FILE', 'r') as f:
        mapping = json.load(f)
    
    # Get last sync time from metadata if available
    last_sync = mapping.get('_last_sync', {})
    
    for file_path, doc_id in mapping.items():
        if file_path.startswith('_'):
            continue
        
        # Get file status
        if os.path.exists(file_path):
            mod_time = os.path.getmtime(file_path)
            sync_time = last_sync.get(file_path, 0)
            
            if sync_time == 0:
                status = 'never'
            elif mod_time > sync_time:
                status = 'pending'
            else:
                status = 'synced'
                
            print(f'{file_path}|{doc_id}|{status}')
        else:
            print(f'{file_path}|{doc_id}|missing')
            
except Exception as e:
    print(f'ERROR: {e}')
" | while IFS='|' read -r file doc_id status; do
            if [ ! -z "$file" ] && [ "$file" != "ERROR:" ]; then
                SYNC_STATUS["$file"]="$status"
                DOC_IDS["$file"]="$doc_id"
                
                case "$status" in
                    "pending") ((NEEDS_SYNC_COUNT++)) ;;
                    "synced") ((SYNCED_COUNT++)) ;;
                    "missing") ((MISSING_COUNT++)) ;;
                esac
                
                if [ "$VERBOSE" = true ]; then
                    case "$status" in
                        "synced") echo "✅ $file" ;;
                        "pending") echo "⚠️  $file (modified)" ;;
                        "never") echo "🆕 $file (never synced)" ;;
                        "missing") echo "❌ $file (file missing)" ;;
                    esac
                fi
            fi
        done
    fi
    
    # Check for new files not in mapping
    find "$DIRECTORY_PATH" -name "*.md" -type f | while read -r file; do
        REL_PATH=$(echo "$file" | sed "s|^./||")
        if [ -z "${SYNC_STATUS[$REL_PATH]}" ]; then
            SYNC_STATUS["$REL_PATH"]="new"
            ((NEEDS_SYNC_COUNT++))
            if [ "$VERBOSE" = true ]; then
                echo "🆕 $REL_PATH (not mapped)"
            fi
        fi
    done
fi

# Summary statistics
echo ""
echo "📊 Summary:"
echo "   ✅ Synced: $SYNCED_COUNT files"
echo "   ⚠️  Needs sync: $NEEDS_SYNC_COUNT files"
echo "   ❌ Missing: $MISSING_COUNT files"

if [ "$NEEDS_SYNC_COUNT" -gt 0 ]; then
    echo ""
    echo "💡 To sync pending changes, run:"
    if [ "$SYNC_MODE" = "directory" ]; then
        echo "   python .claude/scripts/sync_to_docs.py --directory $DIRECTORY_PATH"
    else
        echo "   /push-to-docs"
    fi
fi

echo ""
```

### Phase 5: Google Doc URLs

```bash
echo "🔗 Google Doc URLs"
echo "-----------------"

if [ ${#DOC_IDS[@]} -eq 0 ] && [ "$SYNC_MODE" = "directory" ] && [ -f "$MAPPING_FILE" ]; then
    # Fallback: parse mapping file directly if array is empty
    echo "Loading document URLs..."
    grep -v "^{" "$MAPPING_FILE" | grep -v "^}" | grep '": "' | grep -v '": {' | while IFS='"' read -r _ file _ doc_id _; do
        if [ ! -z "$doc_id" ] && [ "$doc_id" != "CREATE_NEW_DOCUMENT" ]; then
            echo "📄 $file"
            echo "   https://docs.google.com/document/d/$doc_id/edit"
        fi
    done
else
    # Display URLs from parsed data
    for file in "${!DOC_IDS[@]}"; do
        doc_id="${DOC_IDS[$file]}"
        if [ ! -z "$doc_id" ] && [ "$doc_id" != "CREATE_NEW_DOCUMENT" ]; then
            echo "📄 $file"
            echo "   https://docs.google.com/document/d/$doc_id/edit"
        fi
    done
fi

# Count total URLs
URL_COUNT=$([ ${#DOC_IDS[@]} -gt 0 ] && echo ${#DOC_IDS[@]} || grep -c '": "' "$MAPPING_FILE" 2>/dev/null || echo "0")
if [ "$URL_COUNT" -eq 0 ]; then
    echo "ℹ️  No documents synced yet"
    echo "   Run sync command to create Google Docs"
fi

echo ""
```

### Phase 6: Health Check Summary

```bash
echo "🏥 Sync Health Check"
echo "-------------------"

HEALTH_SCORE=100
HEALTH_ISSUES=""

# Check prerequisites
if [ ! -f ".claude/scripts/credentials.json" ]; then
    HEALTH_SCORE=$((HEALTH_SCORE - 30))
    HEALTH_ISSUES="$HEALTH_ISSUES\n   ❌ Missing Google credentials"
fi

if [ ! -d ".claude/scripts/venv" ]; then
    HEALTH_SCORE=$((HEALTH_SCORE - 20))
    HEALTH_ISSUES="$HEALTH_ISSUES\n   ❌ Python environment not set up"
fi

# Check sync configuration
if [ "$SYNC_MODE" = "directory" ] && [ ! -d "$DIRECTORY_PATH" ]; then
    HEALTH_SCORE=$((HEALTH_SCORE - 20))
    HEALTH_ISSUES="$HEALTH_ISSUES\n   ❌ Sync directory missing"
elif [ "$SYNC_MODE" = "config" ] && [ ! -f "$CONFIG_PATH" ]; then
    HEALTH_SCORE=$((HEALTH_SCORE - 20))
    HEALTH_ISSUES="$HEALTH_ISSUES\n   ❌ Sync config missing"
fi

# Check for pending syncs
if [ "$NEEDS_SYNC_COUNT" -gt 5 ]; then
    HEALTH_SCORE=$((HEALTH_SCORE - 10))
    HEALTH_ISSUES="$HEALTH_ISSUES\n   ⚠️  Many files pending sync ($NEEDS_SYNC_COUNT)"
fi

# Check for missing files
if [ "$MISSING_COUNT" -gt 0 ]; then
    HEALTH_SCORE=$((HEALTH_SCORE - 15))
    HEALTH_ISSUES="$HEALTH_ISSUES\n   ⚠️  Missing local files ($MISSING_COUNT)"
fi

# Display health status
if [ "$HEALTH_SCORE" -ge 90 ]; then
    echo "🟢 Excellent ($HEALTH_SCORE/100)"
    echo "   Everything is working perfectly!"
elif [ "$HEALTH_SCORE" -ge 70 ]; then
    echo "🟡 Good ($HEALTH_SCORE/100)"
    echo "   Minor issues detected:"
    echo -e "$HEALTH_ISSUES"
elif [ "$HEALTH_SCORE" -ge 50 ]; then
    echo "🟠 Fair ($HEALTH_SCORE/100)"
    echo "   Several issues need attention:"
    echo -e "$HEALTH_ISSUES"
else
    echo "🔴 Poor ($HEALTH_SCORE/100)"
    echo "   Critical issues found:"
    echo -e "$HEALTH_ISSUES"
fi

echo ""

# Recommendations
if [ "$HEALTH_SCORE" -lt 100 ]; then
    echo "💡 Recommendations:"
    
    if [ ! -f ".claude/scripts/credentials.json" ]; then
        echo "   1. Run /madio-enable-sync to set up Google Docs sync"
    fi
    
    if [ ! -d ".claude/scripts/venv" ]; then
        echo "   2. Run: cd .claude/scripts && ./setup.sh"
    fi
    
    if [ "$NEEDS_SYNC_COUNT" -gt 0 ]; then
        echo "   3. Sync pending changes with the sync command above"
    fi
    
    if [ "$MISSING_COUNT" -gt 0 ]; then
        echo "   4. Check for deleted files or update mappings"
    fi
fi

echo ""

# Last sync information
LAST_SYNC_FILE=".claude/project-config/last-sync.log"
if [ -f "$LAST_SYNC_FILE" ]; then
    echo "📅 Last Sync Activity:"
    tail -n 5 "$LAST_SYNC_FILE" | sed 's/^/   /'
else
    echo "📅 No sync history found"
fi

echo ""
echo "✅ Sync status check complete!"
```

## Features

### Comprehensive Status Display
- Shows all synced files with their current status
- Identifies files needing sync (modified since last sync)
- Lists new files not yet synced
- Displays missing files that were previously synced

### Google Doc URL Management
- Shows clickable Google Doc URLs for all synced files
- Easy copy/paste for sharing or browser access
- Quick reference for Claude Project integration

### Health Scoring
- 0-100 health score based on configuration completeness
- Identifies specific issues affecting sync capability
- Provides actionable recommendations for improvements

### Multi-Mode Support
- Works with directory-based sync (recommended)
- Supports traditional config-based sync
- Auto-detects sync mode from project setup

## Integration Notes

- Works seamlessly with `/generate-ai-system` workflow
- Complements `/push-to-docs` command
- Provides visibility without performing actual sync
- Safe read-only operation for status checking

## Usage Examples

```bash
# Quick status check
/sync-status

# Detailed information
/sync-status --verbose

# Check custom directory
/sync-status --directory=my_custom_docs

# Traditional config mode
/sync-status --config
```

## Troubleshooting

If sync status shows issues:
1. Check health score and follow recommendations
2. Ensure Google credentials are set up (`/madio-enable-sync`)
3. Verify Python environment is ready
4. Run actual sync to resolve pending changes
5. Use `/madio-doctor` for comprehensive diagnostics