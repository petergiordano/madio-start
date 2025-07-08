#!/bin/bash

# MADIO Google Docs Sync Setup Script
# This script helps set up the Google Docs synchronization capability

echo "🚀 Setting up MADIO Google Docs Sync..."

# Check if we're in the right directory
if [ ! -f "sync_config.json" ]; then
    echo "❌ Please run this script from your MADIO project root directory"
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
echo "📋 Next steps:"
echo "1. Go to Google Cloud Console: https://console.cloud.google.com/"
echo "2. Create a new project or select existing"
echo "3. Enable the Google Docs API"
echo "4. Create OAuth2 credentials (Desktop application type)"
echo "5. Download the credentials.json file"
echo "6. Move credentials.json to: .claude/scripts/credentials.json"
echo "7. Edit sync_config.json with your Google Doc IDs"
echo "8. Run: /push-to-docs"
echo ""
echo "📖 See .claude/commands/push-to-docs.md for detailed instructions"
