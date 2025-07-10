# MADIO Import Docs - Import Existing MADIO Documents

Import existing MADIO-compliant AI system documents into the framework with automatic context generation and Google Docs sync setup.

## Command Purpose

This command enables users who already have MADIO-formatted AI system documents to:
- Import them into the MADIO framework structure
- Generate appropriate context files (AI_CONTEXT.md)
- Set up Google Docs synchronization
- Maintain document hierarchy and relationships

Perfect for:
- Migrating existing MADIO projects
- Importing documents from other sources
- Setting up pre-written documentation
- Template development and testing

## Usage

```bash
# Import all AI system documents from current directory
/madio-import-docs

# Import from specific directory
/madio-import-docs --source ./my-ai-system-docs

# Import without moving files (copy instead)
/madio-import-docs --copy

# Skip sync setup (import only)
/madio-import-docs --no-sync
```

## Implementation

### Phase 1: Project Validation & Setup

```bash
#!/bin/bash

echo "📥 MADIO Document Import Tool"
echo "============================="
echo ""

# Initialize variables
PROJECT_ROOT=$(pwd)
SOURCE_DIR=${1:-$PROJECT_ROOT}
COPY_MODE=false
SKIP_SYNC=false
IMPORT_TIMESTAMP=$(date '+%Y%m%d_%H%M%S')
IMPORT_LOG=".madio_import_$IMPORT_TIMESTAMP.log"

# Parse arguments
for arg in "$@"; do
    case $arg in
        --source=*)
            SOURCE_DIR="${arg#*=}"
            ;;
        --copy)
            COPY_MODE=true
            ;;
        --no-sync)
            SKIP_SYNC=true
            ;;
        --help)
            echo "Usage: /madio-import-docs [options]"
            echo ""
            echo "Options:"
            echo "  --source=DIR   Directory containing AI system documents (default: current)"
            echo "  --copy         Copy files instead of moving them"
            echo "  --no-sync      Skip Google Docs sync setup"
            echo ""
            exit 0
            ;;
    esac
done

# Check if this is already a MADIO project
if [ -f ".madio-setup-complete" ]; then
    echo "✅ Existing MADIO project detected"
    echo ""
    read -p "Import will merge with existing project. Continue? (y/N): " CONTINUE
    if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
        echo "❌ Import cancelled"
        exit 1
    fi
else
    echo "🆕 New MADIO project - running initial setup..."
    # Run madio-setup first
    if [ -f ".claude/commands/madio-setup.md" ]; then
        /madio-setup --import-mode
        if [ $? -ne 0 ]; then
            echo "❌ Setup failed. Please run /madio-setup manually first."
            exit 1
        fi
    else
        echo "❌ MADIO setup command not found. Please run from project root."
        exit 1
    fi
fi
```

### Phase 2: Document Discovery & Analysis

```bash
echo ""
echo "🔍 Phase 1: Document Discovery"
echo "------------------------------"

# Create temporary file for discovered documents
TEMP_FILE_LIST=".madio_import_files_$IMPORT_TIMESTAMP.tmp"

# Discover MADIO documents
echo "Scanning for AI system documents in: $SOURCE_DIR"

# Smart AI system document detection - analyze content rather than filenames
echo "Using intelligent document detection..."

# Find all .md files in source directory (non-recursive to avoid issues)
echo "   Scanning $SOURCE_DIR for .md files..."
timeout 30s find "$SOURCE_DIR" -maxdepth 1 -name "*.md" -type f > "$TEMP_FILE_LIST" 2>/dev/null

if [ $? -eq 124 ]; then
    echo "❌ File discovery timed out. Large directory or permission issues?"
    echo "💡 Try using --source with a specific directory containing your MADIO files"
    exit 1
fi

# Filter out non-MADIO files
FILTERED_LIST=".madio_filtered_$IMPORT_TIMESTAMP.tmp"
> "$FILTERED_LIST"

while IFS= read -r file; do
    if [ -f "$file" ]; then
        BASENAME=$(basename "$file")
        
        # Skip system files
        if [[ "$BASENAME" =~ ^(README|GETTING-STARTED|TODO|SYNC_SETUP|AI_CONTEXT|CLAUDE|GEMINI|JULES)\.md$ ]]; then
            echo "   ⏭️  Skipping system file: $BASENAME"
            continue
        fi
        
        # Check if file contains AI system document markers
        if grep -q -E "(# .+ \(Tier [1-3]\)|## Authority Level|## Document Purpose|Tier [1-3] Document)" "$file" 2>/dev/null; then
            echo "   ✅ AI system document detected: $BASENAME"
            echo "$file" >> "$FILTERED_LIST"
        else
            echo "   📄 Regular markdown file: $BASENAME (checking content...)"
            # Check for other AI system document indicators
            if grep -q -E "(orchestrator|system instructions|methodology|framework|evaluation|strategic)" "$file" 2>/dev/null; then
                echo "   🔍 Potential AI system document: $BASENAME (including based on content)"
                echo "$file" >> "$FILTERED_LIST"
            else
                echo "   ⏭️  Skipping non-AI system file: $BASENAME"
            fi
        fi
    fi
done < "$TEMP_FILE_LIST"

# Use filtered list
cp "$FILTERED_LIST" "$TEMP_FILE_LIST"
rm -f "$FILTERED_LIST"

# Remove duplicates and sort
sort -u "$TEMP_FILE_LIST" -o "$TEMP_FILE_LIST"

# Count discovered files
FILE_COUNT=$(wc -l < "$TEMP_FILE_LIST")

if [ "$FILE_COUNT" -eq 0 ]; then
    echo "❌ No AI system documents found in $SOURCE_DIR"
    echo ""
    echo "AI system documents typically include:"
    echo "  • project_system_instructions.md"
    echo "  • orchestrator.md"
    echo "  • Various Tier 3 supporting documents"
    echo ""
    echo "Please ensure your documents follow AI system document naming conventions."
    exit 1
fi

echo "✅ Found $FILE_COUNT potential AI system documents:"
cat "$TEMP_FILE_LIST" | while read -r file; do
    echo "   • $(basename "$file")"
done | head -20

if [ "$FILE_COUNT" -gt 20 ]; then
    echo "   ... and $((FILE_COUNT - 20)) more"
fi

echo ""
echo "📊 Phase 2: Document Analysis"
echo "-----------------------------"

# Run Python analysis script
echo "Analyzing document structure and hierarchy..."

python3 .claude/scripts/analyze_madio_import.py \
    --file-list "$TEMP_FILE_LIST" \
    --output ".madio_import_analysis_$IMPORT_TIMESTAMP.json" \
    --log "$IMPORT_LOG"

if [ $? -ne 0 ]; then
    echo "❌ Document analysis failed. Check $IMPORT_LOG for details."
    exit 1
fi

# Display analysis summary
python3 -c "
import json
with open('.madio_import_analysis_$IMPORT_TIMESTAMP.json', 'r') as f:
    analysis = json.load(f)
    
print(f\"\\n✅ Analysis Complete:\")
print(f\"   • Tier 1 documents: {analysis['summary']['tier1_count']}\")
print(f\"   • Tier 2 documents: {analysis['summary']['tier2_count']}\")
print(f\"   • Tier 3 documents: {analysis['summary']['tier3_count']}\")
print(f\"   • Project complexity: {analysis['summary']['complexity']}\")
print(f\"   • Template compliance: {analysis['summary']['compliance']}%\")
"
```

### Phase 3: Document Organization

```bash
echo ""
echo "📁 Phase 3: Document Organization"
echo "---------------------------------"

# Create synced_docs directory if it doesn't exist
if [ ! -d "synced_docs" ]; then
    mkdir -p synced_docs
    echo "✅ Created synced_docs/ directory"
else
    echo "✅ Using existing synced_docs/ directory"
fi

# Process files based on mode
if [ "$COPY_MODE" = true ]; then
    echo "📋 Copying files to synced_docs/ (preserving originals)..."
    ACTION="Copied"
else
    echo "📋 Moving files to synced_docs/..."
    ACTION="Moved"
    echo ""
    echo "⚠️  WARNING: This will move your original files!"
    read -p "Continue with move operation? (y/N): " CONFIRM_MOVE
    if [[ ! "$CONFIRM_MOVE" =~ ^[Yy]$ ]]; then
        COPY_MODE=true
        ACTION="Copied"
        echo "Switching to copy mode for safety."
    fi
fi

# Process each file
PROCESSED_COUNT=0
cat "$TEMP_FILE_LIST" | while read -r file; do
    if [ -f "$file" ]; then
        BASENAME=$(basename "$file")
        
        # Skip if already in synced_docs
        if [[ "$file" == *"synced_docs"* ]]; then
            echo "   ⏭️  Skipping $BASENAME (already in synced_docs)"
            continue
        fi
        
        # Check if file already exists in destination
        if [ -f "synced_docs/$BASENAME" ]; then
            echo "   ⚠️  $BASENAME already exists in synced_docs"
            read -p "   Overwrite? (y/N): " OVERWRITE
            if [[ ! "$OVERWRITE" =~ ^[Yy]$ ]]; then
                echo "   ⏭️  Skipped $BASENAME"
                continue
            fi
        fi
        
        # Copy or move file
        if [ "$COPY_MODE" = true ]; then
            cp "$file" "synced_docs/"
        else
            mv "$file" "synced_docs/"
        fi
        
        ((PROCESSED_COUNT++))
        echo "   ✅ $ACTION $BASENAME"
    fi
done

echo ""
echo "✅ Organized $PROCESSED_COUNT files in synced_docs/"
```

### Phase 4: Context Generation

```bash
echo ""
echo "📝 Phase 4: Context Generation"
echo "------------------------------"

# Generate AI_CONTEXT.md
echo "Generating AI_CONTEXT.md from imported documents..."

python3 .claude/scripts/generate_madio_context.py \
    --analysis ".madio_import_analysis_$IMPORT_TIMESTAMP.json" \
    --import-mode \
    --timestamp "$IMPORT_TIMESTAMP"

if [ $? -eq 0 ]; then
    echo "✅ Generated AI_CONTEXT.md"
else
    echo "⚠️  Failed to generate AI_CONTEXT.md (non-critical)"
fi

# Update TODO.md if it exists
if [ -f "TODO.md" ]; then
    echo ""
    echo "📋 Updating TODO.md..."
    cat >> TODO.md << EOF

## Import Log - $IMPORT_TIMESTAMP

### Documents Imported
- Total files: $FILE_COUNT
- Source: $SOURCE_DIR
- Mode: $ACTION to synced_docs/

### Next Steps
- [ ] Review imported documents for completeness
- [ ] Customize project-specific content
- [ ] Set up Google Docs sync with /push-to-docs
- [ ] Validate document cross-references

EOF
    echo "✅ Updated TODO.md with import information"
fi

# Create import summary
cat > ".madio_import_summary_$IMPORT_TIMESTAMP.md" << EOF
# AI System Document Import Summary

**Import Date**: $(date '+%Y-%m-%d %H:%M:%S')
**Source Directory**: $SOURCE_DIR
**Documents Imported**: $FILE_COUNT
**Operation Mode**: $ACTION

## Document Analysis

$(python3 -c "
import json
with open('.madio_import_analysis_$IMPORT_TIMESTAMP.json', 'r') as f:
    analysis = json.load(f)
    
print('### Tier 1 - Authority AI System Documents')
for doc in analysis['documents']['tier1']:
    print(f\"- {doc['filename']}\")
    
print('\\n### Tier 2 - Orchestration AI System Documents')
for doc in analysis['documents']['tier2']:
    print(f\"- {doc['filename']}\")
    
print('\\n### Tier 3 - Supporting AI System Documents')
for doc in analysis['documents']['tier3']:
    print(f\"- {doc['filename']}\")
")

## Import Configuration

- Files organized in: synced_docs/
- Context generated: AI_CONTEXT.md
- Ready for sync: $([ "$SKIP_SYNC" = true ] && echo "No (--no-sync flag)" || echo "Yes")

## Next Steps

1. Review imported documents
2. Run \`/push-to-docs\` to sync with Google Docs
3. Customize content as needed

EOF

echo "✅ Created import summary: .madio_import_summary_$IMPORT_TIMESTAMP.md"
```

### Phase 5: Google Docs Sync Setup

```bash
if [ "$SKIP_SYNC" = false ]; then
    echo ""
    echo "☁️  Phase 5: Google Docs Sync Setup"
    echo "-----------------------------------"
    
    # Check if sync is already configured
    if [ -f ".claude/scripts/credentials.json" ]; then
        echo "✅ Google credentials already configured"
        
        echo ""
        echo "🔄 Ready to sync imported AI system documents to Google Docs"
        read -p "Start sync now? (Y/n): " START_SYNC
        
        if [[ ! "$START_SYNC" =~ ^[Nn]$ ]]; then
            echo ""
            echo "🚀 Starting Google Docs sync..."
            
            # Create custom folder for imported AI system documents
            IMPORT_FOLDER="AI System Import - $(date '+%Y-%m-%d')"
            
            python3 .claude/scripts/sync_to_docs.py \
                --directory synced_docs \
                --import-folder "$IMPORT_FOLDER"
            
            if [ $? -eq 0 ]; then
                echo ""
                echo "✅ AI system documents synced to Google Drive!"
                echo "   Folder: $IMPORT_FOLDER"
            else
                echo ""
                echo "⚠️  Sync encountered issues. You can retry with:"
                echo "   /push-to-docs --directory synced_docs"
            fi
        else
            echo ""
            echo "📋 To sync later, run:"
            echo "   /push-to-docs --directory synced_docs"
        fi
    else
        echo "⚠️  Google Docs sync not configured"
        echo ""
        echo "To set up sync:"
        echo "1. Run: /madio-enable-sync"
        echo "2. Follow Google Cloud setup instructions"
        echo "3. Then run: /push-to-docs --directory synced_docs"
    fi
else
    echo ""
    echo "⏭️  Skipping sync setup (--no-sync flag)"
    echo ""
    echo "To sync later:"
    echo "1. Ensure Google credentials are set up (/madio-enable-sync)"
    echo "2. Run: /push-to-docs --directory synced_docs"
fi
```

### Phase 6: Cleanup and Summary

```bash
echo ""
echo "🧹 Phase 6: Cleanup"
echo "-------------------"

# Archive analysis files
ARCHIVE_DIR=".madio/import_history"
mkdir -p "$ARCHIVE_DIR"

mv ".madio_import_analysis_$IMPORT_TIMESTAMP.json" "$ARCHIVE_DIR/" 2>/dev/null
mv "$TEMP_FILE_LIST" "$ARCHIVE_DIR/" 2>/dev/null
mv "$IMPORT_LOG" "$ARCHIVE_DIR/" 2>/dev/null

echo "✅ Archived import artifacts to $ARCHIVE_DIR/"

echo ""
echo "🎉 AI System Document Import Complete!"
echo "=================================="
echo ""
echo "📊 Summary:"
echo "   • AI system documents imported: $FILE_COUNT"
echo "   • Location: synced_docs/"
echo "   • Context: AI_CONTEXT.md generated"
echo "   • Import summary: .madio_import_summary_$IMPORT_TIMESTAMP.md"
echo ""

if [ "$SKIP_SYNC" = false ] && [ -f ".claude/scripts/credentials.json" ]; then
    echo "☁️  Google Docs Status:"
    echo "   • Ready for sync"
    echo "   • Run: /push-to-docs --directory synced_docs"
    echo ""
fi

echo "📋 Recommended Next Steps:"
echo "1. Review import summary"
echo "2. Check AI_CONTEXT.md for accuracy"
echo "3. Validate document relationships"
echo "4. Sync to Google Docs when ready"
echo ""
echo "💡 Tips:"
echo "   • Use /sync-status to monitor sync health"
echo "   • Edit files locally, changes sync automatically"
echo "   • Run /madio-doctor if you encounter issues"
```

## Error Handling

### Document Discovery Issues
- No MADIO documents found
- Invalid document structure
- Missing required documents (Tier 1/2)

### Analysis Failures
- Malformed markdown
- Encoding issues
- Invalid hierarchy

### Organization Problems
- File conflicts
- Permission issues
- Disk space

### Sync Setup Errors
- Missing credentials
- Network issues
- API quotas

## Usage Examples

```bash
# Import from current directory
/madio-import-docs

# Import from specific location
/madio-import-docs --source ~/Desktop/my-madio-project

# Safe import (copy files)
/madio-import-docs --copy

# Import without immediate sync
/madio-import-docs --no-sync

# Import from archive
/madio-import-docs --source ./backup/madio-docs-20240115 --copy
```

## Integration Notes

- Works with existing MADIO projects
- Preserves document relationships
- Generates comprehensive context
- Seamless sync integration
- Maintains audit trail

## Related Commands

- `/madio-setup` - Initial project setup
- `/push-to-docs` - Sync to Google Docs
- `/sync-status` - Check sync health
- `/madio-doctor` - Troubleshooting