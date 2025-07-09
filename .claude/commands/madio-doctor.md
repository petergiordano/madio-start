# MADIO Doctor

Comprehensive diagnostic tool for MADIO projects - identify issues, validate setup, and provide actionable solutions.

## Command Purpose

MADIO Doctor performs health checks on your MADIO project, identifying common issues and providing specific solutions. It validates environment setup, project structure, document integrity, and deployment readiness.

## Diagnostic Categories

1. **Environment Validation** - Check required tools and permissions
2. **Project Structure** - Verify MADIO project setup and files
3. **Document Integrity** - Validate MADIO documents and hierarchy
4. **Template System** - Check template availability and updates
5. **Deployment Readiness** - Assess platform deployment status
6. **Performance Issues** - Identify common bottlenecks

## Implementation

### Phase 1: Environment Diagnostics

```bash
echo "🏥 MADIO Doctor - Comprehensive Project Health Check"
echo "=================================================="
echo ""

# Initialize counters
ISSUES_FOUND=0
WARNINGS_FOUND=0
RECOMMENDATIONS=0

# Check system requirements
echo "🔧 Environment Validation"
echo "-------------------------"

# Git check
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version)
    echo "   ✅ Git: $GIT_VERSION"
    
    # Check if in git repo
    if git rev-parse --git-dir &> /dev/null; then
        echo "   ✅ Git repository initialized"
        
        # Check for remotes
        ORIGIN=$(git remote get-url origin 2>/dev/null || echo "none")
        TEMPLATE=$(git remote get-url template 2>/dev/null || echo "none")
        
        if [[ "$ORIGIN" != "none" ]]; then
            echo "   ✅ Origin remote: $ORIGIN"
        else
            echo "   ❌ No origin remote configured"
            ((ISSUES_FOUND++))
        fi
        
        if [[ "$TEMPLATE" != "none" ]]; then
            echo "   ✅ Template remote: $TEMPLATE"
        else
            echo "   ⚠️  No template remote (run /madio-setup to add)"
            ((WARNINGS_FOUND++))
        fi
    else
        echo "   ❌ Not in a git repository"
        ((ISSUES_FOUND++))
    fi
else
    echo "   ❌ Git not installed or not in PATH"
    ((ISSUES_FOUND++))
fi

# VS Code check
if command -v code &> /dev/null; then
    echo "   ✅ VS Code CLI available"
else
    echo "   ⚠️  VS Code CLI not available (optional)"
    ((WARNINGS_FOUND++))
fi

# Claude Code CLI check
if [ -d ".claude" ]; then
    echo "   ✅ Claude Code CLI structure present"
else
    echo "   ⚠️  No .claude directory (Claude Code CLI may not be set up)"
    ((WARNINGS_FOUND++))
fi
```

### Phase 2: Project Structure Diagnostics

```bash
echo ""
echo "📁 Project Structure Validation"
echo "-------------------------------"

# Check for setup completion
if [ -f ".madio-setup-complete" ]; then
    echo "   ✅ MADIO setup completed"
    SETUP_DATE=$(cat .madio-setup-complete 2>/dev/null || echo "unknown")
    echo "      Setup date: $SETUP_DATE"
else
    echo "   ❌ MADIO setup not completed (run /madio-setup)"
    ((ISSUES_FOUND++))
fi

# Check for AI_CONTEXT.md
if [ -f "AI_CONTEXT.md" ]; then
    echo "   ✅ AI_CONTEXT.md bridge file present"
    
    # Check if it's been customized
    if grep -q "\[PROJECT_NAME\]" "AI_CONTEXT.md"; then
        echo "   ⚠️  AI_CONTEXT.md contains uncustomized placeholders"
        ((WARNINGS_FOUND++))
    else
        echo "   ✅ AI_CONTEXT.md appears customized"
    fi
else
    echo "   ❌ AI_CONTEXT.md missing (critical for AI collaboration)"
    ((ISSUES_FOUND++))
fi

# Check for core context files
for file in "CLAUDE.md" "GEMINI.md" "madio_core_templates.md"; do
    if [ -f "$file" ]; then
        echo "   ✅ $file present"
    else
        echo "   ⚠️  $file missing (run /madio-setup to restore)"
        ((WARNINGS_FOUND++))
    fi
done

# Check for .madio configuration
if [ -f ".madio" ]; then
    echo "   ✅ .madio configuration file present"
else
    echo "   ⚠️  .madio configuration missing (optional)"
    ((WARNINGS_FOUND++))
fi

# Check for workspace file
WORKSPACE_FILE="$(basename "$PWD").code-workspace"
if [ -f "$WORKSPACE_FILE" ]; then
    echo "   ✅ VS Code workspace file: $WORKSPACE_FILE"
else
    echo "   ℹ️  No VS Code workspace file (not required but recommended)"
    ((RECOMMENDATIONS++))
fi
```

### Phase 3: MADIO Document Validation

```bash
echo ""
echo "📄 MADIO Document Integrity"
echo "---------------------------"

# Check for generated MADIO documents
MADIO_DOCS=(
    "project_system_instructions.md"
    "orchestrator.md"
)

TIER3_DOCS=$(ls *_authority.md *_operations.md *_framework.md *_evaluation.md *_protocols.md *_standards.md *_generation.md *_roadmap.md *_reference_map.md 2>/dev/null || true)

# Check core documents
echo "   Core Documents (Always Required):"
for doc in "${MADIO_DOCS[@]}"; do
    if [ -f "$doc" ]; then
        echo "   ✅ $doc"
        
        # Check for placeholders
        PLACEHOLDER_COUNT=$(grep -c "\[.*\]" "$doc" 2>/dev/null | grep -v "^\[x\]" || echo "0")
        if [ "$PLACEHOLDER_COUNT" -gt 0 ]; then
            echo "      ⚠️  Contains $PLACEHOLDER_COUNT uncustomized placeholders"
            ((WARNINGS_FOUND++))
        fi
    else
        echo "   ❌ $doc missing (run /generate-ai-system)"
        ((ISSUES_FOUND++))
    fi
done

# Check Tier 3 documents
if [ ! -z "$TIER3_DOCS" ]; then
    echo ""
    echo "   Tier 3 Supporting Documents:"
    for doc in $TIER3_DOCS; do
        echo "   ✅ $doc"
        
        # Check for placeholders
        PLACEHOLDER_COUNT=$(grep -c "\[.*\]" "$doc" 2>/dev/null | grep -v "^\[x\]" || echo "0")
        if [ "$PLACEHOLDER_COUNT" -gt 0 ]; then
            echo "      ⚠️  Contains $PLACEHOLDER_COUNT uncustomized placeholders"
            ((WARNINGS_FOUND++))
        fi
    done
else
    echo ""
    echo "   ℹ️  No Tier 3 documents found (may be a simple system)"
fi

# Check document hierarchy
if [ -f "project_system_instructions.md" ] && [ -f "orchestrator.md" ]; then
    echo ""
    echo "   Document Hierarchy Validation:"
    
    # Check if orchestrator references project_system_instructions
    if grep -q "project_system_instructions" "orchestrator.md"; then
        echo "   ✅ Orchestrator properly references system instructions"
    else
        echo "   ⚠️  Orchestrator may not reference system instructions"
        ((WARNINGS_FOUND++))
    fi
    
    # Check if system instructions lists subordinate documents
    if grep -q "orchestrator" "project_system_instructions.md"; then
        echo "   ✅ System instructions lists subordinate documents"
    else
        echo "   ⚠️  System instructions may not list subordinate documents"
        ((WARNINGS_FOUND++))
    fi
fi
```

### Phase 4: Template System Health

```bash
echo ""
echo "📚 Template System Status"
echo "-------------------------"

# Check template library status
if [ -d "_template_library" ]; then
    echo "   ℹ️  Template library still present"
    TEMPLATE_COUNT=$(find "_template_library" -name "*.md" | wc -l)
    echo "      Contains $TEMPLATE_COUNT templates"
    echo "      💡 Consider running /generate-ai-system to clean up"
    ((RECOMMENDATIONS++))
else
    echo "   ✅ Template library cleaned up (good practice)"
fi

# Check if scaffolding directory still exists
if [ -d "_project_scaffolding" ]; then
    echo "   ⚠️  Scaffolding directory still present"
    echo "      This suggests /madio-setup was not completed"
    ((WARNINGS_FOUND++))
else
    echo "   ✅ Scaffolding directory properly cleaned up"
fi

# Check template remote status
if git remote get-url template &>/dev/null; then
    echo "   ✅ Template remote configured for updates"
    
    # Check if template updates are available
    git fetch template --quiet 2>/dev/null || true
    if git rev-list HEAD..template/main --count &>/dev/null; then
        UPDATE_COUNT=$(git rev-list HEAD..template/main --count 2>/dev/null || echo "0")
        if [ "$UPDATE_COUNT" -gt 0 ]; then
            echo "   📢 $UPDATE_COUNT template updates available!"
            echo "      Run: git pull template main"
            ((RECOMMENDATIONS++))
        else
            echo "   ✅ Template is up to date"
        fi
    fi
else
    echo "   ⚠️  No template remote (run /madio-setup to add)"
    ((WARNINGS_FOUND++))
fi
```

### Phase 5: Deployment Readiness Assessment

```bash
echo ""
echo "🚀 Deployment Readiness"
echo "----------------------"

# Check platform configuration
if [ -f "project_system_instructions.md" ]; then
    # Check which platforms are selected
    OPENAI_SELECTED=$(grep -c "\[x\] OpenAI CustomGPT" "project_system_instructions.md" 2>/dev/null || echo "0")
    GEMINI_SELECTED=$(grep -c "\[x\] Google Gemini Gem" "project_system_instructions.md" 2>/dev/null || echo "0")
    CLAUDE_SELECTED=$(grep -c "\[x\] Claude Project" "project_system_instructions.md" 2>/dev/null || echo "0")
    MULTI_SELECTED=$(grep -c "\[x\] Multi-platform deployment" "project_system_instructions.md" 2>/dev/null || echo "0")
    
    if [ "$OPENAI_SELECTED" -gt 0 ]; then
        echo "   🎯 OpenAI CustomGPT deployment configured"
    fi
    if [ "$GEMINI_SELECTED" -gt 0 ]; then
        echo "   🎯 Google Gemini Gem deployment configured"
    fi
    if [ "$CLAUDE_SELECTED" -gt 0 ]; then
        echo "   🎯 Claude Project deployment configured"
    fi
    if [ "$MULTI_SELECTED" -gt 0 ]; then
        echo "   🎯 Multi-platform deployment configured"
    fi
    
    if [ "$OPENAI_SELECTED" -eq 0 ] && [ "$GEMINI_SELECTED" -eq 0 ] && [ "$CLAUDE_SELECTED" -eq 0 ] && [ "$MULTI_SELECTED" -eq 0 ]; then
        echo "   ⚠️  No deployment platform selected"
        ((WARNINGS_FOUND++))
    fi
fi

# Check for remaining placeholders across all files
echo ""
echo "   Placeholder Scan:"
TOTAL_PLACEHOLDERS=$(grep -h "\[.*\]" *.md 2>/dev/null | grep -v "^\[x\]" | wc -l || echo "0")
if [ "$TOTAL_PLACEHOLDERS" -gt 0 ]; then
    echo "   ⚠️  $TOTAL_PLACEHOLDERS uncustomized placeholders found"
    echo "      Run: grep -n '\[.*\]' *.md | grep -v '^\[x\]' to see them"
    ((WARNINGS_FOUND++))
else
    echo "   ✅ No uncustomized placeholders found"
fi

# Check file sizes (detect empty or minimal files)
echo ""
echo "   Document Completeness:"
for file in *.md; do
    if [ -f "$file" ]; then
        FILE_SIZE=$(wc -c < "$file" 2>/dev/null || echo "0")
        if [ "$FILE_SIZE" -lt 500 ]; then
            echo "   ⚠️  $file appears small ($FILE_SIZE bytes) - may need content"
            ((WARNINGS_FOUND++))
        fi
    fi
done
```

### Phase 6: Performance and Best Practices

```bash
echo ""
echo "⚡ Performance & Best Practices"
echo "------------------------------"

# Check git status
if git status --porcelain | grep -q .; then
    UNCOMMITTED_FILES=$(git status --porcelain | wc -l)
    echo "   ⚠️  $UNCOMMITTED_FILES uncommitted changes"
    echo "      Consider committing your progress"
    ((WARNINGS_FOUND++))
else
    echo "   ✅ Working directory clean"
fi

# Check for large files
echo ""
echo "   File Size Analysis:"
LARGE_FILES=$(find . -name "*.md" -size +100k 2>/dev/null || true)
if [ ! -z "$LARGE_FILES" ]; then
    echo "   ℹ️  Large files detected (>100KB):"
    echo "$LARGE_FILES" | sed 's/^/      /'
    echo "      Consider splitting large documents"
    ((RECOMMENDATIONS++))
else
    echo "   ✅ All documents are reasonable size"
fi

# Check for backup files
BACKUP_FILES=$(find . -name "*.bak" -o -name "*.tmp" 2>/dev/null || true)
if [ ! -z "$BACKUP_FILES" ]; then
    echo "   🧹 Cleanup opportunities:"
    echo "$BACKUP_FILES" | sed 's/^/      /'
    echo "      Run: find . -name '*.bak' -delete"
    ((RECOMMENDATIONS++))
fi
```

### Phase 7: Health Summary and Recommendations

```bash
echo ""
echo "📊 MADIO Health Summary"
echo "======================="

# Overall health score
TOTAL_CHECKS=$((ISSUES_FOUND + WARNINGS_FOUND + RECOMMENDATIONS))
if [ "$ISSUES_FOUND" -eq 0 ] && [ "$WARNINGS_FOUND" -eq 0 ]; then
    echo "🎉 EXCELLENT HEALTH! Your MADIO project is in top condition."
    HEALTH_SCORE="A+"
elif [ "$ISSUES_FOUND" -eq 0 ] && [ "$WARNINGS_FOUND" -lt 3 ]; then
    echo "✅ GOOD HEALTH! Minor improvements available."
    HEALTH_SCORE="A"
elif [ "$ISSUES_FOUND" -lt 2 ] && [ "$WARNINGS_FOUND" -lt 5 ]; then
    echo "⚠️  FAIR HEALTH. Some issues need attention."
    HEALTH_SCORE="B"
else
    echo "🚨 NEEDS ATTENTION! Multiple issues detected."
    HEALTH_SCORE="C"
fi

echo ""
echo "Health Score: $HEALTH_SCORE"
echo "Critical Issues: $ISSUES_FOUND"
echo "Warnings: $WARNINGS_FOUND"
echo "Recommendations: $RECOMMENDATIONS"

# Priority actions
echo ""
echo "🎯 Priority Actions"
echo "------------------"

if [ "$ISSUES_FOUND" -gt 0 ]; then
    echo "🚨 CRITICAL (Fix First):"
    if [ ! -f ".madio-setup-complete" ]; then
        echo "   • Run /madio-setup to complete MADIO initialization"
    fi
    if [ ! -f "AI_CONTEXT.md" ]; then
        echo "   • Generate AI_CONTEXT.md bridge file (essential for AI collaboration)"
    fi
    if [ ! -f "project_system_instructions.md" ]; then
        echo "   • Run /generate-ai-system to create core MADIO documents"
    fi
    echo ""
fi

if [ "$WARNINGS_FOUND" -gt 0 ]; then
    echo "⚠️  IMPORTANT (Address Soon):"
    if grep -q "\[.*\]" *.md 2>/dev/null; then
        echo "   • Replace remaining placeholders in MADIO documents"
    fi
    if [ ! -d "_template_library" ] && ! git remote get-url template &>/dev/null; then
        echo "   • Add template remote for framework updates"
    fi
    echo ""
fi

if [ "$RECOMMENDATIONS" -gt 0 ]; then
    echo "💡 RECOMMENDED (When Convenient):"
    if git status --porcelain | grep -q .; then
        echo "   • Commit your current progress"
    fi
    if [ -d "_template_library" ]; then
        echo "   • Clean up template library after document generation"
    fi
    echo "   • Review MADIO best practices in madio_core_templates.md"
    echo ""
fi

# Quick fixes
echo "🔧 Quick Fixes"
echo "--------------"
echo "One-line solutions for common issues:"
echo ""
echo "Setup not complete:"
echo "   /madio-setup"
echo ""
echo "No AI system generated:"
echo "   /generate-ai-system \"[describe your AI system]\""
echo ""
echo "Find remaining placeholders:"
echo "   grep -n '\[.*\]' *.md | grep -v '^\[x\]'"
echo ""
echo "Add template remote:"
echo "   git remote add template https://github.com/petergiordano/madio-start.git"
echo ""
echo "Check for updates:"
echo "   git fetch template && git log HEAD..template/main --oneline"
echo ""
echo "Clean up backup files:"
echo "   find . -name '*.bak' -delete"

echo ""
echo "🏥 MADIO Doctor diagnosis complete!"
echo ""
echo "💡 Pro tip: Run /madio-doctor regularly to maintain project health"
echo "📚 Need help? Check madio_core_templates.md for detailed guidance"
```

## Error Handling

### Safe File Operations
- Use proper error checking for file existence
- Handle permission errors gracefully
- Provide clear error messages with solutions

### Git Safety
- Check if in git repository before git operations
- Handle missing remotes appropriately
- Validate git command availability

### Robust Scanning
- Handle files with special characters
- Graceful degradation if tools unavailable
- Comprehensive but safe file system scanning

## Integration Notes

- Can be run at any stage of MADIO development
- Provides actionable next steps for every issue
- Integrates with existing MADIO commands
- Supports continuous project health monitoring

## Usage Examples

```bash
# Regular health check
/madio-doctor

# After making changes
/madio-doctor

# Before deployment
/madio-doctor
```