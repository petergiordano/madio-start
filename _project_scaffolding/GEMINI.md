# MADIO Framework - Gemini CLI Context

**Role:** Ongoing Development & Content Refinement
**Initial Setup:** Handled by Claude Code via `/madio-setup` and `/generate-ai-system`

## Overview

You are helping users develop and refine AI systems using the MADIO (Modular AI Declarative Instruction and Orchestration) framework. **Claude Code handles initial setup and document generation.** Your role begins after the initial MADIO documents are created.

**Gemini CLI Responsibilities:**
1. **Content refinement** and ongoing document improvement
2. **Feature additions** and capability enhancements
3. **AI_CONTEXT.md maintenance** for project continuity
4. **Deployment optimization** and platform-specific adjustments

## Available Commands

### Post-Setup Development Commands

**Note:** `/madio-setup` and `/generate-ai-system` are handled by Claude Code. Gemini CLI takes over for ongoing development.

### Common Development Tasks

When users request improvements or modifications:

1. **Review Existing Documents**
   - Read current MADIO documents to understand system architecture
   - Check AI_CONTEXT.md for context and previous decisions
   - Identify which documents need modification

2. **Content Enhancement**
   - Refine existing document content for clarity and effectiveness
   - Add new capabilities by modifying appropriate Tier 3 documents
   - Enhance personality and voice in character_voice_authority.md
   - Improve workflow steps in orchestrator.md

3. **Feature Additions**
   - Suggest additional Tier 3 templates if new capabilities are needed
   - Modify project_system_instructions.md for core behavior changes
   - Update content_operations.md for new content validation rules

4. **Quality Improvements**
   - Validate document hierarchy and cross-references
   - Check for any remaining placeholders `[BRACKETED_TEXT]`
   - Ensure all documents maintain MADIO framework compliance

5. **Update Documentation**
   - Update AI_CONTEXT.md with changes made
   - Document rationale for modifications
   - Update project phase and status

### MADIO Document Refinement

When users request modifications to existing documents:

1. **Always Reference Templates**
   - Use templates from `_template_library/`
   - Follow MADIO hierarchical structure

2. **Mandatory Documents**
   - Always create `project_system_instructions.md` (Tier 1)
   - Always create `orchestrator.md` (Tier 2)
   - Always update `AI_CONTEXT.md` with generation details

3. **Template Selection**
   - Simple projects: +1-2 Tier 3 documents
   - Moderate projects: +3-5 Tier 3 documents
   - Complex projects: +6-10 Tier 3 documents
   - Enterprise projects: +10+ Tier 3 documents

4. **Available Templates**

   **Content & Character:**
   - `character_voice_authority` - Personality and voice
   - `content_operations` - Content validation
   - `standard` - Output templates

   **Analysis & Evaluation:**
   - `methodology_framework` - 8-step analysis process
   - `rubrics_evaluation` - 4-level scoring system
   - `strategic_framework` - Strategic assessment
   - `research_protocols` - Evidence collection

   **Visual & Implementation:**
   - `visual_design_standards` - Brand consistency
   - `visual_asset_generation` - Image generation
   - `implementation_roadmap` - Phased execution
   - `document_reference_map` - Complex mapping

## Key Principles

1. **Hierarchy Matters**
   - Tier 1 has supreme authority
   - Tier 2 controls workflow
   - Tier 3 provides specifications

2. **Replace Placeholders**
   - All `[BRACKETED_TEXT]` must be project-specific
   - Common: `[PROJECT_NAME]`, `[DOMAIN]`, `[TARGET_AUDIENCE]`

3. **Maintain References**
   - Ensure all cross-document references are valid
   - No circular dependencies
   - Clear reporting structure

4. **Quality First**
   - Include quality gates in orchestrator
   - Define success metrics
   - Establish validation criteria

## Project Types & Template Recommendations

### Simple AI Assistant
- `project_system_instructions`
- `orchestrator`
- Optional: `character_voice_authority`

### Content Generator
- `project_system_instructions`
- `orchestrator`
- `content_operations`
- `standard`
- Optional: `visual_asset_generation`

### Customer Support Bot
- `project_system_instructions`
- `orchestrator`
- `character_voice_authority`
- `content_operations`
- Optional: `implementation_roadmap`

### Analysis System
- `project_system_instructions`
- `orchestrator`
- `methodology_framework`
- `rubrics_evaluation`
- `strategic_framework`
- `research_protocols`
- `implementation_roadmap`
- `document_reference_map`

## Error Handling

If setup fails:
- Check user is in correct directory
- Verify git status
- Ensure templates exist
- Provide clear error messages

## Auto-Update Triggers

### AI_CONTEXT.md Maintenance

AUTOMATICALLY update AI_CONTEXT.md when:

1. **Document Generation**: After creating any new MADIO documents
   - Update context with new documents and architecture
   - Include template selection rationale
   - Update document status tracking

2. **Template Selection**: When choosing specific templates
   - Document why templates were selected
   - Note templates considered but not used
   - Update complexity assessment

3. **Customization**: When modifying generated documents
   - Track custom adaptations made
   - Note design decisions and rationale
   - Update development phase status

4. **Problem Resolution**: When addressing issues or errors
   - Document challenges encountered
   - Record solutions implemented
   - Update lessons learned

### Auto-Update Commands Available

**Context Maintenance:**
- `gemini "Update AI_CONTEXT.md with recent project changes and current status"`
- `gemini "Document the template selection rationale in AI_CONTEXT.md"`
- `gemini "Add recent development notes to AI_CONTEXT.md"`

**Deployment Preparation:**
- `gemini "Generate deployment summary for AI_CONTEXT.md"`
- `gemini "Prepare AI_CONTEXT.md for [platform] deployment"`
- `gemini "Update AI_CONTEXT.md with quality validation checklist status"`

**Development Tracking:**
- `gemini "Log current development phase in AI_CONTEXT.md"`
- `gemini "Update next steps section in AI_CONTEXT.md"`
- `gemini "Document key decisions made in this session"`

### When to Trigger Updates

**Automatic (during operations):**
- Every document generation session
- Template selection decisions
- Error resolution
- Phase transitions (setup → generation → customization → deployment)

**Manual (user-requested):**
- Before copying context to deployed AI
- After major customizations
- During team handoffs
- Before deployment to production

## Success Confirmation

After successful generation:
1. List all created documents
2. Update AI_CONTEXT.md with generation summary
3. Remind about placeholder replacement
4. Suggest testing approach
5. Provide deployment guidance with AI_CONTEXT.md bridge instructions