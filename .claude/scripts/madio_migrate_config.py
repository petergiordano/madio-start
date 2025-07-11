import json
import os
import datetime
from pathlib import Path

# Assuming madio_registry.py is in the same directory or PYTHONPATH
try:
    from . import madio_registry
    from .madio_registry import calculate_sha256_hash # Added this import
except ImportError:
    import madio_registry
    from madio_registry import calculate_sha256_hash # Added this import

# Define this constant locally, as it's specific to how old configs marked it.
NEW_DOC_PLACEHOLDER = "CREATE_NEW_DOCUMENT"

# Old config file paths (relative to project root for consistency)
OLD_SYNC_CONFIG_PATH_REL = ".claude/scripts/sync_config.json"
OLD_DIR_MAPPING_PATH_REL = ".synced_docs_mapping.json" # Usually in project root

def migrate_configurations():
    """
    Migrates old sync configurations (.claude/scripts/sync_config.json and .synced_docs_mapping.json)
    to the new .madio/document_registry.json format.
    """
    project_root = madio_registry.get_project_root()
    print(f"Starting migration for project at: {project_root}")

    old_sync_config_path = project_root / OLD_SYNC_CONFIG_PATH_REL
    old_dir_mapping_path = project_root / OLD_DIR_MAPPING_PATH_REL

    # Load or create a new registry
    # load_registry will create one if it doesn't exist, but we want to ensure we're starting fresh
 убий # for migration unless we decide to merge into an existing new registry.
    # For now, let's assume migration creates a new one or overwrites a basic new one.
    print("Loading/initializing new document registry...")
    new_registry = madio_registry._create_empty_registry() # Start with a clean slate for migration content

    migrated_entries_count = 0
    folder_pref_migrated = False

    # 1. Process old .claude/scripts/sync_config.json
    if old_sync_config_path.exists():
        print(f"Found old sync_config.json at: {old_sync_config_path}")
        try:
            with open(old_sync_config_path, 'r', encoding='utf-8') as f:
                old_sync_config = json.load(f)

            # Migrate folder preference
            old_folder_pref = old_sync_config.get("_google_drive_folder", {})
            if old_folder_pref.get("id") or old_folder_pref.get("name"):
                new_sync_prefs = madio_registry.get_sync_preferences(new_registry)
                new_sync_prefs["google_drive_folder"]["name"] = old_folder_pref.get("name", "")
                new_sync_prefs["google_drive_folder"]["id"] = old_folder_pref.get("id", "")
                madio_registry.update_sync_preferences(new_registry, new_sync_prefs)
                print(f"  Migrated folder preference: Name='{old_folder_pref.get('name', '')}', ID='{old_folder_pref.get('id', '')}'")
                folder_pref_migrated = True

            # Migrate file entries
            for rel_path_from_scripts_dir, doc_id_or_placeholder in old_sync_config.items():
                if rel_path_from_scripts_dir.startswith("_"): # Skip comments like _comment
                    continue

                # Convert path to be relative to project root
                # old paths were like "../../project_system_instructions.md"
                # Path(OLD_SYNC_CONFIG_PATH_REL).parent gives .claude/scripts
                # Then resolve `rel_path_from_scripts_dir` from there
                abs_path = (project_root / OLD_SYNC_CONFIG_PATH_REL).parent / rel_path_from_scripts_dir
                try:
                    path_from_root = str(abs_path.resolve().relative_to(project_root.resolve()))
                except ValueError:
                    print(f"  Warning: Path {rel_path_from_scripts_dir} in old sync_config.json seems to be outside project root. Skipping.")
                    continue

                # Initialize with defaults, then overlay specific migrated data
                entry_data = madio_registry._create_default_document_entry_fields()
                entry_data["google_doc_id"] = doc_id_or_placeholder if doc_id_or_placeholder != NEW_DOC_PLACEHOLDER else None
                entry_data["status"] = "migrated_placeholder" if doc_id_or_placeholder == NEW_DOC_PLACEHOLDER else "migrated"
                entry_data["source"] = "migrated_sync_config"
                # For migrated entries, created_at and last_modified_local_at are effectively the migration time
                migration_time = datetime.datetime.utcnow().isoformat() + "Z"
                entry_data["created_at"] = migration_time
                entry_data["last_modified_local_at"] = migration_time

                # Calculate hash if local file exists
                abs_file_path_for_hash = project_root / path_from_root
                if abs_file_path_for_hash.exists():
                    entry_data["local_sha256_hash"] = madio_registry.calculate_sha256_hash(str(abs_file_path_for_hash))
                else:
                    entry_data["local_sha256_hash"] = None # Or some indicator it was missing at migration

                madio_registry.add_or_update_document_entry(new_registry, path_from_root, entry_data)
                migrated_entries_count +=1
                print(f"  Migrated entry from sync_config: {path_from_root} -> GDocID/Placeholder: {doc_id_or_placeholder}")

        except Exception as e:
            print(f"  Error processing old sync_config.json: {e}")
    else:
        print(f"Old sync_config.json not found at: {old_sync_config_path}")

    # 2. Process old .synced_docs_mapping.json (directory mode mapping)
    # These paths are typically already relative to project root.
    if old_dir_mapping_path.exists():
        print(f"Found old .synced_docs_mapping.json at: {old_dir_mapping_path}")
        try:
            with open(old_dir_mapping_path, 'r', encoding='utf-8') as f:
                old_dir_mapping = json.load(f)

            for path_from_root, doc_id_or_placeholder in old_dir_mapping.items():
                # These paths should already be relative to project root
                # Initialize with defaults, then overlay specific migrated data
                entry_data = madio_registry._create_default_document_entry_fields()
                entry_data["google_doc_id"] = doc_id_or_placeholder if doc_id_or_placeholder != NEW_DOC_PLACEHOLDER else None
                entry_data["status"] = "migrated_placeholder" if doc_id_or_placeholder == NEW_DOC_PLACEHOLDER else "migrated"
                entry_data["source"] = "migrated_dir_mapping"
                migration_time = datetime.datetime.utcnow().isoformat() + "Z"
                entry_data["created_at"] = migration_time # Or try to preserve if it existed in a very old format? No, migration is new creation event for this registry.
                entry_data["last_modified_local_at"] = migration_time

                abs_file_path_for_hash = project_root / path_from_root
                if abs_file_path_for_hash.exists():
                    entry_data["local_sha256_hash"] = madio_registry.calculate_sha256_hash(str(abs_file_path_for_hash))
                else:
                    entry_data["local_sha256_hash"] = None

                # Add/Update, .synced_docs_mapping entries often more specific/correct for GDoc IDs
                # if they came from directory sync which auto-updated them.
                madio_registry.add_or_update_document_entry(new_registry, path_from_root, entry_data)

                # Check if this path was already added from old_sync_config to avoid double counting
                # add_or_update_document_entry handles the merging, so we just need to adjust count
                # This logic for migrated_entries_count might be slightly off if paths are identical and overwritten.
                # The final count `len(new_registry['document_registry'])` is more accurate.
                # For simplicity, let's assume this count is indicative of files processed from this source.
                # A better way: check if it was a truly new key added to new_registry['document_registry'].
                # However, add_or_update_document_entry doesn't return that.
                # Let's rely on the final len() for accuracy of total unique.
                # migrated_entries_count +=1 # This simple increment is fine for "processed from this source".

                print(f"  Migrated/Updated entry from .synced_docs_mapping: {path_from_root} -> GDocID/Placeholder: {doc_id_or_placeholder}")

        except Exception as e:
            print(f"  Error processing old .synced_docs_mapping.json: {e}")
    else:
        print(f"Old .synced_docs_mapping.json not found at: {old_dir_mapping_path}")


    # Finalize and save the new registry
    if migrated_entries_count > 0 or folder_pref_migrated:
        print(f"\nTotal unique entries migrated: {len(new_registry['document_registry'])}") # Use length of dict
        print("Saving new document_registry.json...")
        if madio_registry.save_registry(new_registry):
            print("Migration successful! New registry saved.")
            print(f"  Path: {madio_registry.get_registry_path()}")
            print("\nPlease review the new .madio/document_registry.json file.")
            print("You can now use commands that rely on the new registry (e.g., /push-to-docs).")
            print("It's recommended to backup or rename your old config files after verifying the migration.")
        else:
            print("Migration failed to save the new registry. Please check errors above.")
    else:
        print("\nNo old configuration files found or no data to migrate.")
        # Save an empty registry if none existed before, so project is initialized.
        if not madio_registry.get_registry_path().exists():
            madio_registry.save_registry(new_registry)
            print("Initialized an empty document registry as no old configs were found.")


if __name__ == "__main__":
    print("MADIO Configuration Migration Utility")
    print("-------------------------------------")
    print("This script will attempt to migrate old MADIO sync configurations")
    print("(e.g., .claude/scripts/sync_config.json, .synced_docs_mapping.json)")
    print("to the new .madio/document_registry.json format.")
    print("\nIMPORTANT:")
    print("- If an existing .madio/document_registry.json is found, this script will")
    print("  effectively create a new one based on OLD formats. It does NOT merge.")
    print("  If you ran this previously, re-running might overwrite your new registry.")
    print("- It is STRONGLY recommended to backup your project, especially any existing")
    print("  .madio/document_registry.json and old config files, before proceeding.")

    confirm = input("\nContinue with migration? (y/N): ").strip().lower()
    if confirm == 'y':
        migrate_configurations()
    else:
        print("Migration cancelled by user.")

# TODO: The /madio-migrate-config command definition .md file was already created in Phase 1.
# This script is the backend for it.
