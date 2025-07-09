# Google Cloud Configuration Record

This file records the specific Google Cloud setup for this MADIO project's Google Docs synchronization capability.

**⚠️ This file is auto-generated during Google Docs sync setup. Do not edit manually.**

## Project Information

**Project Name**: `[PROJECT_NAME]`  
**Project ID**: `[PROJECT_ID]`  
**Project Number**: `[PROJECT_NUMBER]`  
**Created**: `[CREATION_DATE]`  
**Setup By**: `[USER_EMAIL]`  
**Setup Date**: `[SETUP_DATE]`

## Configuration Details

### APIs Enabled
- **Google Docs API** - Required for reading/writing Google Documents
- **Google Drive API** - Required for folder organization and document creation

### OAuth 2.0 Configuration
- **Application Type**: Desktop Application
- **Client Name**: `[CLIENT_NAME]`
- **Client ID**: `[CLIENT_ID]` (truncated for security)
- **Consent Screen**: `[CONSENT_SCREEN_TYPE]` (`[CONSENT_SCREEN_STATUS]` mode)
- **Test Users**: `[TEST_USERS]`

### Credentials Location
- **File**: `.claude/scripts/credentials.json`
- **Status**: `[CREDENTIALS_STATUS]`
- **Security**: Added to .gitignore (contains sensitive OAuth secrets)
- **Permissions**: 600 (read/write for owner only)

### Sync Configuration
- **Sync Config File**: `.claude/scripts/sync_config.json`
- **Documents Configured**: `[DOCUMENT_COUNT]`
- **Folder Support**: `[FOLDER_SUPPORT_STATUS]`
- **Auto-Creation**: `[AUTO_CREATION_STATUS]`

## Current Status

**Overall Status**: `[OVERALL_STATUS]`  
**Last Sync**: `[LAST_SYNC_DATE]`  
**Python Environment**: `[PYTHON_ENV_STATUS]`  
**Authentication**: `[AUTH_STATUS]`

## Troubleshooting Context

### Common Issues for This Project
- **403 Forbidden**: Check test user configuration in Google Cloud Console
- **Credentials not found**: Verify `.claude/scripts/credentials.json` exists
- **Token expired**: Delete `token.pickle` and re-authenticate
- **API quota exceeded**: Check Google Cloud Console quotas

### Project-Specific Notes
`[PROJECT_NOTES]`

## Maintenance History

| Date | Action | Status | Notes |
|------|--------|--------|-------|
| `[SETUP_DATE]` | Initial setup | `[INITIAL_STATUS]` | `[INITIAL_NOTES]` |

## Related Files

- `.claude/scripts/sync_to_docs.py` - Main synchronization script
- `.claude/scripts/credentials.json` - OAuth credentials (not in git)
- `.claude/scripts/token.pickle` - Authentication token (not in git)
- `.claude/scripts/sync_config.json` - Document mapping configuration
- `docs/GOOGLE_CLOUD_SETUP.md` - User setup guide

---

**Note**: This configuration enables seamless integration between local MADIO development and cloud-based Claude Project knowledge bases through Google Docs synchronization.

**Security**: All sensitive information is stored in gitignored files. This record contains only non-sensitive configuration details for project maintenance.