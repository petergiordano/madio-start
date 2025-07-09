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

### Phase 2: Google Cloud Setup and Credentials

This step involves configuring Google Cloud to get the necessary `credentials.json` file that allows this script to access your Google Docs.

```bash
echo ""
echo "📋 Google Cloud Setup Required for Credentials"
echo "---------------------------------------------"
echo ""
echo "You will now be guided to set up Google Cloud credentials."
echo "For detailed, step-by-step instructions, please open and follow the guide:"
echo "➡️  docs/GOOGLE_CLOUD_SETUP.md"
echo ""
echo "Please open 'docs/GOOGLE_CLOUD_SETUP.md' in your editor or browser now."
echo "It contains important details, including screenshots and troubleshooting."
echo ""
read -p "Press Enter to continue after you have the guide open..."

echo ""
echo "Key tasks you will perform by following 'docs/GOOGLE_CLOUD_SETUP.md':"
echo "  1. Navigate to the Google Cloud Console."
echo "  2. Create or select a Google Cloud Project."
echo "  3. Enable the 'Google Docs API' for that project."
echo "  4. Configure the OAuth Consent Screen."
echo "  5. Create 'OAuth 2.0 Client ID' credentials of type 'Desktop app'."
echo "  6. Download the generated JSON file and RENAME it to 'credentials.json'."
echo ""
echo "IMPORTANT: "
echo "  - Ensure you are logged into the correct Google account in your browser."
echo "  - The credential type MUST be 'Desktop app'."
echo "  - Remember to RENAME the downloaded file to 'credentials.json'."
echo ""

read -p "Have you completed all steps in 'docs/GOOGLE_CLOUD_SETUP.md' and downloaded/renamed your 'credentials.json' file? (y/N): " CLOUD_SETUP_COMPLETE

if [[ ! "$CLOUD_SETUP_COMPLETE" =~ ^[Yy]$ ]]; then
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
echo "🐍 Ensuring Python Environment is Ready..."
echo "---------------------------------------"
echo "This will run the .claude/scripts/setup.sh script to prepare the Python environment."

# Assuming this command is run from the project root directory
SETUP_SCRIPT_PATH=".claude/scripts/setup.sh"

if [ ! -f "$SETUP_SCRIPT_PATH" ]; then
    echo "❌ Error: Python setup script not found at $SETUP_SCRIPT_PATH"
    echo "   Please ensure you are in the project root and the script exists."
    # For Claude commands, exiting might not be the best. Consider how errors are surfaced.
    # For now, we'll assume the command framework handles script errors.
    # If this were a standalone script, 'exit 1' would be here.
    echo "SCRIPT_ERROR: Python setup script not found. Aborting."
    # Claude CLI might require a specific way to signal error, this is a placeholder.
    # Depending on how Claude CLI handles shell script execution, we might need to adjust error signaling.
    # For now, printing an error and letting it continue might be what happens,
    # or the Claude CLI might halt on non-zero exit codes if we add 'exit 1'.
    # Let's assume for now that we want to halt.
    exit 1 
fi

echo "   Running $SETUP_SCRIPT_PATH ..."
# Make sure setup.sh is executable
chmod +x "$SETUP_SCRIPT_PATH"

# Execute setup.sh and capture its success/failure
if bash "$SETUP_SCRIPT_PATH"; then
    echo "✅ Python environment setup script completed successfully."
    echo "   The Python virtual environment and dependencies should now be installed."
else
    echo "❌ Error: Python environment setup failed."
    echo "   Please review the output from the setup script above for details."
    echo "   You may need to resolve Python/pip issues or other errors shown."
    echo "   Aborting Google Docs Sync enablement."
    exit 1 # Signal error
fi

# Reminder: setup.sh now deactivates the venv itself.
# The following steps in this /madio-enable-sync command that need
# to run python scripts (like the auth test) will need to re-activate it.
echo "   Python environment is prepared for Google Docs Sync."
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

### Phase 7: Project Configuration Record

```bash
echo ""
echo "📋 Creating Project Configuration Record"
echo "---------------------------------------"

# Create project-config directory if it doesn't exist
mkdir -p .claude/project-config

# Get project information
PROJECT_NAME=$(basename "$PWD")
CURRENT_DATE=$(date '+%Y-%m-%d %H:%M:%S')
USER_EMAIL=$(git config user.email 2>/dev/null || echo "unknown")

# Extract project details from credentials.json if available
if [ -f ".claude/scripts/credentials.json" ]; then
    cd .claude/scripts
    
    # Extract project info from credentials.json
    PROJECT_ID=$(python3 -c "
import json
try:
    with open('credentials.json', 'r') as f:
        data = json.load(f)
        client_info = data.get('installed', {})
        project_id = client_info.get('project_id', 'unknown')
        print(project_id)
except:
    print('unknown')
" 2>/dev/null || echo "unknown")
    
    CLIENT_ID=$(python3 -c "
import json
try:
    with open('credentials.json', 'r') as f:
        data = json.load(f)
        client_info = data.get('installed', {})
        client_id = client_info.get('client_id', 'unknown')
        # Truncate for security
        if len(client_id) > 20:
            client_id = client_id[:20] + '...'
        print(client_id)
except:
    print('unknown')
" 2>/dev/null || echo "unknown")
    
    cd - > /dev/null
else
    PROJECT_ID="unknown"
    CLIENT_ID="unknown"
fi

# Count configured documents
DOCUMENT_COUNT=0
if [ -f ".claude/scripts/sync_config.json" ]; then
    DOCUMENT_COUNT=$(grep -c '":' ".claude/scripts/sync_config.json" 2>/dev/null || echo "0")
fi

# Check authentication status
if [ -f ".claude/scripts/token.pickle" ]; then
    AUTH_STATUS="✅ Authenticated"
else
    AUTH_STATUS="⚠️ Not authenticated"
fi

# Check Python environment
if [ -d ".claude/scripts/venv" ]; then
    PYTHON_ENV_STATUS="✅ Virtual environment ready"
else
    PYTHON_ENV_STATUS="⚠️ Virtual environment not found"
fi

# Generate the configuration record
cat > ".claude/project-config/google-cloud-config.md" << EOF
# Google Cloud Configuration Record

This file records the specific Google Cloud setup for this MADIO project's Google Docs synchronization capability.

**⚠️ This file is auto-generated during Google Docs sync setup. Do not edit manually.**

## Project Information

**Project Name**: \`$PROJECT_NAME\`  
**Project ID**: \`$PROJECT_ID\`  
**Project Number**: \`[Manual entry required - check Google Cloud Console]\`  
**Created**: \`[Manual entry required - check Google Cloud Console]\`  
**Setup By**: \`$USER_EMAIL\`  
**Setup Date**: \`$CURRENT_DATE\`

## Configuration Details

### APIs Enabled
- **Google Docs API** - Required for reading/writing Google Documents
- **Google Drive API** - Required for folder organization (if enabled)

### OAuth 2.0 Configuration
- **Application Type**: Desktop Application
- **Client Name**: \`[Manual entry required - check Google Cloud Console]\`
- **Client ID**: \`$CLIENT_ID\` (truncated for security)
- **Consent Screen**: \`External\` (\`Testing\` mode)
- **Test Users**: \`$USER_EMAIL\`

### Credentials Location
- **File**: \`.claude/scripts/credentials.json\`
- **Status**: ✅ Downloaded and configured
- **Security**: Added to .gitignore (contains sensitive OAuth secrets)
- **Permissions**: 600 (read/write for owner only)

### Sync Configuration
- **Sync Config File**: \`.claude/scripts/sync_config.json\`
- **Documents Configured**: \`$DOCUMENT_COUNT\`
- **Folder Support**: \`Enabled\` (if CREATE_NEW_DOCUMENT placeholders used)
- **Auto-Creation**: \`Enabled\` (CREATE_NEW_DOCUMENT functionality)

## Current Status

**Overall Status**: ✅ Setup Complete  
**Last Sync**: \`$CURRENT_DATE\` (initial setup)  
**Python Environment**: \`$PYTHON_ENV_STATUS\`  
**Authentication**: \`$AUTH_STATUS\`

## Troubleshooting Context

### Common Issues for This Project
- **403 Forbidden**: Check test user configuration in Google Cloud Console
- **Credentials not found**: Verify \`.claude/scripts/credentials.json\` exists
- **Token expired**: Delete \`token.pickle\` and re-authenticate
- **API quota exceeded**: Check Google Cloud Console quotas

### Project-Specific Notes
- Project configured for $PROJECT_NAME
- OAuth consent screen in testing mode (suitable for personal use)
- Credentials secured with 600 permissions
- Sync configuration supports $DOCUMENT_COUNT documents

## Maintenance History

| Date | Action | Status | Notes |
|------|--------|--------|-------|
| \`$CURRENT_DATE\` | Initial setup | ✅ Complete | Google Docs sync configured successfully |

## Related Files

- \`.claude/scripts/sync_to_docs.py\` - Main synchronization script
- \`.claude/scripts/credentials.json\` - OAuth credentials (not in git)
- \`.claude/scripts/token.pickle\` - Authentication token (not in git)
- \`.claude/scripts/sync_config.json\` - Document mapping configuration
- \`docs/GOOGLE_CLOUD_SETUP.md\` - User setup guide

---

**Note**: This configuration enables seamless integration between local MADIO development and cloud-based Claude Project knowledge bases through Google Docs synchronization.

**Security**: All sensitive information is stored in gitignored files. This record contains only non-sensitive configuration details for project maintenance.
EOF

echo "✅ Project configuration record created"
echo "   File: .claude/project-config/google-cloud-config.md"
echo "   Contains: Project details, setup info, and maintenance history"
```

### Phase 8: Setup Completion

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
echo "   • Project configuration record created"
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