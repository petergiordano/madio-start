# MADIO Migrate Configuration Command

Migrates existing old MADIO sync configurations to the new `.madio/document_registry.json` format.

## Purpose

As MADIO evolves, its configuration for Google Docs synchronization is changing from:
- `.claude/scripts/sync_config.json` (for specific file mappings and folder preferences)
- `.synced_docs_mapping.json` (for directory-based sync in `synced_docs/`)

to a unified:
- `.madio/document_registry.json`

This command facilitates that transition.

## Usage

```bash
/madio-migrate-config
```

**What this does:**
1.  Reads data from any existing `sync_config.json` and `.synced_docs_mapping.json` files.
2.  Transforms this data into the new `document_registry.json` structure.
3.  Saves the new `.madio/document_registry.json` file.
4.  Prompts the user for confirmation before proceeding.
5.  Advises backing up the project first.

**When to use:**
- If you have an existing MADIO project that was set up with Google Docs sync before the introduction of the `document_registry.json`.
- Run this command **once** per project to upgrade its configuration.

## Important Notes
-   **Backup Recommended**: Before running this command, it is highly recommended to back up your project, especially the old configuration files and any existing `.madio/document_registry.json` if you were experimenting.
-   **Overwriting**: If a `.madio/document_registry.json` file already exists, this script will effectively overwrite its contents with the migrated data (it starts from an empty registry structure and fills it from old configs).
-   **Idempotency**: Running the script multiple times might produce the same result if old configs haven't changed, but it's generally intended to be run once.
-   **Old Files**: The script does **not** delete your old configuration files. You can manually back them up or remove them after verifying the migration was successful.

## Command Implementation (Bash wrapper)

```bash
#!/bin/bash

echo "🚀 MADIO Configuration Migration Tool"
echo "===================================="
echo ""

SCRIPT_PATH=".claude/scripts/madio_migrate_config.py"

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Migration script not found at $SCRIPT_PATH"
    echo "Ensure your MADIO framework is up to date."
    exit 1
fi

# Ask for confirmation within the Python script itself to handle prompts better.
# The Python script has its own confirmation prompt.
python3 "$SCRIPT_PATH"

echo ""
echo "Migration process finished. Check output above for details."

```

## Manual Execution (Alternative)
If the slash command is not available or you prefer direct execution:
```bash
python .claude/scripts/madio_migrate_config.py
```
Follow the prompts in the terminal.
