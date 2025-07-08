# Claude Code Context - MADIO Framework

**Role:** Initial Setup & MADIO Document Generation
**Handoff:** After setup, development continues with Gemini CLI

**Primary Context Source:** Read the complete project context from `AI_CONTEXT.md` - it contains all MADIO project-specific guidelines, template selection rationale, and development context needed for this project.

## MADIO Framework Overview
You are working within a MADIO (Modular AI Declarative Instruction and Orchestration) project that uses structured templates to create production-ready AI systems.

**Claude Code's Responsibilities:**
1. **Initial project setup** via `/madio-setup` command
2. **MADIO document generation** via `/generate-ai-system` command
3. **Handoff preparation** by updating AI_CONTEXT.md for Gemini CLI

## Quick Reference
- **Always read AI_CONTEXT.md completely before starting any work**
- **Framework Type:** MADIO-based AI system development
- **Template Library:** Check `_template_library/` for available MADIO templates
- **Project Phase:** [Determined from AI_CONTEXT.md Current Status section]
- **Document Hierarchy:** Tier 1 (Authority) → Tier 2 (Orchestration) → Tier 3 (Supporting)

## Claude Code Workflow Integration

### 1. Initial Assessment
1. **Use Plan Mode (Shift+Tab twice)** for complex tasks and initial analysis
2. **Read AI_CONTEXT.md** to understand current project state and template selection
3. **Check Document Architecture section** for current MADIO documents and their status
4. **Review Key Decisions** to understand template selection rationale

### 2. MADIO Document Operations
- **Template Selection:** Reference `madio_core_templates.md` for template guidance
- **Document Generation:** Follow MADIO hierarchical structure (Tier 1 → 2 → 3)
- **Placeholder Replacement:** Ensure all `[BRACKETED_TEXT]` is replaced with project-specific content
- **Cross-References:** Maintain proper document interconnections

### 3. Quality Validation
- **Hierarchical Integrity:** Verify Tier 1 has supreme authority over Tier 2 and 3
- **Template Compliance:** Ensure generated documents follow template structure
- **Deployment Readiness:** Confirm documents can be directly deployed to target platforms

## MADIO-Specific Commands

### Document Generation
```bash
# Generate core MADIO documents
claude "Create project_system_instructions.md using the MADIO Tier 1 template"
claude "Generate orchestrator.md that references the Tier 3 documents"
```

### Context Updates (Prepare for Gemini CLI Handoff)
```bash
# Update bridge file with current status
claude "Update AI_CONTEXT.md with the new document architecture and template selections"
claude "Document the rationale for choosing [specific templates] in AI_CONTEXT.md"
claude "Prepare AI_CONTEXT.md for Gemini CLI handoff with current project status"
```

### Validation
```bash
# Validate MADIO system completeness
claude "Validate the document hierarchy and check for any missing cross-references"
claude "Review all placeholders and ensure project-specific content replacement"
```

## Context Handoff Protocol

### From Chat AI (Claude Project/Browser)
- **Receive:** Context-rich prompts that include relevant sections from AI_CONTEXT.md
- **Transfer:** Development notes and architectural decisions from browser-based Claude
- **Continuity:** Maintain awareness of previous sessions through AI_CONTEXT.md

### To Gemini CLI (Ongoing Development)
- **Update AI_CONTEXT.md:** After completing initial MADIO document generation
- **Document Setup Decisions:** Record template selection rationale and initial customizations
- **Handoff Status:** Update project phase to "Ready for Gemini CLI Development"

### To Chat AI (Browser Claude Project)
- **Backup Context:** Provide AI_CONTEXT.md to browser-based Claude for strategic oversight
- **Status Reports:** Share major milestones and architectural decisions
- **Quality Assurance:** Enable browser Claude to validate overall system design

## MADIO Template Reference

### Always Required (Every Project)
- `project_system_instructions.md` (Tier 1) - Core AI agent instructions
- `orchestrator.md` (Tier 2) - Step-by-step methodology and workflow control

### Tier 3 Template Categories
**Content & Character:**
- `character_voice_authority` - Personality and voice consistency
- `content_operations` - Content validation and curation
- `standard` - Templated output formats

**Analysis & Evaluation:**
- `methodology_framework` - 8-step complex analysis process
- `rubrics_evaluation` - 4-level multi-dimensional scoring
- `strategic_framework` - Strategic assessment capabilities
- `research_protocols` - Evidence collection and validation

**Visual & Implementation:**
- `visual_design_standards` - Brand consistency and guidelines
- `visual_asset_generation` - Automated image and graphic creation
- `implementation_roadmap` - Phased execution planning
- `document_reference_map` - Complex project interconnection mapping

## Deployment Preparation

### Platform Export Checklist
- [ ] **OpenAI CustomGPT:** Verify project_system_instructions.md is deployment-ready
- [ ] **Google Gemini Gem:** Ensure document combination follows .madio configuration
- [ ] **Claude Project:** Confirm all supporting documents uploaded to project knowledge
- [ ] **AI_CONTEXT.md Updated:** Bridge file contains current status for handoff

## Quality Standards

### MADIO Framework Requirements
- **System Completeness:** 95%+ workflow coverage and capability mapping
- **Maintainability Index:** 90%+ modular design with clear separation
- **Hierarchical Integrity:** Clear Tier 1 → Tier 2 → Tier 3 authority chain
- **Cross-Reference Accuracy:** Proper document interconnection and workflow
- **Deployment Readiness:** Direct copy-paste capability for target platforms

## Key Reminders
- **Follow MADIO hierarchy:** Tier 1 authority > Tier 2 orchestration > Tier 3 support
- **Replace all placeholders:** Never leave `[BRACKETED_TEXT]` in final documents
- **Maintain template compliance:** Use templates from `_template_library/`
- **Update AI_CONTEXT.md:** Keep bridge file current for browser AI handoff
- **Validate completeness:** Ensure all required documents exist and interconnect properly
- **Document decisions:** Record template selection rationale and customizations

## Error Prevention
- **Check template availability:** Verify template exists in `_template_library/` before referencing
- **Validate hierarchy:** Ensure no circular dependencies in document references
- **Confirm placeholders:** Scan for any remaining `[BRACKETED_TEXT]` before deployment
- **Test cross-references:** Verify all document interconnections function correctly
- **Platform compatibility:** Ensure generated documents work on target deployment platform

## Success Indicators
- All mandatory documents generated (project_system_instructions.md, orchestrator.md)
- Template selection documented in AI_CONTEXT.md with clear rationale
- Document hierarchy maintains proper authority chain
- All placeholders replaced with project-specific content
- Cross-references between documents function correctly
- AI_CONTEXT.md updated with current project status for browser AI handoff
