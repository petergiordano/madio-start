import argparse
import json
import os
import sys
import datetime
from pathlib import Path

try:
    from . import madio_registry
    from .madio_registry import calculate_sha256_hash
    # To access Drive API for checking GDocs and potentially deleting them in --repair
    from .sync_to_docs import GoogleDocsSync
except ImportError:
    import madio_registry
    from madio_registry import calculate_sha256_hash
    from sync_to_docs import GoogleDocsSync


# --- Start: Duplicated/Adapted Interactive Prompt Logic (Marked for Refactor) ---
# This section duplicates/adapts logic from sync_to_docs.py for handling stale mappings.
# TODO: Refactor this into a shared module (e.g., madio_interactive.py or similar)
def prompt_resolve_local_missing(local_path_str, entry_data, doc_registry_map, drive_service_wrapper, is_interactive):
    """Handles interactive resolution for a missing local file."""
    if not is_interactive:
        print(f"  Skipping {local_path_str} (non-interactive, local file missing).")
        return False # Indicates no change that requires saving immediately by this function

    print(f"❓ Stale Registry: Local file '{local_path_str}' is missing.")
    choice = input("   Options: (R)emove from registry, (U)nlink GDoc & Remove from Registry, (S)kip this time, (A)bort? [S]: ").strip().lower()

    if choice == 'r':
        print(f"   Action: Removing '{local_path_str}' from registry.")
        if local_path_str in doc_registry_map:
            del doc_registry_map[local_path_str]
        return True # Registry changed
    elif choice == 'u':
        gdoc_id = entry_data.get("google_doc_id")
        print(f"   Action: Unlinking GDoc (if any) and removing '{local_path_str}' from registry.")
        if gdoc_id:
            print(f"   Note: Associated GDoc ID was {gdoc_id}. It will NOT be deleted from Drive by this action.")
        if local_path_str in doc_registry_map:
            del doc_registry_map[local_path_str]
        return True # Registry changed
    elif choice == 'a':
        print("   Repair aborted by user.")
        sys.exit(1)
    else: # Default 's' (skip)
        print(f"   Action: Skipping resolution for '{local_path_str}' this time.")
        return False

def prompt_resolve_gdoc_inaccessible(local_path_str, entry_data, doc_registry_map, issue_type, drive_service_wrapper, is_interactive):
    """Handles interactive resolution for inaccessible GDoc (trashed or not_found)."""
    gdoc_id = entry_data.get("google_doc_id")
    issue_desc = "in trash" if issue_type == "trashed" else "not found (404)"

    if not is_interactive:
        print(f"  Unlinking GDoc for {local_path_str} (non-interactive, GDoc {issue_desc}).")
        entry_data["google_doc_id"] = None
        entry_data["google_doc_version"] = None
        entry_data["google_doc_last_known_good_at"] = None
        entry_data["status"] = f"local_only_gdoc_{issue_type}"
        return True # Registry changed

    print(f"❓ Stale Registry: Google Doc for '{local_path_str}' (ID: {gdoc_id}) is {issue_desc}.")
    choice = input("   Options: (C)reate new GDoc & link, (U)nlink (mark local as 'local_only'), (S)kip, (A)bort? [S]: ").strip().lower()

    if choice == 'c':
        print(f"   Action: Marking '{local_path_str}' to create a new GDoc on next sync.")
        entry_data["google_doc_id"] = None # Will be picked by sync_to_docs for creation
        entry_data["google_doc_version"] = None
        entry_data["google_doc_last_known_good_at"] = None
        entry_data["status"] = "local_only_needs_gdoc_creation" # New status
        return True
    elif choice == 'u':
        print(f"   Action: Unlinking GDoc for '{local_path_str}'. Local file kept.")
        entry_data["google_doc_id"] = None
        entry_data["google_doc_version"] = None
        entry_data["google_doc_last_known_good_at"] = None
        entry_data["status"] = "local_only"
        return True
    elif choice == 'a':
        print("   Repair aborted by user.")
        sys.exit(1)
    else: # Skip
        print(f"   Action: Skipping resolution for '{local_path_str}' this time.")
        # Status remains as error_gdoc_trashed or error_gdoc_not_found
        return False
# --- End: Duplicated/Adapted Interactive Prompt Logic ---


def perform_health_check(registry_data, project_root, drive_service_wrapper, repair_mode=False, is_interactive=True):
    print("\n--- Health Check Report ---")
    doc_registry_map = registry_data.get("document_registry", {})
    if not doc_registry_map:
        print("Document registry is empty. Nothing to check.")
        return True

    stats = {
        "total": len(doc_registry_map), "synced": 0, "local_changed": 0,
        "remote_changed": 0, "conflict": 0, "errors": 0, "local_missing": 0,
        "gdoc_inaccessible": 0
    }
    registry_changed_by_repair = False

    for local_path_str, entry in doc_registry_map.items():
        print(f"\nChecking: {local_path_str}")
        current_status = entry.get("status", "unknown")
        error_found = False
        absolute_local_path = project_root / local_path_str

        # 1. Check local file
        if not absolute_local_path.exists():
            print(f"  ❌ Local file MISSING: {absolute_local_path}")
            stats["local_missing"] += 1
            error_found = True
            entry["status"] = "error_local_missing" # Update status directly
            if repair_mode:
                if prompt_resolve_local_missing(local_path_str, entry, doc_registry_map, drive_service_wrapper, is_interactive):
                    registry_changed_by_repair = True
                if local_path_str not in doc_registry_map : # Entry was deleted from map by prompt
                    continue # move to next item in the main loop
            # If not repair mode, or repair mode skipped, status remains error_local_missing
            # No further checks if local file is missing for this entry
            continue


        current_hash = calculate_sha256_hash(str(absolute_local_path))
        stored_hash = entry.get("local_sha256_hash")
        local_changed = current_hash != stored_hash
        if local_changed:
            print(f"  ⚠️ Local file CHANGED (Hash: {current_hash[:7]}... vs stored {str(stored_hash)[:7]}...)")
            stats["local_changed"] += 1
            # In repair mode, could offer to update hash if user confirms it's the new baseline
            if repair_mode and is_interactive and local_changed : # Only prompt if actually changed
                 if input(f"    Local file '{local_path_str}' has changed. Update hash in registry to match current file content? (y/N): ").strip().lower() == 'y':
                    entry["local_sha256_hash"] = current_hash
                    entry["last_modified_local_at"] = datetime.datetime.utcnow().isoformat() + "Z"
                    entry["status"] = "active_local_hash_updated" # New status
                    print("    Action: Local hash and last_modified_local_at updated in registry.")
                    registry_changed_by_repair = True
                    local_changed = False # Considered resolved for this check's purpose.
                 else:
                    print("    Action: Stored local hash NOT updated.")


        # 2. Check Google Doc
        gdoc_id = entry.get("google_doc_id")
        remote_changed = False # Reset for each entry
        if gdoc_id:
            try:
                # Ensure fields includes what's needed by prompt_resolve_gdoc_inaccessible if refactored
                gdoc_meta = drive_service_wrapper.drive_service.files().get(fileId=gdoc_id, fields="id, name, trashed, version, headRevisionId, modifiedTime").execute()
                live_gdoc_version = gdoc_meta.get("headRevisionId") or gdoc_meta.get("version")
                stored_gdoc_version = entry.get("google_doc_version") # This is version from last sync

                if gdoc_meta.get("trashed"):
                    print(f"  ❌ Stale Registry: Google Doc for '{local_path_str}' (ID: {gdoc_id}) is TRASHED on Google Drive.")
                    stats["gdoc_inaccessible"] += 1
                    error_found = True
                    entry["status"] = "error_gdoc_trashed"
                    if repair_mode:
                         if prompt_resolve_gdoc_inaccessible(local_path_str, entry, doc_registry_map, "trashed", drive_service_wrapper, is_interactive):
                             registry_changed_by_repair = True
                    # if repair unlinked or marked for creation, gdoc_id might be None now
                    if not entry.get("google_doc_id"): continue

                elif live_gdoc_version != stored_gdoc_version:
                    print(f"  ⚠️ Google Doc CHANGED (Version: {live_gdoc_version} vs stored {stored_gdoc_version})")
                    stats["remote_changed"] += 1
                    remote_changed = True # Mark that we detected a remote change
                    if repair_mode and is_interactive:
                        if input(f"    Google Doc for '{local_path_str}' has changed remotely (Live version: {live_gdoc_version}, Stored: {stored_gdoc_version}). Update registry to acknowledge live version? (y/N): ").strip().lower() == 'y':
                            entry["google_doc_version"] = live_gdoc_version
                            entry["google_doc_last_known_good_at"] = gdoc_meta.get("modifiedTime") or datetime.datetime.utcnow().isoformat() + "Z"
                            entry["status"] = "active_gdoc_version_updated" # New status
                            print("    Action: Stored Google Doc version updated in registry.")
                            registry_changed_by_repair = True
                            remote_changed = False # Considered resolved for this check for this run
                        else:
                            print("    Action: Stored Google Doc version NOT updated.")
                else: # Versions match
                    print(f"  ✅ Google Doc OK (ID: {gdoc_id}, Version: {live_gdoc_version})")
                    # Update last known good time if it was accessible and version matches
                    entry["google_doc_last_known_good_at"] = gdoc_meta.get("modifiedTime") or datetime.datetime.utcnow().isoformat() + "Z"


            except HttpError as e:
                if e.resp.status == 404:
                    print(f"  ❌ Google Doc NOT FOUND (404) (ID: {gdoc_id})")
                    stats["gdoc_inaccessible"] += 1
                    error_found = True
                    entry["status"] = "error_gdoc_not_found"
                    if repair_mode:
                        if prompt_resolve_gdoc_inaccessible(local_path_str, entry, doc_registry_map, "not_found", drive_service_wrapper, is_interactive):
                            registry_changed_by_repair = True
                    if not entry.get("google_doc_id"): continue
                else:
                    print(f"  ❌ Error accessing Google Doc (ID: {gdoc_id}): {e}")
                    stats["errors"] +=1
                    error_found = True
                    entry["status"] = "error_gdoc_api_error"
        elif not gdoc_id and entry.get("status") not in ["local_only", "new", "local_only_needs_gdoc_creation"]:
            print(f"  ℹ️  No Google Doc linked.") # This is fine if status is local_only or new
            if entry.get("status") == "active": # Should have a gdoc_id if active
                entry["status"] = "local_only" # Correct status
                registry_changed_by_repair = True


        # Determine overall status for summary
        if not error_found:
            if local_changed and remote_changed:
                print(f"  🔥 CONFLICT: Local and Remote changes detected.")
                stats["conflict"] += 1
                entry["status"] = "conflict" # TODO: In repair, prompt for conflict resolution
                if repair_mode:
                    # Placeholder for conflict resolution prompt from PRD.
                    # For now, repair mode doesn't resolve content conflicts here.
                    print("    Conflict resolution not yet implemented in --repair. Suggest manual review or /push-to-docs for its conflict handling.")
            elif not local_changed and not remote_changed:
                if entry.get("status") not in ["active", "migrated"]: # If previously had error but now ok
                     entry["status"] = "active" # Mark as active if all checks pass now
                     registry_changed_by_repair = True
                stats["synced"] +=1
            # local_changed or remote_changed already incremented their specific counters
        else: # error_found is true
            stats["errors"] +=1 # General error counter

        # Update entry in the map if status was changed by logic here
        doc_registry_map[local_path_str] = entry


    print("\n--- Summary ---")
    print(f"Total documents in registry: {stats['total']}")
    print(f"Synced (no changes):         {stats['synced']}")
    print(f"Local changes pending sync:  {stats['local_changed']}")
    print(f"Remote GDoc changes:         {stats['remote_changed']}")
    print(f"Conflicts (local & remote):  {stats['conflict']}")
    print(f"Local files missing:         {stats['local_missing']}")
    print(f"Google Docs inaccessible:    {stats['gdoc_inaccessible']}")
    print(f"Other errors:                {stats['errors']}")

    if repair_mode and registry_changed_by_repair:
        print("\nSaving updated registry after repairs...")
        madio_registry.save_registry(registry_data)
        print("Registry saved.")
    elif repair_mode and not registry_changed_by_repair:
        print("\nNo registry changes made during repair.")

    return stats["errors"] == 0 and stats["local_missing"] == 0 and stats["gdoc_inaccessible"] == 0


def main():
    parser = argparse.ArgumentParser(description="Check MADIO sync status and health.")
    parser.add_argument("--repair", action="store_true", help="Attempt to interactively repair issues found.")
    # --health-check is the default, so no explicit arg needed unless we add other modes.
    # For clarity, can add it:
    parser.add_argument("--health-check", action="store_true", help="Perform health check (default action).")

    args = parser.parse_args()

    is_interactive_session = sys.stdin.isatty()
    if args.repair and not is_interactive_session:
        print("Warning: --repair typically requires an interactive session for choices. Proceeding with non-interactive defaults for repairs where possible (usually 'skip' or 'unlink').")
        # Some repair actions might not be possible or safe non-interactively.

    project_root = madio_registry.get_project_root()
    registry_data = madio_registry.load_registry()

    # Initialize GoogleDocsSync to get drive_service for GDoc checks/operations
    # This reuses auth from sync_to_docs.py. Consider a shared auth module later.
    drive_service_wrapper = None
    try:
        # Pass minimal args to GoogleDocsSync for it to init
        sync_args_for_auth = argparse.Namespace(credentials='credentials.json', token='token.pickle', interactive_session=is_interactive_session)
        drive_service_wrapper = GoogleDocsSync(sync_args_for_auth.credentials, sync_args_for_auth.token)
        drive_service_wrapper.set_cli_args(sync_args_for_auth) # For internal use if any method in it needs cli_args
        drive_service_wrapper.authenticate() # Authenticates and sets up drive_service
        if not drive_service_wrapper.drive_service:
            print("❌ Failed to initialize Google Drive service. Cannot perform GDoc checks.")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error initializing Google Drive service: {e}")
        sys.exit(1)

    all_ok = perform_health_check(registry_data, project_root, drive_service_wrapper,
                                  repair_mode=args.repair, is_interactive=is_interactive_session)

    if all_ok and not args.repair :
        print("\nHealth check passed. All entries appear consistent.")
    elif not all_ok and not args.repair:
        print("\nHealth check found issues. Run with --repair to attempt fixes.")

if __name__ == "__main__":
    main()
