# Google Cloud Configuration for MADIO

This document records the Google Cloud setup for MADIO Google Docs synchronization capability.

## Project Overview

**Project Name**: `markdown-to-docs`  
**Project ID**: `markdown-to-docs-465320`  
**Project Number**: `228174740470`  
**Created**: July 8, 2025

## Purpose

Enables local markdown files to be synchronized to Google Docs for seamless Claude Project knowledge base integration. This bridges the gap between local development (with Claude write access via MCP) and cloud-based Claude Project knowledge.

## Configuration Details

### APIs Enabled
- **Google Docs API** - Required for reading/writing Google Documents

### OAuth 2.0 Configuration
- **Application Type**: Desktop Application
- **Client Name**: "MADIO Sync Client"
- **Client ID**: `228174740470-p017...` (truncated for security)
- **Consent Screen**: External (Testing mode)
- **Test Users**: Project owner email

### Credentials Location
- **File**: `.claude/scripts/credentials.json`
- **Status**: ✅ Downloaded and configured
- **Security**: Added to .gitignore (contains sensitive OAuth secrets)

## Testing Mode Limitations

Currently configured in **testing mode**, which means:
- Only test users (project owner) can authenticate
- App shows "unverified" warning during OAuth flow
- Suitable for personal/development use
- See `TODO.md` for production publishing requirements

## Usage Workflow

1. **Local Development**: Claude edits `.md` files via MCP filesystem
2. **Sync Command**: `/push-to-docs` executes Python sync script
3. **Authentication**: OAuth flow (one-time browser consent)
4. **Sync Process**: Full document replacement in Google Docs
5. **Claude Project**: Automatic knowledge base refresh from Google Docs

## Security Considerations

- OAuth credentials stored locally in `.claude/scripts/credentials.json`
- Access tokens cached in `.claude/scripts/token.pickle`
- Both files excluded from version control
- Principle of least privilege: Only Google Docs API access
- User maintains full control over which documents to sync

## Maintenance

### Token Refresh
- Tokens automatically refresh when expired
- Manual refresh: Delete `token.pickle` and re-authenticate

### Adding Test Users
- Google Cloud Console → OAuth consent screen → Test users
- Add email addresses for additional MADIO users

### Production Deployment
- See `TODO.md` for OAuth app verification requirements
- May require privacy policy and terms of service
- Google verification process for public access

## Troubleshooting

### Common Issues
1. **403 Forbidden**: Check test user configuration
2. **Credentials not found**: Verify `credentials.json` location
3. **Token expired**: Delete `token.pickle` and re-authenticate
4. **API quota exceeded**: Check Google Cloud Console quotas

### Support Resources
- Google Cloud Console: https://console.cloud.google.com/
- OAuth 2.0 documentation: https://developers.google.com/identity/protocols/oauth2
- Google Docs API: https://developers.google.com/docs/api

## Related Files

- `.claude/scripts/sync_to_docs.py` - Main synchronization script
- `.claude/commands/push-to-docs.md` - Claude command documentation
- `sync_config.json` - Document mapping configuration
- `TODO.md` - Production deployment tasks

---

**Note**: This configuration enables the MADIO framework's breakthrough capability: seamless integration between local development with Claude write access and cloud-based Claude Project knowledge bases.
