#!/bin/bash

# MADIO Google Docs Sync Setup Script
# This script helps set up the Google Docs synchronization capability

echo "🚀 Setting up MADIO Google Docs Sync..."

# Check if we're in a MADIO project (look for .claude directory)
if [ ! -d ".claude" ]; then
    echo "❌ Please run this script from your MADIO project root directory"
    echo "   (should contain .claude/ directory)"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".claude/scripts/venv" ]; then
    echo "📦 Creating Python virtual environment..."
    cd .claude/scripts
    python3 -m venv venv
    cd ../..
fi

# Activate virtual environment and install dependencies
echo "📥 Installing Python dependencies..."
source .claude/scripts/venv/bin/activate
pip install -r .claude/scripts/requirements.txt

echo "✅ Dependencies installed!"
echo ""

# Offer sync workflow choice
echo "🔗 Google Docs Sync Workflow Setup"
echo ""
echo "Choose your preferred sync workflow:"
echo "1. 🆕 Flexible Directory Sync (Recommended) - Zero configuration"
echo "2. 📝 Traditional Config Sync - Manual file configuration"
echo ""
read -p "Choose workflow [1-2]: " WORKFLOW_CHOICE

case $WORKFLOW_CHOICE in
    1)
        echo ""
        echo "🆕 Setting up Flexible Directory Sync..."
        
        # Create synced_docs directory if it doesn't exist
        if [ ! -d "synced_docs" ]; then
            mkdir -p synced_docs
            echo "   ✅ Created synced_docs/ directory"
        else
            echo "   ✅ synced_docs/ directory already exists"
        fi
        
        # Create example file if directory is empty
        if [ ! "$(ls -A synced_docs)" ]; then
            cat > synced_docs/example.md << 'EOF'
# Example Document

This is an example markdown file in your synced_docs/ directory.

## How Flexible Sync Works

1. Add any `.md` files to this directory (including subdirectories)
2. Run: `python .claude/scripts/sync_to_docs.py --directory synced_docs`
3. Google Docs are automatically created for new files
4. File→Doc ID mappings saved in `.synced_docs_mapping.json`

You can delete this file once you add your own documents.
EOF
            echo "   ✅ Created example.md in synced_docs/"
        fi
        
        SYNC_MODE="flexible"
        ;;
    2)
        echo ""
        echo "📝 Setting up Traditional Config Sync..."
        
        # Create sync_config.json if it doesn't exist
        if [ ! -f ".claude/scripts/sync_config.json" ]; then
            echo "   ✅ sync_config.json already configured"
        else
            echo "   ⚠️  sync_config.json already exists - keeping existing configuration"
        fi
        
        SYNC_MODE="traditional"
        ;;
    *)
        echo "   Invalid choice. Defaulting to Flexible Directory Sync..."
        SYNC_MODE="flexible"
        ;;
esac

echo ""
echo "📋 Google Cloud Setup Required:"
echo "1. Go to Google Cloud Console: https://console.cloud.google.com/"
echo "2. Create a new project or select existing"
echo "3. Enable BOTH APIs:"
echo "   • Google Docs API (for document content sync)"
echo "   • Google Drive API (for document creation and folder management)"
echo "4. Create OAuth2 credentials (Desktop application type)"
echo "5. Download the credentials.json file"
echo "6. Move credentials.json to: .claude/scripts/credentials.json"
echo ""

if [ "$SYNC_MODE" = "flexible" ]; then
    echo "🆕 Next Steps (Flexible Sync):"
    echo "1. After getting credentials, add .md files to synced_docs/"
    echo "2. Run: python .claude/scripts/sync_to_docs.py --directory synced_docs"
    echo "3. First run will:"
    echo "   • Create Google Docs for all files"
    echo "   • Set up Google Drive folder organization (interactive)"
    echo "   • Save file→doc mappings in .synced_docs_mapping.json"
    echo "4. Future runs automatically sync changes to existing docs"
else
    echo "📝 Next Steps (Traditional Sync):"
    echo "1. Edit .claude/scripts/sync_config.json with your file paths and doc IDs"
    echo "2. Use CREATE_NEW_DOCUMENT for new files (auto-creation)"
    echo "3. Run: python .claude/scripts/sync_to_docs.py --config .claude/scripts/sync_config.json"
fi

echo ""
echo "📖 For detailed help: see .claude/commands/push-to-docs.md"
echo "🔧 For troubleshooting: run /madio-doctor"
