# MADIO Enable Google Docs Sync

**OPTIONAL**: Set up Google Docs synchronization for advanced Claude Project integration.

## Command Purpose

This optional command enables Google Docs sync for users who want automatic synchronization between local MADIO documents and Google Docs. This allows Claude Projects to automatically refresh when local files change.

**⚠️ IMPORTANT: This is completely optional. Most MADIO users don't need this feature.**

## When You Might Want This

- You're using Claude Projects as your primary AI platform
- You want automatic document updates in Claude Project knowledge
- You're collaborating with business users who prefer Google Docs
- You're building AI systems that evolve frequently

## When You DON'T Need This

- You're only using OpenAI CustomGPT or Gemini Gems
- You prefer manual document uploads
- You want to keep things simple
- You don't use Google Workspace

## Implementation

### Phase 1: Prerequisites Check

```bash
echo "🔗 MADIO Google Docs Sync Setup (OPTIONAL)"
echo "==========================================="
echo ""
echo "⚠️ IMPORTANT: This feature is completely OPTIONAL"
echo "   Most MADIO users don't need Google Docs sync"
echo "   Only continue if you specifically need automatic"
echo "   document sync for Claude Projects"
echo ""

read -p "Do you want to enable Google Docs sync? (y/N): " ENABLE_SYNC
if [[ ! "$ENABLE_SYNC" =~ ^[Yy]$ ]]; then
    echo "✅ Skipping Google Docs sync setup"
    echo "   Your MADIO project works perfectly without it!"
    exit 0
fi

# Check if setup already exists
if [ -f ".claude/scripts/credentials.json" ]; then
    echo "✅ Google Docs sync already configured"
    echo "   Run /push-to-docs to sync documents"
    exit 0
fi

# Verify Python installation
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required for Google Docs sync"
    echo "   Install Python 3 and run this command again"
    echo "   Or skip sync setup entirely - MADIO works fine without it"
    exit 1
fi

echo "✅ Prerequisites check passed"
```

### Phase 2: Google Cloud Setup Guide

```bash
echo ""
echo "📋 Google Cloud Setup Required"
echo "------------------------------"
echo ""
echo "You'll need to set up Google Cloud credentials:"
echo ""
echo "1. Go to: https://console.cloud.google.com/"
echo "2. Create a new project or select existing"
echo "3. Enable Google Docs API"
echo "4. Create OAuth2 credentials (Desktop application)"
echo "5. Download credentials.json"
echo ""
echo "Detailed instructions: https://developers.google.com/docs/api/quickstart/python"
echo ""

read -p "Have you completed Google Cloud setup? (y/N): " CLOUD_SETUP
if [[ ! "$CLOUD_SETUP" =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔄 No problem! Complete the setup when ready:"
    echo "   1. Follow the Google Cloud setup above"
    echo "   2. Run /madio-enable-sync again"
    echo ""
    echo "💡 Remember: Google Docs sync is optional"
    echo "   Your MADIO project works great without it!"
    exit 0
fi
```

### Phase 3: Credentials Installation

```bash
echo ""
echo "📁 Installing Credentials"
echo "-------------------------"

# Create scripts directory if needed
mkdir -p .claude/scripts

echo "Please provide the path to your downloaded credentials.json file:"
read -p "Credentials file path: " CREDS_PATH

if [ ! -f "$CREDS_PATH" ]; then
    echo "❌ File not found: $CREDS_PATH"
    echo "   Please check the path and try again"
    exit 1
fi

# Copy credentials
cp "$CREDS_PATH" .claude/scripts/credentials.json
echo "✅ Credentials installed to .claude/scripts/credentials.json"

# Secure the credentials file
chmod 600 .claude/scripts/credentials.json
echo "✅ Credentials secured (600 permissions)"
```

### Phase 4: Python Dependencies

```bash
echo ""
echo "🐍 Installing Python Dependencies"
echo "---------------------------------"

cd .claude/scripts

# Create virtual environment if not exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✅ Created Python virtual environment"
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -q google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
echo "✅ Installed Google API dependencies"

cd - > /dev/null
```

### Phase 5: Sync Configuration

```bash
echo ""
echo "📋 Document Sync Configuration"
echo "------------------------------"
echo ""
echo "Which documents do you want to sync to Google Docs?"
echo ""

# Show available MADIO documents
echo "Available MADIO documents:"
for file in *.md; do
    if [ -f "$file" ] && [[ ! "$file" =~ ^(README|CLAUDE|GEMINI|madio_core_templates|AI_CONTEXT)\.md$ ]]; then
        echo "   • $file"
    fi
done

echo ""
echo "For each document you want to sync:"
echo "1. Create a new Google Doc"
echo "2. Copy the document ID from the URL"
echo "3. Enter it when prompted below"
echo ""

# Create sync configuration
cat > .claude/scripts/sync_config.json << EOF
{
EOF

FIRST_ENTRY=true
for file in *.md; do
    if [ -f "$file" ] && [[ ! "$file" =~ ^(README|CLAUDE|GEMINI|madio_core_templates|AI_CONTEXT)\.md$ ]]; then
        echo ""
        read -p "Google Doc ID for $file (press Enter to skip): " DOC_ID
        if [ ! -z "$DOC_ID" ]; then
            if [ "$FIRST_ENTRY" = true ]; then
                FIRST_ENTRY=false
            else
                echo "," >> .claude/scripts/sync_config.json
            fi
            echo "  \"../../$file\": \"$DOC_ID\"" >> .claude/scripts/sync_config.json
        fi
    fi
done

cat >> .claude/scripts/sync_config.json << EOF

}
EOF

echo ""
echo "✅ Sync configuration saved to .claude/scripts/sync_config.json"
```

### Phase 6: First Sync Test

```bash
echo ""
echo "🧪 Testing Sync Setup"
echo "---------------------"

# Test authentication
echo "Testing Google authentication..."
cd .claude/scripts
source venv/bin/activate

python3 -c "
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
import os

SCOPES = ['https://www.googleapis.com/auth/documents']

if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
else:
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)

print('✅ Authentication successful')
"

if [ $? -eq 0 ]; then
    echo "✅ Google authentication successful"
else
    echo "❌ Authentication failed"
    echo "   Check your credentials.json file"
    exit 1
fi

cd - > /dev/null

# Test sync if configuration exists
if [ -s ".claude/scripts/sync_config.json" ]; then
    echo ""
    echo "Testing document sync..."
    /push-to-docs
    
    if [ $? -eq 0 ]; then
        echo "✅ Document sync successful"
    else
        echo "⚠️ Sync test had issues"
        echo "   Check document IDs in sync_config.json"
    fi
fi
```

### Phase 7: Setup Completion

```bash
echo ""
echo "🎉 Google Docs Sync Setup Complete!"
echo "===================================="
echo ""
echo "✅ What was configured:"
echo "   • Google Cloud credentials installed"
echo "   • Python environment with required packages"
echo "   • Document sync mapping configured"
echo "   • Authentication tested and working"
echo ""
echo "🔗 Available Commands:"
echo "   • /push-to-docs - Sync all configured documents"
echo "   • /push-to-docs --file filename.md doc-id - Sync specific file"
echo ""
echo "📋 Next Steps:"
echo "1. Edit your MADIO documents locally"
echo "2. Run /push-to-docs to sync to Google Docs"
echo "3. Your Claude Project will automatically see updates"
echo ""
echo "💡 Pro Tips:"
echo "   • Only sync documents you actively edit"
echo "   • Run /madio-doctor to check sync health"
echo "   • You can disable sync anytime by removing .claude/scripts/"
echo ""
echo "🔄 Development Workflow:"
echo "   Local Edit → /push-to-docs → Claude Project Auto-Updates"
echo ""
echo "Remember: This sync is completely optional!"
echo "MADIO works perfectly without Google Docs integration."
```

## Error Handling

### Google Cloud Issues
- Verify credentials.json validity
- Check API enablement status
- Handle authentication failures gracefully

### Python Environment
- Check Python 3 availability
- Handle virtual environment creation failures
- Provide clear dependency installation errors

### Configuration Validation
- Validate Google Doc IDs
- Check file permissions
- Ensure sync mapping is correct

## Integration Notes

- Only runs when explicitly requested
- Doesn't interfere with core MADIO functionality
- Can be completely removed without affecting MADIO
- Works alongside existing /push-to-docs command

## Removal Instructions

To completely remove Google Docs sync:
```bash
rm -rf .claude/scripts/
```

Your MADIO project will continue working perfectly without sync.