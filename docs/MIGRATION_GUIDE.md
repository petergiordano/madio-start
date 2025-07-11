# MADIO Project Migration Guide
## Upgrading to the New `.madio/document_registry.json` System

This guide is for users who have existing MADIO projects that were set up for Google Docs synchronization using the older configuration methods (`.claude/scripts/sync_config.json` and/or `.synced_docs_mapping.json`). The MADIO framework has transitioned to a new, unified system for managing document state and synchronization: the `.madio/document_registry.json` file.

To continue using Google Docs sync and benefit from new features like improved stale mapping detection, conflict resolution, and lifecycle tracking, you'll need to migrate your project's configuration.

## Why Migrate?

The new `.madio/document_registry.json` system offers:
-   **Centralized Management:** All document metadata, local file info (like content hashes), Google Doc IDs, versions, and sync preferences (like the target Google Drive folder) are stored in one place.
-   **Enhanced Accuracy:** Tracking file hashes and Google Doc versions allows for more precise detection of changes and potential conflicts.
-   **Improved Stability:** Better handling of stale mappings (e.g., deleted local files or Google Docs).
-   **Richer Feature Set:** Enables more advanced commands like `/sync-status --repair` and more granular control with `/madio-update-docs`.

## Before You Begin: Backup!

**It is STRONGLY recommended to back up your entire project directory before running the migration command.** This is especially important for:
-   `.claude/scripts/sync_config.json` (if you use it)
-   `.synced_docs_mapping.json` (if you use it, typically in your project root)
-   Any existing `.madio/document_registry.json` if you were part of early testing or manually created one.

A simple way to back up is to create a zip archive of your project or copy the entire project folder to a safe location.

## The Migration Command: `/madio-migrate-config`

MADIO provides a command to help automate this transition:

```bash
/madio-migrate-config
```

**What this command does:**
1.  **Prompts for Confirmation:** It will ask you to confirm before proceeding, reminding you about backups and potential overwrites if a `.madio/document_registry.json` already exists from a previous migration attempt.
2.  **Locates Old Configuration Files:**
    *   It looks for `.claude/scripts/sync_config.json`.
    *   It looks for `.synced_docs_mapping.json` in your project root.
3.  **Initializes a New Registry:** It prepares to create a fresh `.madio/document_registry.json`.
4.  **Migrates Data:**
    *   **Folder Preference:** If `_google_drive_folder` was defined in your `sync_config.json`, its `name` and `id` are copied to the `sync_preferences.google_drive_folder` section of the new registry.
    *   **Document Entries:**
        *   It reads file paths and Google Doc IDs (or `CREATE_NEW_DOCUMENT` placeholders) from both old configuration files.
        *   Paths from `sync_config.json` (which were relative to `.claude/scripts/`) are correctly resolved to be relative to your project root in the new registry.
        *   Paths from `.synced_docs_mapping.json` (which were usually already relative to project root) are used as is.
        *   If a document path appears in both old files, the information from `.synced_docs_mapping.json` might be prioritized for the `google_doc_id` if it seems more specific (e.g., an actual ID vs. a placeholder). The `add_or_update_document_entry` logic in `madio_registry.py` handles merging these.
        *   For each migrated entry, the new registry will store:
            *   `google_doc_id` (or `null` if it was `CREATE_NEW_DOCUMENT`).
            *   `status` set to "migrated" or "migrated_placeholder".
            *   `source` set to "migrated_sync_config" or "migrated_dir_mapping".
            *   `created_at` and `last_modified_local_at` timestamps set to the time of migration.
            *   `local_sha256_hash` calculated from the local file if it exists at the registered path.
            *   Other fields (like `google_doc_version`, `last_synced_at`) initialized to `null` or default values.
5.  **Saves the New Registry:** The populated `.madio/document_registry.json` is saved.
6.  **Does NOT Delete Old Files:** The original `sync_config.json` and `.synced_docs_mapping.json` are NOT deleted by the script. You can manually remove or archive them after you've verified the migration.

## Steps to Migrate Your Project

1.  **Ensure your MADIO framework scripts are up-to-date,** especially:
    *   `.claude/commands/madio-migrate-config.md`
    *   `.claude/scripts/madio_migrate_config.py`
    *   `.claude/scripts/madio_registry.py`
    *   `.claude/scripts/sync_to_docs.py` (as it will use the new registry).
2.  **Open your MADIO project in your terminal.**
3.  **BACK UP YOUR PROJECT.** (See "Before You Begin" above).
4.  **Run the migration command:**
    ```bash
    /madio-migrate-config
    ```
5.  **Confirm Execution:** Read the prompt carefully and type `y` or `yes` if you wish to proceed.
6.  **Review Output:** The script will print information about the files it found and migrated. Note any warnings or errors.
7.  **Inspect the New Registry:** Open `.madio/document_registry.json` and review its contents. Check if:
    *   Your document paths look correct (relative to project root).
    *   Google Doc IDs seem to have transferred.
    *   Your Google Drive folder preference (if any) is in `sync_preferences`.
8.  **Test with New Commands:**
    *   Run `/sync-status` or `/sync-status --health-check`. It should now read from the new registry and report the status of your documents. This is a good way to see if the migration correctly captured your document states.
    *   If you need to fix anything reported by health check (e.g., hashes for existing files that weren't found during migration but exist now), you can try `/sync-status --repair`.
    *   When ready, try `/push-to-docs`. This will use the new registry. Pay attention to the first sync after migration, especially regarding folder selection (it should use your migrated preference or prompt you if none was set).

## Troubleshooting Common Migration Issues

*   **"Old sync_config.json not found" / ".synced_docs_mapping.json not found":**
    *   This is okay if your project didn't use one of these methods. The script will migrate what it finds. If you expect a file to be there, ensure you're in the correct project root directory and the file exists at the expected path.
*   **Incorrect paths in the new registry:**
    *   If paths in `.madio/document_registry.json` don't look right (e.g., still have `../../`), double-check the path resolution logic in your version of `madio_migrate_config.py`. The script attempts to make all `local_path` entries relative to the project root.
*   **Folder preference not migrated:**
    *   Ensure your old `sync_config.json` had a `_google_drive_folder` object with a `name` or `id`.
*   **`/push-to-docs` wants to re-create all Google Docs:**
    *   This might happen if `google_doc_id` fields in the new registry are all `null` (e.g., if all old entries were `CREATE_NEW_DOCUMENT` or IDs were lost). If you have existing GDocs, you might need to manually edit the `google_doc_id` in `document_registry.json` before the first `/push-to-docs` if the migration couldn't pick them up. `/sync-status --repair` might also help re-link if local files and GDocs titles match in a detectable way (though this advanced re-linking is not a primary feature of Phase 2/3 repair).

## After Successful Migration

Once you are confident that `.madio/document_registry.json` is correct and commands like `/push-to-docs` and `/sync-status` are working as expected:
1.  You can **safely delete or archive** your old configuration files:
    *   `.claude/scripts/sync_config.json`
    *   `.synced_docs_mapping.json` (from project root)
2.  Commit the new `.madio/document_registry.json` to your version control (Git), but ensure your `.gitignore` is correctly set up to exclude sensitive files like `token.pickle` or any direct credentials. The registry itself (with file paths and non-sensitive IDs) is intended to be version controlled.

If you encounter issues, refer to the output of the scripts, check the main `README.md`, or the specific command documentations.
