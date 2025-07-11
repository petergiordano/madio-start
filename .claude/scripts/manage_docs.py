import argparse
import json
import os
import shutil
import sys
import datetime
from pathlib import Path

try:
    from . import madio_registry # Relative import
    # May need Drive service for GDoc deletion if implemented here
    # from .sync_to_docs import GoogleDocsSync # Or a shared Drive service module
except ImportError:
    import madio_registry
    # from sync_to_docs import GoogleDocsSync


# Helper to get a Drive service - Placeholder, actual implementation might be more complex
# For now, GDoc deletion prompt will be informational, actual deletion not implemented in this script.
def get_drive_service_placeholder():
    print("INFO: Google Drive service interaction (e.g., for GDoc deletion) is a placeholder in this script version.")
    # In a real scenario:
    # sync_instance = GoogleDocsSync() # Initializes auth etc.
    # return sync_instance.drive_service
    return None

def get_user_confirmation(prompt_message, default_yes=False):
    suffix = " (Y/n): " if default_yes else " (y/N): "
    choice = input(prompt_message + suffix).strip().lower()
    if default_yes:
        return choice != 'n'
    else:
        return choice == 'y'

def add_document(args, registry_data, project_root):
    filepath_to_add = Path(args.add).resolve() # Absolute path of the source file

    if not filepath_to_add.exists() or not filepath_to_add.is_file():
        print(f"❌ Error: Source file not found or is not a file: {filepath_to_add}")
        return False

    # Determine managed location. Convention: 'synced_docs/' or project_root if not specified
    # For now, let's assume new docs are copied to 'synced_docs/' for consistency with import.
    # If the source is already in 'synced_docs/', we might just register it.
    # This needs a clearer project convention for where "managed" local docs live.
    # Let's assume if a file is added, it's meant to be part of the synced set.
    # A simple convention: if `synced_docs` exists, copy there. Otherwise, register in place.

    synced_docs_dir = project_root / "synced_docs"
    target_filename = filepath_to_add.name

    destination_path_abs = filepath_to_add # Default to registering in-place if not copied
    path_in_registry_str = str(filepath_to_add.relative_to(project_root))


    if synced_docs_dir.is_dir(): # If synced_docs exists, prefer copying there
        destination_path_abs = synced_docs_dir / target_filename
        path_in_registry_str = str(destination_path_abs.relative_to(project_root))

        if filepath_to_add.resolve() != destination_path_abs.resolve(): # Only copy if not already in dest
            if destination_path_abs.exists():
                if not get_user_confirmation(f"File {destination_path_abs} already exists. Overwrite?"):
                    print("Skipping add operation.")
                    return True # Not an error, user chose to skip
            try:
                shutil.copy(str(filepath_to_add), str(destination_path_abs))
                print(f"Copied {filepath_to_add.name} to {destination_path_abs}")
            except Exception as e:
                print(f"❌ Error copying file to {destination_path_abs}: {e}")
                return False
        else:
            print(f"File {filepath_to_add.name} is already in the managed location: {destination_path_abs}")

    elif not filepath_to_add.is_relative_to(project_root): # Must be within project if not copied
        print(f"❌ Error: File {filepath_to_add} is outside the project root {project_root} and 'synced_docs' directory does not exist. Cannot determine managed path.")
        return False


    print(f"Adding '{path_in_registry_str}' to registry...")
    entry = madio_registry.get_document_entry(registry_data, path_in_registry_str)
    if entry:
        print(f"Warning: Document '{path_in_registry_str}' already exists in registry. Updating its metadata.")
        # Fall through to update logic for existing entry if needed, or just update specific fields.

    new_entry_data = madio_registry._create_default_document_entry_fields()
    new_entry_data["source"] = args.source if args.source else "manual_add"
    new_entry_data["tier"] = args.tier if args.tier is not None else None
    new_entry_data["status"] = "local_only" # New docs start as local_only
    new_entry_data["local_sha256_hash"] = madio_registry.calculate_sha256_hash(str(destination_path_abs))
    now = datetime.datetime.utcnow().isoformat() + "Z"
    new_entry_data["created_at"] = now # Or preserve if entry existed? For --add, assume new or full overwrite.
    new_entry_data["last_modified_local_at"] = now

    madio_registry.add_or_update_document_entry(registry_data, path_in_registry_str, new_entry_data)
    return True


def remove_document(args, registry_data, project_root):
    path_in_registry_str = str(Path(args.remove).relative_to(project_root)) # Assume args.remove is relative to root

    entry = madio_registry.get_document_entry(registry_data, path_in_registry_str)
    if not entry:
        print(f"❌ Error: Document '{path_in_registry_str}' not found in registry.")
        return False

    print(f"Removing '{path_in_registry_str}' from registry...")

    # Handle Google Doc
    gdoc_id = entry.get("google_doc_id")
    if gdoc_id:
        gdoc_title = Path(path_in_registry_str).name
        # In non-interactive, default to unlink only (i.e., do not delete GDoc)
        delete_gdoc_from_drive = False
        is_interactive = sys.stdin.isatty() # Basic interactivity check

        if is_interactive:
            if get_user_confirmation(f"Associated Google Doc: '{gdoc_title}' (ID: {gdoc_id}). Delete from Google Drive? (Choosing 'N' will only unlink it)"):
                delete_gdoc_from_drive = True

        if delete_gdoc_from_drive:
            print(f"Attempting to delete Google Doc ID: {gdoc_id} from Google Drive...")
            drive_service = get_drive_service_placeholder()
            if drive_service:
                try:
                    # drive_service.files().delete(fileId=gdoc_id).execute()
                    print(f"  SUCCESS: Google Doc {gdoc_id} would be deleted (Placeholder).")
                except Exception as e: # Catch specific HttpError in real code
                    print(f"  ⚠️ FAILED to delete Google Doc {gdoc_id}: {e}. Please delete manually if needed.")
            else:
                print(f"  Drive service not available. Cannot delete GDoc. Please delete manually if needed.")
        else:
            print(f"  Google Doc {gdoc_id} will be unlinked but not deleted from Google Drive.")

    # Handle Local File
    # Convention: if path_in_registry_str points to a file inside 'synced_docs', delete it.
    # Otherwise, if it points to a file elsewhere in the project, only unregister it.
    absolute_local_path = project_root / path_in_registry_str
    synced_docs_dir = project_root / "synced_docs"

    if absolute_local_path.exists() and absolute_local_path.is_file():
        try:
            if absolute_local_path.is_relative_to(synced_docs_dir): # Only delete if it's in synced_docs
                if get_user_confirmation(f"Delete local managed file at '{absolute_local_path}'?", default_yes=False):
                    os.remove(absolute_local_path)
                    print(f"  Deleted local file: {absolute_local_path}")
                else:
                    print(f"  Local file '{absolute_local_path}' was not deleted.")
            else: # File is outside synced_docs, just unregister
                print(f"  Local file '{absolute_local_path}' is outside 'synced_docs/'. It will be unlinked from MADIO but not deleted from filesystem.")
        except Exception as e:
            print(f"  ⚠️ Error trying to delete local file {absolute_local_path}: {e}")

    madio_registry.remove_document_entry(registry_data, path_in_registry_str)
    return True

def update_metadata(args, registry_data, project_root):
    path_in_registry_str = str(Path(args.update_metadata).relative_to(project_root))

    entry = madio_registry.get_document_entry(registry_data, path_in_registry_str)
    if not entry:
        print(f"❌ Error: Document '{path_in_registry_str}' not found in registry.")
        return False

    print(f"Updating metadata for '{path_in_registry_str}'...")
    updated_fields = {}
    if args.tier is not None:
        updated_fields["tier"] = args.tier
        print(f"  Set tier to: {args.tier}")
    if args.status:
        updated_fields["status"] = args.status
        print(f"  Set status to: {args.status}")
    if args.source:
        updated_fields["source"] = args.source
        print(f"  Set source to: {args.source}")

    if not updated_fields:
        print("No metadata fields specified for update.")
        return True # Not an error, just nothing to do.

    # existing_entry = entry.copy() # No, add_or_update_document_entry handles merging
    madio_registry.add_or_update_document_entry(registry_data, path_in_registry_str, updated_fields)
    return True


def main():
    parser = argparse.ArgumentParser(description="Manage MADIO document registry entries.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--add", metavar="FILEPATH", help="Path to the local markdown file to add to the registry.")
    group.add_argument("--remove", metavar="FILEPATH_IN_REGISTRY", help="Path (relative to project root) of the document to remove from the registry.")
    group.add_argument("--update-metadata", metavar="FILEPATH_IN_REGISTRY", help="Path (relative to project root) of the document to update metadata for.")

    # Optional arguments for --add
    parser.add_argument("--tier", type=int, help="MADIO tier for the document (used with --add or --update-metadata).")
    parser.add_argument("--source", type=str, help="Source description for the document (used with --add or --update-metadata).")

    # Optional arguments for --update-metadata
    parser.add_argument("--status", type=str, help="New status for the document (used with --update-metadata).")

    args = parser.parse_args()

    project_root = madio_registry.get_project_root()
    registry_data = madio_registry.load_registry()

    success = False
    if args.add:
        success = add_document(args, registry_data, project_root)
    elif args.remove:
        success = remove_document(args, registry_data, project_root)
    elif args.update_metadata:
        if not (args.tier is not None or args.status or args.source):
            parser.error("--update-metadata requires at least one metadata flag like --tier, --status, or --source.")
        success = update_metadata(args, registry_data, project_root)

    if success:
        madio_registry.save_registry(registry_data)
        print("Registry updated successfully.")
        sys.exit(0)
    else:
        print("Operation failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
