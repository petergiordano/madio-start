#!/bin/bash

echo "🔧 MADIO Import Debug Script"
echo "=========================="
echo ""

# Get current directory
PWD_DIR=$(pwd)
echo "Current directory: $PWD_DIR"
echo ""

# Check if we're in a MADIO project
if [ ! -d ".claude" ]; then
    echo "❌ Not in a MADIO project directory (no .claude folder)"
    exit 1
fi

echo "✅ MADIO project detected"
echo ""

# Test SOURCE_DIR (should default to current directory)
SOURCE_DIR="."
echo "Source directory: $SOURCE_DIR"
echo ""

# List existing .md files
echo "📁 Existing .md files in current directory:"
ls -la *.md 2>/dev/null || echo "   No .md files found"
echo ""

# Test the problematic patterns one by one
MADIO_PATTERNS=(
    "project_system_instructions.md"
    "orchestrator.md"
    "*character_voice*.md"
    "*content_operations*.md"
    "*methodology_framework*.md"
    "*rubrics_evaluation*.md"
    "*strategic_framework*.md"
    "*research_protocols*.md"
    "*implementation_roadmap*.md"
    "*document_reference_map*.md"
    "*visual_design*.md"
    "*visual_asset*.md"
    "*standard*.md"
)

echo "🔍 Testing pattern matching (this is where the timeout likely occurs):"
echo ""

TEMP_FILE="/tmp/madio_debug_$$.tmp"
> "$TEMP_FILE"

for pattern in "${MADIO_PATTERNS[@]}"; do
    echo "Testing pattern: $pattern"
    
    # Test with timeout to prevent hanging
    timeout 5s find "$SOURCE_DIR" -name "$pattern" -type f 2>/dev/null || echo "   ⚠️  Pattern timed out or failed"
    
    # Count matches
    MATCHES=$(find "$SOURCE_DIR" -name "$pattern" -type f 2>/dev/null | wc -l)
    echo "   Found: $MATCHES matches"
    echo ""
done

echo "🧹 Debug complete!"
rm -f "$TEMP_FILE"