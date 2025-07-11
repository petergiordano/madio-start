# Product Requirements Document: MADIO Iterative Development Framework

## Executive Summary

The MADIO Framework currently operates under a "one-time setup" model that assumes users create AI system documents once and deploy them. Real-world usage patterns reveal that users require iterative development capabilities - the ability to continuously add, replace, update, and refine their AI system documents throughout the project lifecycle. Additionally, critical user interaction features like Google Drive folder selection are being bypassed, degrading the user experience. This PRD outlines the structural changes needed to transform MADIO from a static setup tool into a dynamic development framework with proper user interaction flows.

## Problem Statement

### Current State Limitations

- **Single Document Lifecycle**: System assumes documents are created once via `/generate-ai-system` or `/madio-import-docs`
- **Stale Mapping Persistence**: Document-to-Google Doc ID mappings persist indefinitely, causing sync failures when documents are replaced
- **No Lifecycle Management**: No tracking of document creation, modification, or replacement events
- **Poor User Experience**: Users encounter cryptic errors when attempting iterative workflows
- **Brittle Sync Process**: The current Google Docs sync process (`sync_to_docs.py`) lacks pre-sync validation. It may attempt to operate on stale document IDs (from `sync_config.json` or `.synced_docs_mapping.json`) if Google Docs have been trashed or deleted, leading to HTTP errors during the API calls. It also doesn't detect if local files listed in mappings are missing before attempting to read them.
- **Missing User Interaction**: The Google Drive folder selection prompt in `sync_to_docs.py` relies on `sys.stdin.isatty()` to detect interactive terminals. The `push-to-docs` bash command, when executed from environments like the Claude Code CLI, is detected as non-interactive. This causes the folder prompt to be skipped, and documents default to the Google Drive root folder without user choice. While a `--folder` argument exists as a workaround, the interactive experience is broken in these common environments.

### Impact on User Workflows

1. **Initial Setup → Development Iteration**: Users complete setup, then need to add new specialized documents
2. **Document Replacement**: Users want to replace existing documents with improved versions
3. **Template Evolution**: Users need to upgrade to newer MADIO template versions
4. **Collaborative Development**: Multiple team members contribute documents that need integration
5. **Experimentation**: Users want to test different document combinations without breaking existing setups
6. **Document Organization**: Users cannot organize their Google Docs into proper folders, leading to cluttered Drive structure

## Vision Statement

Enable MADIO users to continuously evolve their AI systems through seamless iterative development workflows, treating AI system documents as living assets that can be created, modified, replaced, and refined throughout the project lifecycle, with full control over document organization and sync preferences.

## Key User Stories

### Epic 1: Document Lifecycle Management

**As a MADIO user, I want to manage my AI system documents as living assets so that I can continuously improve my AI system.**

- **Story 1.1**: Add new documents to existing project without breaking sync
- **Story 1.2**: Replace existing documents with new versions (local file update should reflect in the linked Google Doc).
- **Story 1.3**: Remove documents that are no longer needed (user should be prompted whether to also delete/archive the corresponding Google Doc or just remove the mapping).
- **Story 1.4**: Track document history (local changes, sync events) and changes in the document registry.

### Epic 2: Iterative Import Workflows

**As a MADIO user, I want to bring new AI system documents into my project at any time so that I can expand my AI system capabilities.**

- **Story 2.1**: Import additional documents after initial setup
- **Story 2.2**: Replace all documents with a new set
- **Story 2.3**: Merge new documents with existing ones
- **Story 2.4**: Preview import changes before applying

### Epic 3: Robust Sync Management

**As a MADIO user, I want reliable Google Docs sync that adapts to my document changes so that my deployed AI system stays current.**

- **Story 3.1**: Automatically detect and resolve stale Google Doc mappings
- **Story 3.2**: Create new Google Docs when needed without manual intervention
- **Story 3.3**: Preserve working document mappings during updates
- **Story 3.4**: Recover from sync failures gracefully

### Epic 4: Interactive User Experience

**As a MADIO user, I want to control where my documents are organized and how sync operations proceed so that I can maintain an organized workspace.**

- **Story 4.1**: Choose Google Drive folder for document organization during sync
- **Story 4.2**: Receive clear prompts and confirmations during critical operations
- **Story 4.3**: Override default behaviors when needed
- **Story 4.4**: Understand what the system is doing through clear status messages

### Epic 5: Development Workflow Integration

**As a MADIO user, I want development workflows that match my iterative process so that I can work efficiently.**

- **Story 5.1**: Generate new documents and integrate them seamlessly
- **Story 5.2**: Update existing documents while preserving relationships
- **Story 5.3**: Validate document consistency after changes
- **Story 5.4**: Deploy changes incrementally

## Technical Requirements

### Core Architecture Changes

#### 1. Document Lifecycle State Management

```json
{
  "project_state": {
    "created": "2025-07-10T16:50:27Z",
    "last_updated": "2025-07-10T17:01:35Z",
    "document_count": 10,
    "sync_status": "active",
    "registry_version": "1.0"
  },
  "document_registry": {
    "project_system_instructions.md": {
      "local_path": "project_system_instructions.md", // Relative to project root
      "tier": 1,
      "created_at": "2025-07-10T16:50:27Z",
      "last_modified_local_at": "2025-07-10T17:01:35Z",
      "last_synced_at": "2025-07-10T17:05:00Z",
      "local_sha256_hash": "abc123...", // SHA256 hash of the local file content
      "google_doc_id": "11gjGlApE4r6HfiDWYlc3Ah4p6mKfo8KOdOMIoRXKTb4",
      "google_doc_version": "123", // If available from Drive API (e.g., headRevisionId or version)
      "google_doc_last_known_good_at": "2025-07-10T17:05:00Z", // Timestamp of last successful GDoc access
      "status": "active", // e.g., active, local_only, orphaned_gdoc, conflict
      "source": "import", // e.g., import, generated, manual_add
      "dependencies": [] // For future use, e.g. if docs reference each other
    }
  },
  "sync_preferences": {
    "google_drive_folder": {
      "name": "MADIO AI System Documents",
      "id": "1ABC...xyz",
      "auto_organize": true
    },
    "interaction_mode": "interactive" // interactive, non_interactive, auto
  }
}
```
    *   **Location:** This registry should reside in a project-specific file, e.g., `.madio/document_registry.json`.
    *   **Relationship to existing files:** This will replace `sync_config.json` and `.synced_docs_mapping.json`. A migration path will be needed for existing projects.

#### 2. Enhanced Command Interface

- `madio-import-docs --mode=replace|merge|fresh`:
    *   `replace`: Existing local documents (and their entries in `document_registry`) are removed. User is prompted whether to attempt deletion of associated Google Docs or just sever the link. New documents are then imported.
    *   `merge`: New documents are added. If a new document has the same name as an existing one, user is prompted to overwrite, skip, or rename.
    *   `fresh`: Entire `document_registry` is wiped. User is prompted about existing Google Docs (similar to `replace`). Project is then treated as new.
- `push-to-docs --force-new --validate-mappings --interactive`:
    *   `--force-new`: For each local file being synced, a new Google Doc is created, even if a valid mapping already exists in the `document_registry`. The old Google Doc is unlinked (user prompted if it should be deleted/archived).
    *   `--validate-mappings`: Triggers Smart Mapping Validation before sync.
    *   `--interactive` (deprecated, use `sync_preferences.interaction_mode` or global CLI flag): Hint for behavior, see Interactive User Flow Management.
- `madio-update-docs --add path/to/file.md | --remove path/to/file.md | --replace path/to/file.md --with path/to/newfile.md`: Manages entries in the `document_registry` and corresponding local files.
- `madio-sync-status --health-check --repair`: Validates `document_registry` against local files and Google Docs. `--repair` attempts to fix issues interactively.

#### 3. Interactive User Flow Management

- **Environment Detection & Robust Input:**
    *   The `push-to-docs` bash script (and other user-facing commands) should, if an interactive session is intended by the user, pass a specific flag like `--interactive-session` to underlying Python scripts (e.g., `sync_to_docs.py`).
    *   Python scripts like `sync_to_docs.py`, when receiving `--interactive-session`, should still first attempt `sys.stdin.isatty()`.
    *   If `isatty()` is false but `--interactive-session` is present, the script should attempt more robust methods to solicit user input. This could involve:
        *   Attempting to open and read from `/dev/tty` directly (on Unix-like systems).
        *   Exploring if the calling environment (e.g., Claude Code CLI) offers a specific mechanism or environment variable to facilitate direct user interaction for child processes.
        *   As a last resort, clearly informing the user that interaction is desired but not achievable, and guiding them to use command-line flags for non-interactive specification (e.g., `--folder-id X`, `--default-action approve`).
- **Prompt Management**: Ensure critical user prompts are displayed and awaited properly. Prompts should be clear, concise, and offer understandable choices.
- **Fallback Behavior**: Provide sensible defaults when interaction is not possible or explicitly overridden (e.g., using `sync_preferences.interaction_mode = "non_interactive"`).
- **User Preference Persistence**: Remember user choices for future operations (e.g., selected Google Drive folder ID stored in `sync_preferences`).

#### 4. Smart Mapping Validation

- **Trigger Points:** Validation should occur at the beginning of `/push-to-docs` (if `--validate-mappings` is used or by default), and can be invoked directly by `/madio-sync-status --health-check`.
- **Validation Steps:**
    1.  For each entry in `document_registry`:
        *   Check if `local_path` exists. If not, mark status as `orphaned_mapping` (or similar) and prompt user: "Local file [path] is missing but mapped. (R)emove from registry? (S)kip this sync? (A)bort?".
        *   If local file exists, verify `local_sha256_hash`. If changed since last sync, mark for sync.
        *   If `google_doc_id` exists:
            *   Attempt to access the Google Doc (e.g., `drive.files.get` with minimal fields).
            *   If inaccessible (404, 403), mark status as `orphaned_gdoc` and prompt: "Google Doc for [local_path] (ID: [gdoc_id]) is inaccessible. (C)reate new GDoc? (U)nlink from registry? (S)kip? (A)bort?".
            *   (Optional) If accessible, compare `google_doc_version` with stored version to detect remote changes.
- **Automatic Stale Mapping Detection and Resolution**: Based on the validation steps, offer interactive or pre-configured resolutions.
- **Interactive Conflict Resolution**: For more complex conflicts (e.g., both local and remote changed), guide the user.
- **Fallback to New Document Creation**: If a mapping is invalid and user chooses to, create a new Google Doc and update the registry.

#### 5. Workflow State Persistence

- Track document creation and modification events
- Maintain sync history and success/failure states
- Enable rollback to previous working states
- Provide audit trail for troubleshooting

## Functional Requirements

### FR1: Multi-Mode Import Operations

- **Replace Mode**: Clear existing documents and import new set
- **Merge Mode**: Add new documents while preserving existing ones
- **Fresh Mode**: Reset entire project and start clean
- **Preview Mode**: Show what changes will be made before applying

### FR2: Intelligent Sync Management

- **Mapping Validation**: Verify Google Doc accessibility before sync (as detailed in Technical Requirements).
- **Stale Detection**: Identify and handle trashed/deleted Google Docs, or missing local files (as detailed in Technical Requirements).
- **Auto-Recovery**: Based on user preference or interactive choice, create new documents when mappings fail or are missing.
- **Conflict Resolution**:
    *   Handle duplicate local filenames during import (prompt: Overwrite, Skip, Rename).
    *   Handle mapping collisions (e.g., two local files trying to map to the same Google Doc ID - should be rare with new registry but needs consideration).
    *   Handle concurrent modification conflicts: If both the local file (based on `local_sha256_hash`) and the Google Doc (based on `google_doc_version`) have changed since the `last_synced_at` timestamp in the `document_registry`, prompt user: "File [X] has been changed locally and on Google Drive. (L)ocal overwrites GDoc, (G)Doc overwrites local, (S)kip sync for this file?".

### FR3: Interactive User Experience

- **Google Drive Folder Selection**: Always attempt to prompt user for folder choice during initial sync setup, using robust interaction methods (see Technical Requirements). Allow override via command-line flags or `sync_preferences`.
- **Operation Confirmation**: Confirm destructive operations (e.g., deleting Google Docs, overwriting files) before execution, unless in non-interactive mode with explicit force flags.
- **Progress Visibility**: Show clear progress indicators during operations (e.g., using `tqdm` or similar).
- **Error Recovery Guidance**: Provide actionable steps or choices when operations fail (e.g., "Retry API call?", "Skip this file?", "Edit credentials?").

### FR4: Document Registry System

- **Lifecycle Tracking**: Record creation, modification, local and GDoc deletion/unlinking events in the `document_registry`.
- **Dependency Management**: (Future) Track document relationships and hierarchies.
- **Status Monitoring**: Monitor sync health and document accessibility using the `status` field in the `document_registry`.
- **Change Detection**:
    *   Identify local changes by comparing current file hash (`sha256`) against stored `local_sha256_hash` in the `document_registry`.
    *   Identify remote Google Doc changes by comparing current `google_doc_version` (e.g., `headRevisionId` from Drive API) against stored version.

### FR5: Environment-Aware Operation

- **Interactive Mode**: Full prompts and confirmations in terminal environments
- **Non-Interactive Mode**: Sensible defaults for CI/CD and automated environments
- **Hybrid Mode**: Critical prompts only, with defaults for routine operations
- **Override Flags**: Command-line flags to force specific behaviors

## Critical Bug Fixes

### BUG-001: Missing Google Drive Folder Selection

**Priority**: Critical

**Description**: During `/push-to-docs` execution, particularly within environments like the Claude Code CLI, users are not prompted to select a Google Drive folder. This results in documents being placed in the Google Drive root folder by default, bypassing user choice for organization.

**Root Cause**:
- The `push-to-docs` bash script checks if stdin/stdout are TTYs (`[ ! -t 0 ] || [ ! -t 1 ]`). In environments like Claude Code CLI, this check often results in a "non-interactive" determination.
- If deemed non-interactive, the bash script calls `sync_to_docs.py` without the `--folder` argument.
- `sync_to_docs.py` then uses `sys.stdin.isatty()` which also reports false, causing it to skip the interactive folder prompt and default to the root Drive folder.
- The core issue is the difficulty in reliably detecting user-interactive sessions versus truly non-interactive (e.g., CI/CD) sessions, and the lack of robust input fallbacks in the Python script when `isatty()` is false but interaction is desired.

**Fix Requirements**:
- Modify `push-to-docs` (bash) to pass an `--interactive-session` flag to `sync_to_docs.py` if the user's invocation of `/push-to-docs` implies an interactive context (e.g., not explicitly a CI environment).
- Update `sync_to_docs.py` to:
    - Prioritize the `--interactive-session` flag if present.
    - If `--interactive-session` is true and `isatty()` is false, attempt alternative input methods (e.g., direct read from `/dev/tty`, or platform-specific techniques for Claude Code CLI if available).
    - If robust interaction cannot be established, provide clear guidance to the user on how to specify the folder non-interactively (e.g., using `--folder "Folder Name"` or by setting `sync_preferences.google_drive_folder`).
- Ensure command-line flags for explicit folder specification (e.g., `--folder-id <ID>`, `--folder-name "Name"`) are robust and clearly documented.
- Test interaction flows in various environments (standard terminal, VS Code terminal, Claude Code CLI, CI/CD mock).

### BUG-002: Stale Document Mapping Persistence

**Priority**: High

**Description**: Document mappings in `sync_config.json` or `.synced_docs_mapping.json` can become stale if local files are deleted/moved or corresponding Google Docs are deleted/trashed outside of MADIO's control. Sync operations then fail with errors when trying to access these non-existent resources.

**Fix Requirements**:
- Implement pre-sync validation logic within `sync_to_docs.py` (or a dedicated module called by it) that uses the new `document_registry.json`.
- This validation (as detailed in Technical Requirements - Smart Mapping Validation) should:
    - Check for the existence of local files specified in the registry.
    - Verify accessibility of linked Google Docs via API calls.
    - Prompt users interactively (if in interactive mode) to resolve discrepancies (e.g., remove mapping, recreate GDoc, re-link, skip).
- Provide non-interactive resolution strategies (e.g., `--fix-stale-mappings=remove_link` or `--fix-stale-mappings=create_new_gdoc`).
- Ensure that operations like local file deletion via `madio-update-docs --remove` correctly update the `document_registry` and prompt for Google Doc deletion/unlinking.

## Success Metrics

### Primary KPIs

- **Workflow Success Rate**: 95% of iterative workflows complete without errors
- **Sync Reliability**: 99% of sync operations succeed on first attempt
- **User Satisfaction**: 90% of users report positive experience with iterative workflows
- **Error Recovery**: 95% of sync failures auto-resolve without manual intervention
- **User Interaction Success**: 100% of users receive folder selection prompts when expected

### Secondary Metrics

- **Time to Add Document**: <2 minutes to add new document to existing project
- **Documentation Clarity**: <5 support requests per month for workflow guidance
- **System Reliability**: <1 critical bug per month affecting iterative workflows
- **Adoption Rate**: 80% of users use iterative features within 30 days
- **Folder Organization**: 90% of users successfully organize documents in chosen folders

## Implementation Phases

### Phase 1: Critical Bug Fixes & Initial Registry (Week 1-2)

- **BUG-001 Fix - Robust Folder Interaction**:
    - Implement the `--interactive-session` flag strategy between `push-to-docs` (bash) and `sync_to_docs.py`.
    - Enhance `sync_to_docs.py` with fallback input methods if `isatty()` is false but interactive session is requested. Test thoroughly in Claude Code CLI.
- **Basic Document Registry**:
    - Introduce the initial `document_registry.json` structure (`.madio/document_registry.json`).
    - Modify `sync_to_docs.py` to read from/write to this registry for basic file path to Google Doc ID mapping (replacing `.synced_docs_mapping.json` and aspects of `sync_config.json`).
- **Migration Script (Initial Version)**: Develop a script to migrate existing projects from `.synced_docs_mapping.json` and `sync_config.json` (for folder preference) to the new `document_registry.json`.
- **BUG-002 Fix - Basic Stale Mapping Detection**:
    - Implement initial pre-sync validation in `sync_to_docs.py` to check:
        - Local file existence for entries in `document_registry`.
        - Basic Google Doc accessibility (e.g., a `files.get` call).
    - For now, on error, provide clear error messages and skip problematic files (interactive resolution comes later).
- **Force-New Flag**: Implement `--force-new` for `push-to-docs` as described in Technical Requirements.

### Phase 2: Full Document Registry & Lifecycle (Week 3-4)

- **Complete Document Registry**: Enhance `document_registry.json` entries with all fields specified in Technical Requirements (hashes, versions, timestamps, status, source).
- **Lifecycle Event Tracking**: Update `sync_to_docs.py` and other relevant commands (`madio-import-docs`, `madio-update-docs`) to populate and update these new registry fields during operations.
- **Smart Mapping Validation (Interactive)**: Implement the full interactive stale mapping detection and resolution logic (user prompts for missing files, inaccessible GDocs) as part of `sync_to_docs.py` or a module it uses.
- **User Preference Persistence**: Store chosen folder ID and interaction mode in `sync_preferences` within `document_registry.json` or a separate `.madio/user_prefs.json`.

### Phase 3: Enhanced Commands & Workflows (Week 5-6)

- **`madio-import-docs` Enhancements**: Implement `replace`, `merge`, `fresh` modes with defined behaviors for Google Docs.
- **`madio-update-docs` Implementation**: Create the `madio-update-docs` command for granular registry and file management.
- **`madio-sync-status --health-check --repair`**: Develop this command to use the full document registry for validation and interactive repair.
- **Conflict Resolution**: Implement handling for concurrent modification conflicts (local vs. GDoc changes).

### Phase 4: User Experience & Testing (Week 7-8)

- **Comprehensive User Prompts**: Review and refine all user prompts for clarity and consistency.
- **Documentation**: Update all relevant documentation (README, SYNC_SETUP, command docs) to reflect the new architecture and workflows. Create a migration guide for existing users.
- **Comprehensive Testing**: Validate all iterative workflow scenarios, bug fixes, and new command functionalities across different environments.
- **Migration Script (Final Version)**: Ensure the migration script is robust and handles edge cases.

### Phase 5: Polish & Advanced Features (Week 9-10)

- **Performance Optimization**: Profile and optimize sync speed and registry operations.
- **Advanced Features (Optional)**: Consider adding rollback capabilities or more detailed audit trails if time permits.
- **Final Documentation & Training Materials**: Complete user guides, workflow examples, and any training materials.

## Risk Assessment

### Technical Risks

- **Backward Compatibility**: Changes might break existing user workflows
- **Google API Limits**: Increased API usage due to validation calls
- **State Management Complexity**: Document registry adds system complexity
    - **Data Migration**: Existing projects need migration to new state format (`document_registry.json`).
    - **Environment Compatibility**: Interactive features (especially folder selection prompts) may behave differently or fail in diverse CLI environments (standard terminals, VS Code integrated terminal, Claude Code CLI, CI/CD).
    - **Complexity of Robust Interaction**: Reliably detecting true user interactive intent versus scripted/non-interactive sessions across all target environments for `sync_to_docs.py` is challenging.

### Mitigation Strategies

- **Phased Rollout**: Gradual introduction of new features with fallbacks to existing behavior where possible during transition.
- **API Optimization**: Batch operations and intelligent caching to stay within Google API limits.
- **Comprehensive Testing**: Extensive testing of migration paths, new interactive flows, and edge cases for stale data.
- **Clear Migration Path**: Provide an automated script (`madio-migrate-config`) and clear documentation for upgrading existing projects to the new `document_registry.json`.
- **Multi-Environment Testing**: Validate functionality across all supported environments, with specific focus on Claude Code CLI for interactive prompts.
- **Graceful Fallback for Interaction**: Prioritize a graceful fallback to non-interactive mode with clear user guidance if robust interactive input cannot be reliably obtained, even when an interactive session was intended. Offer explicit command-line flags for all prompted actions.

## Acceptance Criteria

### Must-Have Features

- ✅ Users are reliably prompted for Google Drive folder selection during initial sync operations (e.g., first `/push-to-docs` for a project or when no folder is configured), even within environments like Claude Code CLI. If interaction is impossible, clear guidance for non-interactive specification is provided.
- ✅ Subsequent syncs use the configured/remembered Google Drive folder without re-prompting, unless explicitly requested.
- ✅ Users can add new documents to existing projects (e.g., via `madio-import-docs` or manually adding to `synced_docs/`), and these are correctly synced to new Google Docs in the chosen folder.
- ✅ Stale Google Doc mappings (missing local files or inaccessible Google Docs) are automatically detected before sync attempts. Users are interactively prompted (in interactive mode) to resolve these issues (e.g., remove mapping, create new GDoc, skip).
- ✅ `madio-import-docs` command supports `merge` (default), `replace`, and `fresh` modes with clear, predictable behavior regarding local files and their Google Doc counterparts.
- ✅ The sync process provides clear error messages for API failures or other issues, along with actionable recovery options or guidance.
- ✅ The `document_registry.json` is the source of truth for mappings and sync state, replacing older config/mapping files.
- ✅ A migration path (script and documentation) exists for users with existing `sync_config.json` or `.synced_docs_mapping.json` based projects.

### Should-Have Features

- ✅ All document lifecycle events (creation, local modification, sync, GDoc linking/unlinking, deletion) are tracked with timestamps and relevant metadata in the `document_registry.json`.
- ✅ Interactive conflict resolution guides users through issues
- ✅ Health-check commands validate project and sync status
- ✅ Migration tools upgrade existing projects to new format
- ✅ User preferences are remembered across sessions

### Nice-to-Have Features

- ✅ Rollback capability for failed operations
- ✅ Batch operations for bulk document management
- ✅ Advanced workflow automation and scripting
- ✅ Integration with version control systems
- ✅ Command-line flags for non-interactive operation

## Conclusion

This structural transformation will position MADIO as a true development framework rather than a one-time setup tool. By enabling iterative development workflows and fixing critical user interaction issues, users can continuously evolve their AI systems while maintaining full control over their document organization and sync preferences.

The immediate focus on fixing the Google Drive folder selection issue addresses a critical user experience problem that affects every sync operation. Combined with the iterative development capabilities, this creates a robust foundation for sophisticated AI system development workflows.

**Key Success Factor**: The system must feel natural to users who expect to iterate on their AI systems continuously, with full control over where their documents are organized and how operations proceed.
