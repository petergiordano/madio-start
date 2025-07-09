# Google Docs Sync Test Files

Test files for validating MADIO Google Docs synchronization functionality.

## Test Files

### Knowledge Base Files (3)
- `test_orchestrator.md` → Google Doc ID: `1RdDNthNa0ayZu31MnKNo6RE20b_RBVzGqIDrKHkzIYc`
- `test_methodology_framework.md` → Google Doc ID: `1rl8lbQrjlRoNZ2F62g3VWfxc_eGN5D1qk17F9Fu9eY0`
- `test_content_operations.md` → Google Doc ID: `1WpUo3I9X7F9vmQdiE_ip1y4RN84__R_Vlzs85me_20M`

### Configuration
- `test_sync_config.json` - Maps test files to Google Doc IDs

## Test Behavior Triggers

Each file contains deliberate test responses:

- **Orchestrator**: "analyze test scenario" → "ORCHESTRATOR ACTIVE"
- **Methodology**: Test scenarios → "FRAMEWORK VERSION: Original"
- **Content Operations**: "what are the content guidelines" → "CONTENT OPERATIONS GUIDELINES VERSION: Original"

## Test Plan

1. Create Claude Project with these 3 Google Docs as knowledge
2. Test initial behavior triggers
3. Modify test files locally via Claude Code/MCP
4. Run `/push-to-docs` to sync changes
5. Verify Google Docs updated
6. Refresh Claude Project knowledge
7. Test behavior changes to confirm sync worked

## Note
Project instructions (`test_project_system_instructions.md`) removed - goes into Claude Project Instructions, not knowledge base.