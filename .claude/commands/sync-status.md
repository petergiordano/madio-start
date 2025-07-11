# MADIO Sync Status Command

Checks the health of the document registry, local files, and their Google Doc counterparts, and can attempt to repair issues.

## Command Purpose

This command helps users understand the current synchronization state of their MADIO project and fix common problems with document mappings and accessibility. It uses the `.madio/document_registry.json` as the source of truth.

## Usage

```bash
# Perform a health check (default action)
/sync-status
/sync-status --health-check

# Perform a health check and attempt interactive repair of issues
/sync-status --repair
```

## Arguments

### `--health-check` (Default)
- Loads the `.madio/document_registry.json`.
- For each document entry, it verifies:
    - **Local File:** Existence at the registered `local_path`. Consistency by comparing current SHA256 hash with `local_sha256_hash` in the registry.
    - **Google Doc Link:** If `google_doc_id` exists, it checks accessibility (not trashed, not 404). It may also compare the stored `google_doc_version` with the live version on Google Drive.
- Reports a summary of findings:
    - Number of documents in registry.
    - Number of documents perfectly synced (`status: "active"` and hashes/versions match).
    - Number of documents with local changes not yet synced (hash mismatch, local newer).
    - Number of documents with remote (Google Doc) changes not yet pulled/reconciled (version mismatch, GDoc newer).
    - Number of documents with errors (e.g., `status` indicates `error_local_missing`, `error_gdoc_inaccessible`).
- Lists individual documents with discrepancies or errors, showing their current `status` from the registry and any live-check findings.
- Does **not** make any changes to files or the registry.

### `--repair`
- Performs all actions of `--health-check`.
- For each discrepancy or error found where an automated or interactive fix is possible:
    - **Local file missing:** Invokes interactive prompts (similar to `sync_to_docs.py`) to (R)emove from registry, (U)nlink GDoc & Remove, (S)kip, or (A)bort.
    - **GDoc inaccessible (trashed/404):** Invokes interactive prompts to (C)reate new GDoc, (U)nlink, (S)kip, or (A)bort.
    - **Local changes detected (hash mismatch) AND GDoc also changed (version mismatch) - Conflict:** Invokes conflict resolution prompts (similar to `sync_to_docs.py`) - (L)ocal overwrites GDoc, (G)Doc overwrites local, (S)kip. (Note: This part might be deferred if conflict resolution logic is complex and primarily in `sync_to_docs.py` for Phase 3).
    - **Only local changes detected:** Suggests running `/push-to-docs`. Repair might offer to update `local_sha256_hash` and `last_modified_local_at` if user confirms file is as intended but just not yet processed for sync.
    - **Only remote GDoc changes detected:** Suggests user manually review. Repair might offer to update `google_doc_version` in registry to acknowledge remote state.
- Updates the `.madio/document_registry.json` based on user choices during repair.

## Important Notes
- The `--repair` option can make significant changes to your registry. It's advisable to understand the implications or back up your registry file first.
- Actual content synchronization (pushing or pulling content) is primarily handled by `/push-to-docs`. This command focuses on fixing registry metadata, links, and known states.

## Command Implementation (Bash wrapper)

```bash
#!/bin/bash

echo "🩺 MADIO Sync Status & Health Check"
echo "==================================="
echo ""

SCRIPT_PATH=".claude/scripts/check_sync_health.py" # Python script to handle the logic

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Sync health check script not found at $SCRIPT_PATH"
    echo "Ensure your MADIO framework is up to date."
    exit 1
fi

# Pass all arguments to the Python script
python3 "$SCRIPT_PATH" "$@"

RESULT=$?

echo ""
if [ $RESULT -eq 0 ]; then
    echo "✅ Sync status operation completed."
else
    echo "❌ Sync status operation encountered issues. See output above for details."
fi
exit $RESULT
```

## Manual Execution (Alternative)
```bash
python .claude/scripts/check_sync_health.py [--health-check | --repair]
```
