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
                # Basic validation or version check could go here
                if not isinstance(registry_data.get("document_registry"), dict):
                    print(f"Warning: 'document_registry' key missing or not a dict in {registry_path}. Initializing fresh.")
                    return _create_empty_registry()
                if not isinstance(registry_data.get("sync_preferences"), dict):
                     print(f"Warning: 'sync_preferences' key missing or not a dict in {registry_path}. Initializing fresh.")
                     return _create_empty_registry()
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

def _create_empty_registry():
    """Helper to create a default empty registry structure."""
    return {
        "project_state": {
            "created_at": datetime.datetime.utcnow().isoformat() + "Z",
            "last_updated_at": datetime.datetime.utcnow().isoformat() + "Z",
            "document_count": 0,
            "registry_version": "1.0.0" # Semantic versioning for the registry schema
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
    # entry_data["local_path"] = str(local_path_str)

    # Initialize created_at if it's a new entry
    if str(local_path_str) not in registry_data["document_registry"]:
        entry_data["created_at"] = datetime.datetime.utcnow().isoformat() + "Z"

    # Always update last_modified_local_at when this function is called,
    # assuming it implies a change or addition that warrants it.
    # More sophisticated logic might check hashes if available.
    entry_data["last_modified_local_at"] = datetime.datetime.utcnow().isoformat() + "Z"

    registry_data["document_registry"][str(local_path_str)] = entry_data
    # print(f"Added/Updated entry for: {local_path_str}")

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
        "status": "active",
        "local_sha256_hash": "hash1",
        "last_synced_at": datetime.datetime.utcnow().isoformat() + "Z"
    }
    add_or_update_document_entry(registry, doc1_path, doc1_data)

    doc2_path = "project_instructions.md" # A root level file
    doc2_data = {
        "google_doc_id": "another_gdoc_id_456",
        "status": "local_only",
        "local_sha256_hash": "hash2",
    }
    add_or_update_document_entry(registry, doc2_path, doc2_data)

    print("\nRegistry after adding entries:")
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
