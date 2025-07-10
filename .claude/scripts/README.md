# Google Docs Sync for MADIO

This directory contains the Google Docs synchronization system for MADIO projects. This enables seamless integration between local markdown development and Claude Project knowledge bases.

## What This Enables

- **Local Development**: Claude can edit markdown files directly via MCP filesystem
- **Cloud Sync**: Automatic synchronization to Google Docs
- **Project Knowledge**: Google Docs automatically update Claude Project knowledge
- **Framework Evolution**: Continuous improvement workflow without git barriers

## Two Sync Workflows Available

### 🆕 Flexible Directory Sync (Recommended)
- **Zero Configuration**: Just add `.md` files to `synced_docs/` directory
- **Auto-Discovery**: Recursively finds all markdown files
- **Auto-Creation**: Creates Google Docs automatically for new files
- **Persistent Mapping**: Tracks file→doc relationships in `.synced_docs_mapping.json`

### 📝 Traditional Config Sync
- **Manual Configuration**: Edit `sync_config.json` with file paths and doc IDs
- **Precise Control**: Specify exactly which files sync where
- **Legacy Support**: Maintains compatibility with existing setups

## Quick Start

1. **Run setup script:**
   ```bash
   chmod +x .claude/scripts/setup.sh
   ./.claude/scripts/setup.sh
   ```
   Choose your preferred workflow (Flexible recommended for new users)

2. **Get Google credentials:**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Enable **both** Google Docs API and Google Drive API
   - Create OAuth2 credentials (Desktop application)
   - Download as `credentials.json` to this directory

3. **Sync your documents:**
   
   **Flexible Directory Sync:**
   ```bash
   # Add your .md files to synced_docs/
   python .claude/scripts/sync_to_docs.py --directory synced_docs
   ```
   
   **Traditional Config Sync:**
   ```bash
   # Edit sync_config.json first, then:
   python .claude/scripts/sync_to_docs.py --config sync_config.json
   ```

## Complete MADIO Workflow

### New User Journey:
1. **Setup Framework**: Run `/madio-setup` (sets up MADIO templates)
2. **Setup Sync**: Run `./.claude/scripts/setup.sh` (installs dependencies, chooses workflow)
3. **Generate AI System**: Run `/generate-ai-system` (creates MADIO documents)
4. **First-Time Sync**: Run sync command (auto-creates Google Docs, stores IDs)
5. **Ongoing Development**: Edit files locally, sync pushes changes to existing docs

### MADIO Integration:
- `/generate-ai-system` can automatically move files to `synced_docs/`
- First sync creates Google Docs for all generated MADIO files
- Subsequent syncs update existing docs using stored document IDs
- File→Doc mappings persist in `.synced_docs_mapping.json`

## Files in this directory

- `sync_to_docs.py` - Main synchronization script with flexible directory support
- `requirements.txt` - Python dependencies (Google APIs)
- `setup.sh` - Automated setup script with workflow choice
- `sync_config.json` - Traditional config file (if using config mode)
- `credentials.json` - Google OAuth credentials (you add this)
- `token.pickle` - Cached authentication token (auto-generated)

## Security Notes

- `credentials.json` contains sensitive data - add to .gitignore
- `token.pickle` contains access tokens - add to .gitignore
- `.synced_docs_mapping.json` tracks doc IDs - safe to commit
- Only add directories you trust to MCP filesystem access
- Google Docs sync uses full document replacement for reliability

## Troubleshooting

### Flexible Directory Sync Issues:
1. Check `synced_docs/` directory exists and contains `.md` files
2. Verify `.synced_docs_mapping.json` has correct file→doc ID mappings
3. Ensure Google Drive API is enabled (for document creation)

### Traditional Config Sync Issues:
1. Check `sync_config.json` exists and has valid structure
2. Verify Google Doc IDs are correct and accessible
3. Use `CREATE_NEW_DOCUMENT` placeholder for auto-creation

### General Issues:
1. Check `credentials.json` exists and is valid JSON
2. Ensure both Google Docs API and Google Drive API are enabled
3. Verify you have edit access to all Google Docs
4. Delete `token.pickle` and re-authenticate if needed
5. Run `/madio-doctor` for comprehensive diagnostics

For detailed help, see `../commands/push-to-docs.md`
