# Google Docs Sync Test Files

This directory contains test files for validating the MADIO Google Docs synchronization functionality.

## Test Files

### Markdown Test Documents
- `test_project_system_instructions.md` - Marketing Analysis AI with test behavior trigger
- `test_orchestrator.md` - Step-by-step methodology with "ORCHESTRATOR ACTIVE" response
- `test_methodology_framework.md` - Analysis framework with "FRAMEWORK VERSION: Original" response

### Configuration
- `test_sync_config.json` - Test configuration mapping these files to Google Doc IDs

## Test Behavior Triggers

These files contain specific triggers to validate sync functionality:

1. **Initial Behavior Test**
   - Trigger: "analyze test scenario"
   - Expected Response: "INITIAL BEHAVIOR: This response confirms..."

2. **Orchestrator Test**
   - Trigger: "test orchestrator active"
   - Expected Response: "ORCHESTRATOR ACTIVE: Step-by-step methodology engaged..."

3. **Framework Version Test**
   - Trigger: "check framework version"
   - Expected Response: "FRAMEWORK VERSION: Original"

## Testing Workflow

1. **Setup Google Docs**
   - Create test Google Docs for each markdown file
   - Get the document IDs from the URLs
   - Update `test_sync_config.json` with actual IDs

2. **Initial Sync**
   ```bash
   /push-to-docs --config .claude/tests/google-docs-sync/test_sync_config.json
   ```

3. **Test Initial Behavior**
   - Create Claude Project with test docs
   - Test triggers to verify initial responses

4. **Modify and Re-sync**
   - Change test behaviors in markdown files
   - Re-sync to Google Docs
   - Verify Claude Project picks up changes

5. **Validate Results**
   - Confirm modified behaviors work
   - Test all three documents
   - Verify sync completeness

## Important Notes

- These files are for framework testing only
- Do not include in user projects during `/madio-setup`
- Keep updated as sync functionality evolves
- Use for regression testing when updating sync code