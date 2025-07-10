# MADIO Google Docs Sync - Complete Setup Guide

> **🎯 Goal**: Get your MADIO project syncing with Google Docs in under 10 minutes

This guide provides **step-by-step instructions** for setting up Google Docs synchronization in your MADIO project. Follow each section in order for a smooth setup experience.

---

## 📋 Quick Overview

**What you'll accomplish:**
1. ✅ Configure Google Cloud APIs and credentials  
2. ✅ Install Python dependencies  
3. ✅ Choose your sync workflow (flexible or traditional)  
4. ✅ Complete your first successful sync  
5. ✅ Verify everything works correctly  

**Time Required:** ~10 minutes (plus Google Cloud setup waiting)  
**Prerequisites:** MADIO project with `.claude/` directory

---

## 🚨 Security Notice

> **⚠️ CRITICAL SECURITY REQUIREMENTS:**
> - **NEVER commit** `credentials.json` or `token.pickle` files to Git
> - **Set proper permissions:** `chmod 600 credentials.json` after download
> - **Keep credentials private:** These files provide access to your Google account
> - **Use separate accounts:** Consider a dedicated Google account for MADIO projects

---

## 🔧 Step 1: Google Cloud Setup

### 1.1 Create/Select Google Cloud Project
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. **Create new project** OR select existing project
3. Note your **Project ID** for reference

### 1.2 Enable Required APIs
**Enable BOTH APIs** (both are required):

1. **Google Docs API**
   - Search: "Google Docs API" → **Enable**
   - Purpose: Read/write document content

2. **Google Drive API** 
   - Search: "Google Drive API" → **Enable**
   - Purpose: Create documents and manage folders

### 1.3 Create OAuth2 Credentials
1. Navigate to **APIs & Services** → **Credentials**
2. Click **+ Create Credentials** → **OAuth client ID**
3. **Application type:** Desktop application
4. **Name:** "MADIO Sync" (or your preference)
5. **Download** the JSON file (e.g., `client_secret_xxx.json`)

### 1.4 Install Credentials
1. **Rename** downloaded file to `credentials.json`
2. **Move** to `.claude/scripts/credentials.json` in your project
3. **Set secure permissions:** `chmod 600 .claude/scripts/credentials.json`

✅ **Verification:** File exists at `.claude/scripts/credentials.json` with 600 permissions

---

## 📦 Step 2: Install Dependencies

### Option A: Automatic Setup (Recommended)
```bash
# From your project root
/madio-enable-sync
```

This command automatically:
- Creates Python virtual environment
- Installs all dependencies  
- Guides you through workflow selection
- Sets up initial configuration

### Option B: Manual Setup
```bash
# From your project root
cd .claude/scripts

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

✅ **Verification:** Run `python3 .claude/scripts/sync_to_docs.py --help` (should show help without errors)

---

## 🔀 Step 3: Choose Your Sync Workflow

### 🆕 Option A: Flexible Directory Sync (Recommended)
**Best for:** New projects, simple workflows, auto-discovery

**Setup:**
1. Create sync directory: `mkdir synced_docs`
2. Add markdown files: `echo "# My Document" > synced_docs/example.md`
3. Run sync: `python3 .claude/scripts/sync_to_docs.py --directory synced_docs`

**Benefits:**
- ✅ Zero configuration required
- ✅ Automatic file discovery
- ✅ Dynamic document creation
- ✅ Automatic ID mapping

### 📝 Option B: Traditional Config Sync
**Best for:** Specific file control, existing setups, complex mappings

**Setup:**
1. Edit `.claude/scripts/sync_config.json`
2. Configure file mappings:
   ```json
   {
     "../../project_system_instructions.md": "CREATE_NEW_DOCUMENT",
     "../../orchestrator.md": "CREATE_NEW_DOCUMENT"
   }
   ```
3. Run sync: `python3 .claude/scripts/sync_to_docs.py --config .claude/scripts/sync_config.json`

**Benefits:**
- ✅ Precise file control
- ✅ Custom document IDs
- ✅ Organized configuration
- ✅ Team-friendly setup

---

## 🚀 Step 4: Complete Your First Sync

### For Flexible Directory Sync:
```bash
# From project root - works from any directory!
python3 .claude/scripts/sync_to_docs.py --directory synced_docs
```

### For Traditional Config Sync:
```bash
# From project root - works from any directory!  
python3 .claude/scripts/sync_to_docs.py --config .claude/scripts/sync_config.json
```

**What happens on first run:**
1. 🔐 **Authentication**: Browser opens for Google OAuth consent
2. 📁 **Folder Setup**: Interactive Google Drive folder creation
3. 📄 **Document Creation**: New Google Docs created for each file
4. 💾 **ID Mapping**: Document IDs saved for future syncs
5. ✅ **Success**: Links to created documents displayed

**Expected Output:**
```
🚀 Starting Google Docs sync...
🔐 Authenticating with Google...
📁 Setting up Google Drive folder...
📄 Creating document: example.md
   ✅ Created: https://docs.google.com/document/d/ABC123/edit
💾 Updated mapping file: .synced_docs_mapping.json
🎉 Sync completed successfully!
```

---

## ✅ Step 5: Verification & Testing

### 5.1 Verify Document Creation
1. Check Google Drive for new "MADIO Documents" folder (or your chosen name)
2. Confirm documents appear with correct content
3. Verify document links work and are editable

### 5.2 Test Sync Updates
1. **Edit local file:** Add content to your markdown file
2. **Run sync again:** Same command as before
3. **Check Google Doc:** Verify changes appear in Google Docs

### 5.3 Test from Different Directories
```bash
# Test script works from anywhere
cd docs
python3 ../.claude/scripts/sync_to_docs.py --directory ../synced_docs

cd ..
# Should work the same
```

✅ **Success Criteria:** 
- Documents created in Google Drive ✅
- Content syncs correctly ✅  
- Script works from any directory ✅
- No error messages ✅

---

## 🎉 Next Steps

### Essential Commands
Now that sync is set up, use these commands:

**Sync changes:**
```bash
/push-to-docs  # Via MADIO command
# OR
python3 .claude/scripts/sync_to_docs.py --directory synced_docs
```

**Enable auto-sync on file changes:**
```bash
npm run watch-sync  # Automatically syncs when files change
```

**Troubleshoot issues:**
```bash
/madio-doctor  # Comprehensive diagnostic tool
```

### Workflow Integration
- **Claude Projects:** Copy Google Doc URLs to your Claude Project knowledge
- **AI Integration:** Documents now accessible by your AI companions
- **Team Collaboration:** Share Google Docs for collaborative editing
- **Version Control:** Keep markdown files in Git, sync to Docs for AI access

---

## 🔧 Troubleshooting

### Common Issues

**"Config file not found"**
- ✅ **Solution:** Use full path: `--config .claude/scripts/sync_config.json`
- ✅ **New:** Script now works from any directory (path resolution fixed)

**"Credentials not found"**  
- ✅ **Check:** File exists at `.claude/scripts/credentials.json`
- ✅ **Permissions:** Run `chmod 600 .claude/scripts/credentials.json`
- ✅ **Path:** Ensure file is in script directory, not project root

**"API not enabled"**
- ✅ **Verify:** Both Google Docs API AND Google Drive API enabled
- ✅ **Wait:** API enablement can take 5-10 minutes to propagate

**"Permission denied"**
- ✅ **OAuth:** Complete OAuth consent flow in browser
- ✅ **Scopes:** Ensure credentials have Docs + Drive permissions

**"Token expired"**
- ✅ **Delete:** Remove `.claude/scripts/token.pickle`
- ✅ **Re-auth:** Run sync again to re-authenticate

### Get Help
- **Diagnostic tool:** `/madio-doctor` for automated troubleshooting
- **Detailed docs:** `.claude/commands/push-to-docs.md`
- **Architecture guide:** `docs/ARCHITECTURAL_REFACTORING_ROADMAP.md`

---

## 📚 Advanced Features

### Auto-sync on File Changes
Set up automatic syncing when files are modified:
```bash
# Install chokidar globally
npm install -g chokidar-cli

# Watch and sync automatically  
chokidar "synced_docs/**/*.md" -c "python3 .claude/scripts/sync_to_docs.py --directory synced_docs"
```

### Custom Google Drive Folders
Organize documents in specific folders during sync setup:
- Interactive folder creation during first run
- Nested folder support
- Team folder sharing options

### Multiple Project Support
Each MADIO project maintains its own:
- Credentials and authentication
- Document mappings
- Folder organization
- Sync configuration

---

*✅ **Setup Complete!** Your MADIO project now syncs seamlessly with Google Docs for enhanced AI collaboration.*

**Quick Reference:**
- **Sync:** `/push-to-docs` or `python3 .claude/scripts/sync_to_docs.py --directory synced_docs`
- **Help:** `/madio-doctor` for troubleshooting
- **Docs:** `.claude/commands/push-to-docs.md` for advanced usage