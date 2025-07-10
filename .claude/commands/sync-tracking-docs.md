# Sync Tracking Documents

Comprehensive audit and update of all project tracking documents to ensure consistency with current project state.

## Command Purpose

Synchronizes all TODO lists, roadmaps, AI context files, and tracking documents to reflect the actual current state of the project. This command addresses the common issue where tasks are completed but tracking documents are not updated, leading to inconsistencies.

## What Gets Audited & Updated

### 📋 Primary Tracking Documents
- `TODO.md` - Active items and recently completed sections
- `docs/ARCHITECTURAL_REFACTORING_ROADMAP.md` - Task completion status and progress tracking
- `AI_CONTEXT.md` - Current project phase and recent accomplishments
- `.madio` configuration file - Project metadata and timestamps

### 🔍 Secondary Tracking Files
- `GETTING-STARTED.md` - Setup status indicators
- `README.md` - Project status sections
- `SYNC_SETUP.md` - Implementation status references
- `CLAUDE.md` / `GEMINI.md` - Context file updates

### 📊 Progress Indicators
- Phase completion percentages
- Task completion counts
- Timeline updates
- Status badge updates

## Implementation

### Phase 1: Project State Analysis

```bash
#!/bin/bash

echo "🔍 Analyzing Current Project State"
echo "=================================="
echo ""

# Initialize tracking variables
ANALYSIS_START_TIME=$(date +%s)
CURRENT_DATE=$(date '+%Y-%m-%d')
PROJECT_ROOT=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_ROOT")

echo "📁 Project: $PROJECT_NAME"
echo "📅 Analysis Date: $CURRENT_DATE"
echo "📂 Location: $PROJECT_ROOT"
echo ""

# Create analysis directory
mkdir -p .tracking-sync
echo "$(date): Starting tracking document sync analysis" > .tracking-sync/sync.log

echo "🎯 Phase 1: Project State Analysis"
echo "-----------------------------------"
echo ""

# Check for key files existence
echo "📄 Checking tracking document availability:"
TRACKING_FILES=(
    "TODO.md"
    "docs/ARCHITECTURAL_REFACTORING_ROADMAP.md"  
    "AI_CONTEXT.md"
    ".madio"
    "GETTING-STARTED.md"
    "README.md"
    "SYNC_SETUP.md"
)

MISSING_FILES=0
for file in "${TRACKING_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file"
    else
        echo "   ❌ $file (missing)"
        ((MISSING_FILES++))
    fi
done

echo ""
echo "📊 Document Status: $((${#TRACKING_FILES[@]} - MISSING_FILES))/${#TRACKING_FILES[@]} files available"

if [ $MISSING_FILES -gt 0 ]; then
    echo "⚠️  Some tracking documents are missing. Sync will focus on available files."
fi

echo ""
```

### Phase 2: Scan for Completed Tasks

```bash
echo "🔍 Phase 2: Scanning for Completed Tasks"
echo "----------------------------------------"
echo ""

# Scan git history for recent completions
echo "📜 Analyzing recent git commits for completed work:"
RECENT_COMMITS=$(git log --oneline -10 --grep="feat\|fix\|docs\|complete" 2>/dev/null || echo "")

if [ -n "$RECENT_COMMITS" ]; then
    echo "$RECENT_COMMITS" | while read commit; do
        echo "   🔸 $commit"
    done
else
    echo "   ℹ️  No recent completion-related commits found"
fi

echo ""

# Scan for completion indicators in files
echo "🎯 Scanning for completion indicators:"

# Check for newly created files that indicate progress
NEW_FEATURES=()
if [ -f "SYNC_SETUP.md" ]; then
    NEW_FEATURES+=("Unified Setup Guide (SYNC_SETUP.md)")
fi

if grep -q "resolve_from_root" .claude/scripts/sync_to_docs.py 2>/dev/null; then
    NEW_FEATURES+=("Path Resolution Robustness (CFG-4)")
fi

if grep -q "handle_http_error" .claude/scripts/sync_to_docs.py 2>/dev/null; then
    NEW_FEATURES+=("Enhanced Error Handling")
fi

if [ ${#NEW_FEATURES[@]} -gt 0 ]; then
    echo "   🆕 Detected new features/improvements:"
    for feature in "${NEW_FEATURES[@]}"; do
        echo "      ✅ $feature"
    done
else
    echo "   ℹ️  No obvious new features detected in codebase"
fi

echo ""

# Check for outdated completion dates
echo "📅 Checking for outdated timestamps:"
if [ -f "TODO.md" ]; then
    LAST_TODO_UPDATE=$(stat -f "%Sm" -t "%Y-%m-%d" TODO.md 2>/dev/null || stat -c "%y" TODO.md 2>/dev/null | cut -d' ' -f1)
    echo "   📋 TODO.md last modified: $LAST_TODO_UPDATE"
fi

if [ -f "docs/ARCHITECTURAL_REFACTORING_ROADMAP.md" ]; then
    LAST_ROADMAP_UPDATE=$(stat -f "%Sm" -t "%Y-%m-%d" docs/ARCHITECTURAL_REFACTORING_ROADMAP.md 2>/dev/null || stat -c "%y" docs/ARCHITECTURAL_REFACTORING_ROADMAP.md 2>/dev/null | cut -d' ' -f1)
    echo "   🗺️  Roadmap last modified: $LAST_ROADMAP_UPDATE"
fi

echo ""
```

### Phase 3: Identify Inconsistencies

```bash
echo "🕵️ Phase 3: Identifying Inconsistencies"
echo "---------------------------------------"
echo ""

INCONSISTENCIES=0

# Check TODO.md vs actual state
if [ -f "TODO.md" ]; then
    echo "📋 TODO.md consistency check:"
    
    # Check if SYNC_SETUP.md exists but isn't marked complete in TODO
    if [ -f "SYNC_SETUP.md" ] && ! grep -q "DOC-3.*✅\|Unified Setup Guide.*✅" TODO.md; then
        echo "   ❌ SYNC_SETUP.md exists but DOC-3 not marked complete in TODO.md"
        ((INCONSISTENCIES++))
    fi
    
    # Check if path resolution is implemented but not marked complete
    if grep -q "resolve_from_root" .claude/scripts/sync_to_docs.py 2>/dev/null && ! grep -q "CFG-4.*✅\|Path Resolution.*✅" TODO.md; then
        echo "   ❌ Path resolution implemented but CFG-4 not marked complete in TODO.md"
        ((INCONSISTENCIES++))
    fi
    
    # Check if error handling is enhanced but not marked complete
    if grep -q "handle_http_error" .claude/scripts/sync_to_docs.py 2>/dev/null && ! grep -q "Error Handling.*✅" TODO.md; then
        echo "   ❌ Error handling enhanced but not marked complete in TODO.md"
        ((INCONSISTENCIES++))
    fi
    
    if [ $INCONSISTENCIES -eq 0 ]; then
        echo "   ✅ TODO.md appears consistent with project state"
    fi
else
    echo "   ⚠️  TODO.md not found, skipping consistency check"
fi

echo ""

# Check roadmap vs actual state
if [ -f "docs/ARCHITECTURAL_REFACTORING_ROADMAP.md" ]; then
    echo "🗺️  Roadmap consistency check:"
    
    ROADMAP_INCONSISTENCIES=0
    
    # Check for unchecked completed items
    if [ -f "SYNC_SETUP.md" ] && grep -q "\[ \].*DOC-3" docs/ARCHITECTURAL_REFACTORING_ROADMAP.md; then
        echo "   ❌ DOC-3 should be checked as complete in roadmap"
        ((ROADMAP_INCONSISTENCIES++))
    fi
    
    if grep -q "resolve_from_root" .claude/scripts/sync_to_docs.py 2>/dev/null && grep -q "\[ \].*CFG-4" docs/ARCHITECTURAL_REFACTORING_ROADMAP.md; then
        echo "   ❌ CFG-4 should be checked as complete in roadmap"
        ((ROADMAP_INCONSISTENCIES++))
    fi
    
    if [ $ROADMAP_INCONSISTENCIES -eq 0 ]; then
        echo "   ✅ Roadmap appears consistent with project state"
    else
        ((INCONSISTENCIES+=$ROADMAP_INCONSISTENCIES))
    fi
else
    echo "   ⚠️  Roadmap not found, skipping consistency check"
fi

echo ""
echo "📊 Total inconsistencies found: $INCONSISTENCIES"
echo ""
```

### Phase 4: Generate Update Recommendations

```bash
echo "💡 Phase 4: Update Recommendations"
echo "===================================="
echo ""

if [ $INCONSISTENCIES -eq 0 ]; then
    echo "🎉 All tracking documents appear to be consistent!"
    echo "   No updates needed at this time."
else
    echo "🔧 Recommended updates to sync tracking documents:"
    echo ""
    
    # Generate specific update commands/suggestions
    if [ -f "SYNC_SETUP.md" ] && ! grep -q "DOC-3.*✅" TODO.md; then
        echo "📋 TODO.md updates needed:"
        echo "   • Mark DOC-3 (Unified Setup Guide) as completed"
        echo "   • Add SYNC_SETUP.md to recent completions section"
        echo ""
    fi
    
    if grep -q "resolve_from_root" .claude/scripts/sync_to_docs.py 2>/dev/null && ! grep -q "CFG-4.*✅" TODO.md; then
        echo "📋 TODO.md updates needed:"
        echo "   • Mark CFG-4 (Path Resolution Robustness) as completed"
        echo "   • Add path resolution improvements to recent completions"
        echo ""
    fi
    
    if [ -f "docs/ARCHITECTURAL_REFACTORING_ROADMAP.md" ]; then
        echo "🗺️  Roadmap updates needed:"
        echo "   • Check completed tasks as [x] instead of [ ]"
        echo "   • Update progress tracking dashboard"
        echo "   • Update phase completion percentages"
        echo ""
    fi
    
    if [ -f "AI_CONTEXT.md" ]; then
        echo "🤖 AI_CONTEXT.md updates needed:"
        echo "   • Update current project phase"
        echo "   • Add recent accomplishments"
        echo "   • Update last modified timestamp"
        echo ""
    fi
fi
```

### Phase 5: Interactive Update Mode

```bash
echo "⚙️ Phase 5: Interactive Update Options"
echo "====================================="
echo ""

if [ $INCONSISTENCIES -gt 0 ]; then
    echo "🛠️  Update Options:"
    echo "   1. Generate detailed update instructions"
    echo "   2. Create update checklist for manual completion"
    echo "   3. Show specific file sections that need updating"
    echo "   4. Exit and update manually"
    echo ""
    
    read -p "Choose an option (1-4): " UPDATE_CHOICE
    
    case $UPDATE_CHOICE in
        1)
            echo ""
            echo "📝 Generating detailed update instructions..."
            echo ""
            
            # Create update instructions file
            cat > .tracking-sync/update-instructions.md << EOF
# Tracking Document Update Instructions

Generated: $(date)
Project: $PROJECT_NAME

## Files Requiring Updates

EOF
            
            if [ -f "SYNC_SETUP.md" ] && ! grep -q "DOC-3.*✅" TODO.md; then
                cat >> .tracking-sync/update-instructions.md << EOF
### TODO.md
- [ ] Mark DOC-3 as completed in recent completions section
- [ ] Add SYNC_SETUP.md creation to accomplishments list
- [ ] Update last modified date

EOF
            fi
            
            if [ -f "docs/ARCHITECTURAL_REFACTORING_ROADMAP.md" ]; then
                cat >> .tracking-sync/update-instructions.md << EOF
### ARCHITECTURAL_REFACTORING_ROADMAP.md  
- [ ] Change \`[ ]\` to \`[x]\` for completed tasks
- [ ] Update progress tracking dashboard percentages
- [ ] Add recent completions to tracking section

EOF
            fi
            
            echo "✅ Update instructions saved to: .tracking-sync/update-instructions.md"
            ;;
            
        2)
            echo ""
            echo "📋 Creating update checklist..."
            
            cat > .tracking-sync/update-checklist.txt << EOF
Tracking Document Sync Checklist - $(date)

TODO.md:
[ ] Mark completed tasks as done
[ ] Update recent completions section  
[ ] Verify all new features are documented

ARCHITECTURAL_REFACTORING_ROADMAP.md:
[ ] Check off completed tasks [x]
[ ] Update progress percentages
[ ] Update phase status indicators

AI_CONTEXT.md:
[ ] Update current project phase
[ ] Add recent accomplishments
[ ] Update modification timestamp

Additional:
[ ] Review other tracking documents for consistency
[ ] Commit tracking document updates
[ ] Verify all changes are accurate
EOF
            
            echo "✅ Update checklist saved to: .tracking-sync/update-checklist.txt"
            ;;
            
        3)
            echo ""
            echo "📍 Specific sections requiring updates:"
            echo ""
            
            if [ -f "TODO.md" ]; then
                echo "🔸 TODO.md - Recent Completions section (around line 75+)"
                echo "🔸 TODO.md - Active Items section for completed tasks"
            fi
            
            if [ -f "docs/ARCHITECTURAL_REFACTORING_ROADMAP.md" ]; then
                echo "🔸 Roadmap - Progress Tracking Dashboard (around line 784+)"
                echo "🔸 Roadmap - Individual task checkboxes throughout document"
            fi
            ;;
            
        4)
            echo "✅ Exiting for manual updates"
            ;;
            
        *)
            echo "Invalid option selected"
            ;;
    esac
else
    echo "🎉 No updates needed - all tracking documents are consistent!"
fi

echo ""
```

### Phase 6: Summary and Completion

```bash
echo "📊 Sync Analysis Summary"
echo "========================"
echo ""

ANALYSIS_END_TIME=$(date +%s)
ANALYSIS_DURATION=$((ANALYSIS_END_TIME - ANALYSIS_START_TIME))

echo "⏱️  Analysis Duration: $ANALYSIS_DURATION seconds"
echo "📁 Project: $PROJECT_NAME"
echo "📅 Analysis Date: $CURRENT_DATE"
echo "🔍 Files Checked: ${#TRACKING_FILES[@]}"
echo "❌ Inconsistencies Found: $INCONSISTENCIES"
echo ""

if [ $INCONSISTENCIES -eq 0 ]; then
    echo "✅ STATUS: All tracking documents are synchronized"
    echo "   Your project documentation is up to date!"
else
    echo "⚠️  STATUS: $INCONSISTENCIES inconsistencies require attention"
    echo "   Check the generated files in .tracking-sync/ for detailed guidance"
fi

echo ""
echo "📂 Generated Files:"
if [ -f ".tracking-sync/update-instructions.md" ]; then
    echo "   📝 .tracking-sync/update-instructions.md"
fi
if [ -f ".tracking-sync/update-checklist.txt" ]; then
    echo "   📋 .tracking-sync/update-checklist.txt" 
fi
echo "   📜 .tracking-sync/sync.log"

echo ""
echo "💡 Next Steps:"
if [ $INCONSISTENCIES -gt 0 ]; then
    echo "   1. Review generated update guidance"
    echo "   2. Update the identified tracking documents"
    echo "   3. Run /sync-tracking-docs again to verify"
    echo "   4. Commit the documentation updates"
else
    echo "   1. Continue with your development work"
    echo "   2. Run /sync-tracking-docs periodically to maintain consistency"
    echo "   3. Use this command after completing major features"
fi

echo ""
echo "🔄 Recommendation: Run this command after completing major tasks"
echo "   to keep all tracking documents synchronized."

# Log completion
echo "$(date): Tracking document sync analysis completed" >> .tracking-sync/sync.log
echo "Inconsistencies found: $INCONSISTENCIES" >> .tracking-sync/sync.log
echo "Analysis duration: $ANALYSIS_DURATION seconds" >> .tracking-sync/sync.log

echo ""
echo "📋 Tracking document sync analysis complete!"
```

## Usage Examples

```bash
# Regular sync check after completing work
/sync-tracking-docs

# Quick consistency verification
/sync-tracking-docs --quick

# Generate update guidance only
/sync-tracking-docs --guide-only
```

## Benefits

### 🎯 Consistency Maintenance
- Ensures all tracking documents reflect actual project state
- Prevents outdated TODO items and roadmap tasks
- Maintains accurate progress indicators

### 🕵️ Automated Detection
- Scans for completed features in codebase
- Identifies missing checkmarks in tracking documents
- Detects timestamp inconsistencies

### 🛠️ Guided Updates
- Provides specific update recommendations
- Generates checklists for manual completion
- Points to exact file sections needing updates

### 📊 Progress Accuracy
- Maintains accurate completion percentages
- Updates phase status indicators
- Keeps AI context files current

## Integration Notes

- **Run Frequency**: After completing major features or tasks
- **Automation**: Can be integrated into git pre-commit hooks
- **Scope**: Covers all project tracking and documentation files
- **Safety**: Read-only analysis with guided update recommendations

This command solves the exact problem you described - ensuring that completed work is properly reflected across all tracking documents in the project.