import json
import os
from pathlib import Path
import datetime

REGISTRY_DIR = ".madio"
REGISTRY_FILENAME = "document_registry.json"

def get_project_root():
    """Finds the project root by looking for the .claude directory."""
    current = Path.cwd().resolve()
    while current != current.parent:
        if (current / '.claude').is_dir():
            return current
        current = current.parent
    # Fallback if .claude is not found, though this indicates a problem
    # For safety, let's assume cwd if no .claude dir is found up the tree.
    # A more robust solution might raise an error or have a defined project marker.
    print("Warning: .claude directory not found. Assuming current directory as project root for registry.")
    return Path.cwd().resolve()

def get_registry_path():
    """Gets the absolute path to the document_registry.json file."""
    project_root = get_project_root()
    registry_dir_path = project_root / REGISTRY_DIR
    return registry_dir_path / REGISTRY_FILENAME

def load_registry():
    """Loads the document registry from .madio/document_registry.json.
    Creates an empty registry if the file doesn't exist.
    """
    registry_path = get_registry_path()
    registry_dir = registry_path.parent

    if not registry_dir.exists():
        try:
            registry_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created registry directory: {registry_dir}")
        except OSError as e:
            print(f"Error creating registry directory {registry_dir}: {e}")
            # Fallback to an in-memory empty registry if dir creation fails
            return _create_empty_registry()

    if registry_path.exists():
        try:
            with open(registry_path, 'r', encoding='utf-8') as f:
                registry_data = json.load(f)

                # --- Start: Handle potential old format and missing fields ---
                if "project_state" not in registry_data: # Very old or corrupt
                    print(f"Warning: 'project_state' missing in {registry_path}. Re-initializing.")
                    return _create_empty_registry()

                # Ensure 'document_registry' and 'sync_preferences' exist
                if "document_registry" not in registry_data or not isinstance(registry_data["document_registry"], dict):
                    registry_data["document_registry"] = {}
                    print(f"Warning: 'document_registry' was missing/invalid in {registry_path}. Initialized.")
                if "sync_preferences" not in registry_data or not isinstance(registry_data["sync_preferences"], dict):
                    registry_data["sync_preferences"] = _create_empty_registry()["sync_preferences"]
                    print(f"Warning: 'sync_preferences' was missing/invalid in {registry_path}. Initialized.")
                else: # Ensure sub-keys of sync_preferences also exist
                    default_sync_prefs = _create_empty_registry()["sync_preferences"]
                    if "google_drive_folder" not in registry_data["sync_preferences"]:
                        registry_data["sync_preferences"]["google_drive_folder"] = default_sync_prefs["google_drive_folder"]
                    if "interaction_mode" not in registry_data["sync_preferences"]:
                        registry_data["sync_preferences"]["interaction_mode"] = default_sync_prefs["interaction_mode"]


                # For each document entry, ensure all new fields exist, providing defaults if not
                updated_doc_registry = {}
                for local_path, entry in registry_data.get("document_registry", {}).items():
                    default_fields = _create_default_document_entry_fields()
                    # If loaded entry is from Phase 1, it might only have a few fields.
                    # We merge default_fields with entry, where entry's values take precedence.
                    # `created_at` and `last_modified_local_at` should be preserved if they exist.

                    # Preserve critical existing values before defaulting
                    preserved_values = {}
                    for key_to_preserve in ["google_doc_id", "status", "created_at", "last_synced_at", "last_modified_local_at", "source"]:
                        if key_to_preserve in entry:
                            preserved_values[key_to_preserve] = entry[key_to_preserve]

                    # Start with defaults, then overlay existing entry, then re-overlay preserved critical values
                    # This ensures that if a field was None in preserved_values (e.g. google_doc_id), it stays None
                    # rather than getting a default from _create_default_document_entry_fields if entry didn't have it.
                    # However, _create_default_document_entry_fields already sets many to None.
                    # Simpler: defaults, then existing entry.

                    merged_entry = {**default_fields, **entry} # entry's values overwrite defaults

                    # Specific handling for created_at: if entry had it, use it, else default_fields already set it.
                    if "created_at" in entry:
                         merged_entry["created_at"] = entry["created_at"]

                    updated_doc_registry[local_path] = merged_entry

                registry_data["document_registry"] = updated_doc_registry
                # --- End: Handle potential old format ---

                return registry_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from {registry_path}: {e}. Initializing fresh registry.")
            return _create_empty_registry()
        except Exception as e:
            print(f"Unexpected error loading registry {registry_path}: {e}. Initializing fresh registry.")
            return _create_empty_registry()
    else:
        print(f"Registry file not found at {registry_path}. Creating new one.")
        new_registry = _create_empty_registry()
        save_registry(new_registry) # Save the newly created empty registry
        return new_registry

def _create_default_document_entry_fields():
    """Provides default values for a new document entry's extended fields."""
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return {
        "tier": None, # int
        "created_at": now,
        "last_modified_local_at": now,
        "last_synced_at": None, # timestamp
        "local_sha256_hash": None, # string
        "google_doc_id": None, # string
        "google_doc_version": None, # string (e.g. headRevisionId)
        "google_doc_last_known_good_at": None, # timestamp
        "status": "new", # string: e.g., new, active, local_only, orphaned_gdoc, conflict, error_local_missing etc.
        "source": "unknown", # string: e.g., import, generated, manual_add, migrated
        "dependencies": [] # list of strings (local_paths)
    }

def _create_empty_registry():
    """Helper to create a default empty registry structure."""
    now = datetime.datetime.utcnow().isoformat() + "Z"
    return {
        "project_state": {
            "created_at": now,
            "last_updated_at": now,
            "document_count": 0,
            "registry_version": "1.1.0" # Updated version for Phase 2 structure
        },
        "document_registry": {}, # Stores entries keyed by local_path relative to project root
        "sync_preferences": {
            "google_drive_folder": {
                "name": "", # e.g., "MADIO Documents"
                "id": ""    # Google Drive Folder ID
            },
            "interaction_mode": "interactive" # Or "auto", "non_interactive"
        }
    }

def save_registry(registry_data):
    """Saves the registry data to .madio/document_registry.json."""
    registry_path = get_registry_path()
    registry_dir = registry_path.parent

    if not registry_dir.exists():
        try:
            registry_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"Error: Could not create directory for registry at {registry_dir}: {e}")
            return False # Indicate save failure

    # Update last_updated timestamp and document_count
    if "project_state" in registry_data:
        registry_data["project_state"]["last_updated_at"] = datetime.datetime.utcnow().isoformat() + "Z"
        registry_data["project_state"]["document_count"] = len(registry_data.get("document_registry", {}))
    else: # Should not happen if _create_empty_registry is used
        print("Warning: project_state missing from registry data during save.")


    try:
        with open(registry_path, 'w', encoding='utf-8') as f:
            json.dump(registry_data, f, indent=2, ensure_ascii=False)
        # print(f"Registry saved successfully to {registry_path}")
        return True
    except IOError as e:
        print(f"Error writing registry to {registry_path}: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error saving registry {registry_path}: {e}")
        return False

def get_document_entry(registry_data, local_path_str):
    """Retrieves a document entry by its local_path (relative to project root)."""
    return registry_data.get("document_registry", {}).get(str(local_path_str))

def add_or_update_document_entry(registry_data, local_path_str, entry_data):
    """Adds or updates a document entry.
    local_path_str should be relative to the project root.
    entry_data is a dict with fields like google_doc_id, status, etc.
    """
    # Ensure local_path is part of the entry_data for completeness if needed later
    # entry_data["local_path"] = str(local_path_str) # Key is already the local_path_str

    path_key = str(local_path_str)
    existing_entry = registry_data["document_registry"].get(path_key)

    if existing_entry:
        # Update existing: overlay new data onto existing, preserving fields not in entry_data
        updated_entry = {**existing_entry, **entry_data}
        # Ensure last_modified_local_at is updated if significant data changed
        # For now, always update it on this call, or rely on caller to set it in entry_data.
        if "last_modified_local_at" not in entry_data: # If caller didn't specify, set it
            updated_entry["last_modified_local_at"] = datetime.datetime.utcnow().isoformat() + "Z"
        registry_data["document_registry"][path_key] = updated_entry
    else:
        # New entry: start with defaults, then overlay provided entry_data
        new_entry = _create_default_document_entry_fields()
        new_entry = {**new_entry, **entry_data}
        # created_at and last_modified_local_at are set by _create_default_document_entry_fields initially
        # If entry_data provides them, they will overwrite.
        if "created_at" not in entry_data: # If not explicitly provided, ensure it's set by default
             new_entry["created_at"] = _create_default_document_entry_fields()["created_at"]
        if "last_modified_local_at" not in entry_data:
             new_entry["last_modified_local_at"] = _create_default_document_entry_fields()["last_modified_local_at"]

        registry_data["document_registry"][path_key] = new_entry

    # print(f"Added/Updated entry for: {path_key}")

def remove_document_entry(registry_data, local_path_str):
    """Removes a document entry by its local_path."""
    if str(local_path_str) in registry_data.get("document_registry", {}):
        del registry_data["document_registry"][str(local_path_str)]
        # print(f"Removed entry for: {local_path_str}")
        return True
    return False

def get_sync_preferences(registry_data):
    """Retrieves the sync_preferences part of the registry."""
    return registry_data.get("sync_preferences", _create_empty_registry()["sync_preferences"])

def update_sync_preferences(registry_data, prefs_data):
    """Updates the sync_preferences part of the registry."""
    registry_data["sync_preferences"] = prefs_data
    # print("Sync preferences updated.")

if __name__ == '__main__':
    # Example Usage & Basic Test
    print(f"Project root determined as: {get_project_root()}")
    reg_path = get_registry_path()
    print(f"Registry path is: {reg_path}")

    # Test loading (will create if not exists)
    registry = load_registry()
    print("\nInitial or Loaded Registry:")
    print(json.dumps(registry, indent=2))

    # Test adding an entry
    doc1_path = "docs/test_document_1.md"
    doc1_data = {
        "google_doc_id": "dummy_gdoc_id_123",
        "status": "active", # Will be part of the merged entry
        "local_sha256_hash": "hash1_updated", # Example of providing some fields
        "last_synced_at": datetime.datetime.utcnow().isoformat() + "Z",
        "tier": 1,
        "source": "manual_test"
        # created_at and last_modified_local_at will be set by add_or_update or defaults
    }
    add_or_update_document_entry(registry, doc1_path, doc1_data)

    doc2_path = "project_instructions.md" # A root level file
    # For doc2, let's provide fewer fields to see defaults take effect
    doc2_data = {
        "google_doc_id": "another_gdoc_id_456",
        "status": "local_only"
        # Other fields will use defaults from _create_default_document_entry_fields
        # or be updated by add_or_update_document_entry
    }
    add_or_update_document_entry(registry, doc2_path, doc2_data)

    print("\nRegistry after adding/updating entries:")
    print(json.dumps(registry["document_registry"], indent=2))

    # Test saving
    if save_registry(registry):
        print("\nRegistry saved.")
        # Test loading again
        reloaded_registry = load_registry()
        print("\nReloaded Registry:")
        print(json.dumps(reloaded_registry, indent=2))

        entry = get_document_entry(reloaded_registry, doc1_path)
        print(f"\nRetrieved entry for {doc1_path}: {entry}")

        # Test updating sync preferences
        prefs = get_sync_preferences(reloaded_registry)
        prefs["google_drive_folder"]["name"] = "My MADIO Test Docs"
        prefs["google_drive_folder"]["id"] = "folder_id_xyz"
        update_sync_preferences(reloaded_registry, prefs)
        save_registry(reloaded_registry)
        print("\nReloaded Registry after pref update:")
        print(json.dumps(load_registry(), indent=2))


        # Test removing an entry
        # remove_document_entry(reloaded_registry, doc1_path)
        # print("\nRegistry after removing an entry:")
        # print(json.dumps(reloaded_registry["document_registry"], indent=2))
        # save_registry(reloaded_registry)

    else:
        print("\nFailed to save registry.")

    # Clean up test file
    # if reg_path.exists():
    #     os.remove(reg_path)
    #     print(f"\nCleaned up test registry file: {reg_path}")
    # if reg_path.parent.exists() and not any(reg_path.parent.iterdir()): # if .madio is empty
    #     os.rmdir(reg_path.parent)
    #     print(f"Cleaned up test registry directory: {reg_path.parent}")

def calculate_sha256_hash(filepath):
    """Calculates the SHA256 hash of a file."""
    import hashlib
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        # print(f"Warning: File not found for hashing: {filepath}")
        return None
    except Exception as e:
        # print(f"Error hashing file {filepath}: {e}")
        return None
