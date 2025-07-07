# MADIO Framework - Gemini CLI Context

## Overview

You are helping users set up and generate AI systems using the MADIO (Modular AI Declarative Instruction and Orchestration) framework. This framework enables creation of production-ready AI applications for ChatGPT Custom GPTs, Gemini Gems, and Claude Projects.

## Available Commands

### `/madio-setup` - Project Initialization

When a user runs `/madio-setup`, you should:

1. **Validate Environment**
   - Check if setup was already completed (look for `.madio-setup-complete` marker)
   - Verify user is in their own project directory (not in `madio-start`)
   - Confirm git is properly initialized

2. **Configure Git Remotes**
   ```bash
   # Add template remote for updates
   git remote add template https://github.com/petergiordano/madio-start.git
   ```

3. **Move Templates to Project Root**
   - Copy `_project_scaffolding/_template_library/` to `_template_library/`
   - Copy `_project_scaffolding/madio_core_templates.md` to root
   - Copy any other scaffolding files

4. **Update Configuration**
   - Update `.madio` file with project name from directory
   - Set appropriate defaults

5. **Clean Up**
   - Remove `_project_scaffolding/` directory
   - Create `.madio-setup-complete` marker file

6. **Commit Changes**
   ```bash
   git add -A
   git commit -m "Initialize MADIO project structure"
   ```

7. **Provide Next Steps**
   - Confirm successful setup
   - Guide user to generate their AI system

### MADIO Document Generation

When users request AI system creation:

1. **Always Reference Templates**
   - Use templates from `_template_library/`
   - Follow MADIO hierarchical structure

2. **Mandatory Documents**
   - Always create `project_system_instructions.md` (Tier 1)
   - Always create `orchestrator.md` (Tier 2)

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

## Success Confirmation

After successful generation:
1. List all created documents
2. Remind about placeholder replacement
3. Suggest testing approach
4. Provide deployment guidance