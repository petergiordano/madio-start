# Google Docs Sync for MADIO

This directory contains the Google Docs synchronization system for MADIO projects. This enables seamless integration between local markdown development and Claude Project knowledge bases.

## What This Enables

- **Local Development**: Claude can edit markdown files directly via MCP filesystem
- **Cloud Sync**: Automatic synchronization to Google Docs
- **Project Knowledge**: Google Docs automatically update Claude Project knowledge
- **Framework Evolution**: Continuous improvement workflow without git barriers

## Quick Start

1. **Run setup script:**
   ```bash
   chmod +x .claude/scripts/setup.sh
   ./.claude/scripts/setup.sh
   ```

2. **Get Google credentials:**
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Google Docs API
   - Create OAuth2 credentials (Desktop application)
   - Download as `credentials.json` to this directory

3. **Configure document mapping:**
   - Edit `sync_config.json` in project root
   - Replace placeholder IDs with actual Google Doc IDs

4. **Test the sync:**
   ```bash
   /push-to-docs
   ```

## Files in this directory

- `sync_to_docs.py` - Main synchronization script
- `requirements.txt` - Python dependencies
- `setup.sh` - Automated setup script
- `credentials.json` - Google OAuth credentials (you add this)
- `token.pickle` - Cached authentication token (auto-generated)

## Security Notes

- `credentials.json` contains sensitive data - add to .gitignore
- `token.pickle` contains access tokens - add to .gitignore
- Only add directories you trust to MCP filesystem access
- Google Docs sync uses full document replacement for reliability

## Troubleshooting

If sync fails:
1. Check `credentials.json` exists and is valid
2. Verify Google Doc IDs in `sync_config.json`
3. Ensure you have edit access to all Google Docs
4. Delete `token.pickle` and re-authenticate if needed

For detailed help, see `../commands/push-to-docs.md`
