# MADIO Update Docs Command

Manages individual documents within the MADIO project registry and their corresponding local files and Google Doc links.

## Command Purpose

This command provides granular control over the document registry, allowing users to:
- Add new local documents to the registry.
- Remove documents from the registry (and optionally delete local files and associated Google Docs).
- Update metadata for existing documents in the registry.

## Usage

```bash
# Add a new document to the registry
/madio-update-docs --add path/to/your/new_document.md [--tier N] [--source X]

# Remove a document from the registry
/madio-update-docs --remove path/to/document_in_registry.md

# Update metadata for a document in the registry
/madio-update-docs --update-metadata path/to/document_in_registry.md [--tier N] [--status new_status] [--source new_source]
```

## Arguments

### `--add <filepath>`
- Adds a new document to the MADIO registry.
- `<filepath>`: Path to the local markdown file to add.
- The file is typically copied into a managed location (e.g., `synced_docs/` or project root, depending on project convention). The registry will store its path relative to the project root.
- Initializes the document with `status: "local_only"`. A `/push-to-docs` is needed to sync it to Google Drive.
- Optional arguments for `--add`:
    - `--tier <N>`: Specify the MADIO tier (e.g., 1, 2, 3).
    - `--source <description>`: Describe the source of the document (e.g., "manual", "generated_topic_X").

### `--remove <filepath>`
- Removes a document from the MADIO registry.
- `<filepath>`: Path (relative to project root) of the document as stored in the registry.
- Deletes the local managed file.
- Prompts the user whether to delete the associated Google Doc from Google Drive or just unlink it.

### `--update-metadata <filepath>`
- Updates metadata fields for an existing document in the registry.
- `<filepath>`: Path (relative to project root) of the document in the registry.
- Optional arguments for `--update-metadata` (at least one must be provided):
    - `--tier <N>`: Change the MADIO tier.
    - `--status <status_string>`: Manually set a new status (e.g., "archived", "review_needed").
    - `--source <description>`: Update the source description.
    - _Other fields like `google_doc_id` might be updatable via specific flags in future enhancements if manual re-linking is needed._

## Important Notes
- All paths specified should generally be relative to the project root.
- This command directly manipulates the `.madio/document_registry.json` file.
- Ensure your project is initialized (`/madio-setup`) before using this command.

## Command Implementation (Bash wrapper)

```bash
#!/bin/bash

echo "🛠️ MADIO Document Update Tool"
echo "============================"
echo ""

SCRIPT_PATH=".claude/scripts/manage_docs.py" # Python script to handle the logic

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "❌ Document management script not found at $SCRIPT_PATH"
    echo "Ensure your MADIO framework is up to date."
    exit 1
fi

# Pass all arguments to the Python script
python3 "$SCRIPT_PATH" "$@"

RESULT=$?

echo ""
if [ $RESULT -eq 0 ]; then
    echo "✅ Document update operation completed successfully."
else
    echo "❌ Document update operation failed. See output above for details."
fi
exit $RESULT
```

## Manual Execution (Alternative)
If the slash command is not available or you prefer direct execution:
```bash
python .claude/scripts/manage_docs.py [arguments]
```
Example: `python .claude/scripts/manage_docs.py --add docs/my_new_idea.md --tier 3`
