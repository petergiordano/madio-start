# Product Requirements Document: MADIO Iterative Development Framework

## Executive Summary

The MADIO Framework currently operates under a "one-time setup" model that assumes users create AI system documents once and deploy them. Real-world usage patterns reveal that users require iterative development capabilities - the ability to continuously add, replace, update, and refine their AI system documents throughout the project lifecycle. Additionally, critical user interaction features like Google Drive folder selection are being bypassed, degrading the user experience. This PRD outlines the structural changes needed to transform MADIO from a static setup tool into a dynamic development framework with proper user interaction flows.

## Problem Statement

### Current State Limitations

- **Single Document Lifecycle**: System assumes documents are created once via `/generate-ai-system` or `/madio-import-docs`
- **Stale Mapping Persistence**: Document-to-Google Doc ID mappings persist indefinitely, causing sync failures when documents are replaced
- **No Lifecycle Management**: No tracking of document creation, modification, or replacement events
- **Poor User Experience**: Users encounter cryptic errors when attempting iterative workflows
- **Brittle Sync Process**: Google Docs sync breaks when attempting to sync to trashed or deleted documents
- **Missing User Interaction**: Google Drive folder selection prompts are bypassed, forcing documents into root folder without user choice

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
- **Story 1.2**: Replace existing documents with new versions
- **Story 1.3**: Remove documents that are no longer needed
- **Story 1.4**: Track document history and changes

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
    "sync_status": "active"
  },
  "document_registry": {
    "project_system_instructions.md": {
      "tier": 1,
      "created": "2025-07-10T16:50:27Z",
      "last_modified": "2025-07-10T17:01:35Z",
      "google_doc_id": "11gjGlApE4r6HfiDWYlc3Ah4p6mKfo8KOdOMIoRXKTb4",
      "status": "active",
      "source": "import",
      "dependencies": []
    }
  },
  "sync_preferences": {
    "google_drive_folder": {
      "name": "MADIO AI System Documents",
      "id": "1ABC...xyz",
      "auto_organize": true
    },
    "interaction_mode": "interactive"
  }
}
```

#### 2. Enhanced Command Interface

- `madio-import-docs --mode=replace|merge|fresh`
- `push-to-docs --force-new --validate-mappings --interactive`
- `madio-update-docs --add|remove|replace`
- `madio-sync-status --health-check --repair`

#### 3. Interactive User Flow Management

- **Environment Detection**: Distinguish between interactive (terminal) and non-interactive (CI/CD) environments
- **Prompt Management**: Ensure critical user prompts are displayed and awaited properly
- **Fallback Behavior**: Provide sensible defaults when interaction is not possible
- **User Preference Persistence**: Remember user choices for future operations

#### 4. Smart Mapping Validation

- Pre-sync validation of Google Doc accessibility
- Automatic stale mapping detection and resolution
- Interactive conflict resolution for ambiguous cases
- Fallback to new document creation when needed

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

- **Mapping Validation**: Verify Google Doc accessibility before sync
- **Stale Detection**: Identify and handle trashed/deleted documents
- **Auto-Recovery**: Create new documents when mappings fail
- **Conflict Resolution**: Handle duplicate names and mapping collisions

### FR3: Interactive User Experience

- **Google Drive Folder Selection**: Always prompt user for folder choice unless explicitly overridden
- **Operation Confirmation**: Confirm destructive operations before execution
- **Progress Visibility**: Show clear progress indicators during operations
- **Error Recovery Guidance**: Provide actionable steps when operations fail

### FR4: Document Registry System

- **Lifecycle Tracking**: Record creation, modification, and deletion events
- **Dependency Management**: Track document relationships and hierarchies
- **Status Monitoring**: Monitor sync health and document accessibility
- **Change Detection**: Identify when documents need re-sync

### FR5: Environment-Aware Operation

- **Interactive Mode**: Full prompts and confirmations in terminal environments
- **Non-Interactive Mode**: Sensible defaults for CI/CD and automated environments
- **Hybrid Mode**: Critical prompts only, with defaults for routine operations
- **Override Flags**: Command-line flags to force specific behaviors

## Critical Bug Fixes

### BUG-001: Missing Google Drive Folder Selection

**Priority**: Critical

**Description**: During push-to-docs execution, users are not prompted to select Google Drive folder destination, causing documents to be placed in root folder without user choice.

**Root Cause**:
- Environment detection incorrectly identifies interactive terminal as non-interactive
- Claude Code CLI environment may not properly forward stdin to Python subprocess
- Folder selection prompt logic bypassed due to environment detection failure

**Fix Requirements**:
- Implement robust interactive environment detection
- Ensure stdin forwarding works correctly in Claude Code CLI
- Add fallback prompts using alternative input methods if needed
- Provide command-line flags for explicit folder specification
- Test interaction flows in all supported environments

### BUG-002: Stale Document Mapping Persistence

**Priority**: High

**Description**: Document mappings persist after documents are deleted, causing sync failures when users perform iterative workflows.

**Fix Requirements**:
- Implement mapping validation before sync operations
- Add automatic cleanup of stale mappings
- Provide user confirmation for mapping conflicts
- Enable forced regeneration of mappings when needed

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

### Phase 1: Critical Bug Fixes (Week 1)

- **Interactive Environment Detection**: Fix Google Drive folder selection prompt
- **Stdin Forwarding**: Ensure prompts work correctly in Claude Code CLI
- **Sync Validation**: Add mapping validation to prevent stale document errors
- **Force-New Flag**: Enable users to force creation of new Google Docs

### Phase 2: Foundation (Week 2)

- **Document Registry**: Implement lifecycle state tracking
- **User Preference Persistence**: Remember folder choices and interaction preferences
- **Clear Documentation**: Document current workarounds and best practices

### Phase 3: Core Functionality (Week 3-4)

- **Enhanced Import**: Add replace/merge/fresh modes to madio-import-docs
- **Smart Sync**: Automatic stale mapping detection and resolution
- **Interactive Flows**: Comprehensive user interaction management

### Phase 4: User Experience (Week 5-6)

- **Conflict Resolution**: Add user prompts for mapping conflicts
- **Status Commands**: Implement sync-status and health-check tools
- **Comprehensive Testing**: Validate all iterative workflow scenarios

### Phase 5: Polish & Optimization (Week 7-8)

- **Performance Optimization**: Improve sync speed and reliability
- **Advanced Features**: Add rollback, audit trails, and advanced workflows
- **Documentation & Training**: Complete user guides and workflow documentation

## Risk Assessment

### Technical Risks

- **Backward Compatibility**: Changes might break existing user workflows
- **Google API Limits**: Increased API usage due to validation calls
- **State Management Complexity**: Document registry adds system complexity
- **Data Migration**: Existing projects need migration to new state format
- **Environment Compatibility**: Interactive features may not work in all environments

### Mitigation Strategies

- **Phased Rollout**: Gradual introduction of new features with fallbacks
- **API Optimization**: Batch operations and intelligent caching
- **Comprehensive Testing**: Extensive testing of migration and edge cases
- **Clear Migration Path**: Automated tools for upgrading existing projects
- **Multi-Environment Testing**: Validate functionality across all supported environments

## Acceptance Criteria

### Must-Have Features

- ✅ Users are always prompted for Google Drive folder selection during sync operations
- ✅ Users can add new documents to existing projects without sync failures
- ✅ Stale Google Doc mappings are automatically detected and resolved
- ✅ Import operations support replace, merge, and fresh modes
- ✅ Sync process provides clear error messages and recovery options
- ✅ Interactive prompts work correctly in Claude Code CLI environment

### Should-Have Features

- ✅ Document lifecycle events are tracked and auditable
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
