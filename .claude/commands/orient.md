# Orient - MADIO Project Status & Navigation

Get oriented in your current MADIO project and see your next best actions based on current context and development phase.

## Purpose

This command helps you get re-oriented when returning to a MADIO project after time away. It combines system status with MADIO project analysis to show:
- Where you are in the MADIO development workflow
- What templates and documents are available
- Exact commands to run for your next best actions
- Current AI system generation status

## Process

1. **System Status Check**
   - Display Claude Code system information
   - Show MADIO framework availability
   - Confirm working directory and MADIO setup

2. **MADIO Project State Analysis**
   - Scan for MADIO templates and generated documents
   - Determine development phase (setup/generation/customization/deployment)
   - Identify available templates and complexity level

3. **Contextual MADIO Guidance**
   - Show current position in MADIO workflow
   - Provide numbered next action options
   - Include exact commands for AI system generation

4. **MADIO Context Loading**
   - Read AI_CONTEXT.md for project status
   - Load template selection rationale
   - Understand document hierarchy and relationships

## Implementation

### Phase 1: System Status
First, gather technical context about the MADIO environment:

```bash
Working Directory: [show current path]
IDE Integration: [VS Code + Claude Code status]
MADIO Framework: [setup status and version]
Git Remotes: [origin and template remote status]
```

### Phase 2: MADIO Project Analysis
Analyze the current directory structure for MADIO components:

**Key MADIO Files to Check:**
- `.madio-setup-complete` - Setup completion marker
- `_project_scaffolding/` - Indicates fresh template (setup needed)
- `_template_library/` - Available MADIO templates (14 templates)
- `madio_core_templates.md` - Template selection guide
- `AI_CONTEXT.md` - Project bridge file and current status
- `GEMINI.md` / `CLAUDE.md` - CLI context files
- `.madio` - Project configuration
- Generated AI system documents (project_system_instructions.md, orchestrator.md, etc.)

**MADIO Workflow Stage Detection Logic:**
```
IF _project_scaffolding/ exists:
  → "Template Setup Mode" - need to run /madio-setup

ELIF no AI_CONTEXT.md exists:
  → "Setup Incomplete" - framework available but bridge file missing

ELIF no project_system_instructions.md exists:
  → "Generation Phase" - ready to generate core AI system documents

ELIF project_system_instructions.md exists but few Tier 3 documents:
  → "Expansion Phase" - ready to add supporting templates

ELIF complete document set exists:
  → "Deployment Phase" - ready for platform deployment

ELIF deployed:
  → "Production Mode" - system live, ready for iteration
```

### Phase 3: Contextual MADIO Action Menu

Based on detected stage, provide numbered options:

**Template Setup Mode:**
```
📍 Status: MADIO Template Setup Required
🎯 Next Actions:
1. Run /madio-setup (transforms template to MADIO workspace)
2. Verify git configuration and template remote
3. Learn about MADIO framework and 14 templates
4. Review madio_core_templates.md for template guidance
5. Prepare for AI system generation
```

**Generation Phase:**
```
📍 Status: MADIO AI System Generation
🎯 Next Actions:
1. Generate core system: gemini "Create [your AI system] using MADIO framework"
2. Let MADIO choose templates: gemini "I want [your idea], use MADIO templates"
3. Review template options: Read madio_core_templates.md
4. Update context: gemini "Update AI_CONTEXT.md with generation progress"
5. Examples:
   - Customer support: gemini "Create customer support bot with MADIO"
   - Content system: gemini "Create content writing AI with MADIO"
   - Analysis system: gemini "Create data analysis AI with MADIO"
```

**Expansion Phase:**
```
📍 Status: MADIO System Expansion
🎯 Next Actions:
1. Add templates: gemini "Add [template_name] to my AI system for [purpose]"
2. Enhance system: gemini "Expand my AI system with [capability]"
3. Review hierarchy: Validate Tier 1 → Tier 2 → Tier 3 relationships
4. Update context: gemini "Document template additions in AI_CONTEXT.md"
5. Available templates: [list unused templates from madio_core_templates.md]
```

**Deployment Phase:**
```
📍 Status: MADIO System Ready for Deployment
🎯 Next Actions:
1. Deploy to OpenAI: Copy project_system_instructions.md + upload documents
2. Deploy to Gemini: Combine documents per .madio configuration
3. Deploy to Claude: Upload to Claude Project with AI_CONTEXT.md
4. Test deployment: Validate all platform integrations
5. Update context: Document deployment status in AI_CONTEXT.md
```

**Production Mode:**
```
📍 Status: MADIO System in Production
🎯 Next Actions:
1. Monitor performance: Check quality gates and user feedback
2. Iterate system: gemini "Improve [aspect] of my AI system"
3. Add capabilities: gemini "Add [new feature] using AI system document templates"
4. Get updates: git pull template main (latest AI system document improvements)
5. New project: Use madio-start template for next AI system
```

### Phase 4: MADIO Context Integration

Based on detected project state, provide MADIO-specific guidance:

```
For any MADIO project:
- Read AI_CONTEXT.md for complete project context
- Check madio_core_templates.md for template guidance
- Review .madio configuration for project settings

For specific stages:
- Setup: Review _project_scaffolding/ contents before /madio-setup
- Generation: Reference _template_library/ for available templates
- Expansion: Check AI_CONTEXT.md for current template selection rationale
- Deployment: Review platform-specific instructions in AI_CONTEXT.md
```

### Phase 5: MADIO Template Status

Show current template usage and availability:

```bash
📚 MADIO Template Status:

✅ Generated Documents:
[List existing AI system documents with their purposes]

🔄 Available Templates:
[List unused templates with brief descriptions and use cases]

📊 Project Complexity: [Simple/Moderate/Complex/Enterprise based on document count]

🎯 Template Recommendations:
[Suggest next templates based on current system and common patterns]
```

## Output Format

```
🔄 CLAUDE CODE + MADIO FRAMEWORK STATUS
Working Directory: [path]
MADIO Setup: [✅ Complete / ❌ Required]
Templates: [14 available / X generated]
Bridge File: [✅ AI_CONTEXT.md / ❌ Missing]

📁 MADIO PROJECT STATE ANALYSIS
Project: [project name from .madio or directory]
Framework Stage: [setup/generation/expansion/deployment/production]
Document Count: [X documents generated]
Complexity Level: [simple/moderate/complex/enterprise]

📍 WHERE YOU ARE
[Clear description of current MADIO development position]

🎯 YOUR NEXT BEST MADIO OPTIONS
1. [Action 1 with exact Gemini CLI command]
2. [Action 2 with exact command]
3. [Action 3 with exact command]
4. [Action 4 with exact command]

📚 MADIO TEMPLATE INSIGHTS
Current System: [description based on generated AI system documents]
Available Templates: [count] unused AI system document templates ready for integration
Recommended Next: [specific template suggestions]

💡 NEED MORE HELP?
- Read AI_CONTEXT.md for complete project context
- Check madio_core_templates.md for template guidance
- Run /madio-setup if framework not initialized
- Use Gemini CLI for AI system generation
- Get updates: git pull template main
```

## MADIO-Specific Features

### **Template Intelligence**
- Analyzes current document hierarchy for gaps
- Suggests complementary templates based on existing system
- Identifies complexity escalation opportunities
- Recommends template combinations for common use cases

### **Bridge File Integration**
- Reads AI_CONTEXT.md for accumulated project knowledge
- Shows recent development activity and decisions
- Displays template selection rationale
- Indicates deployment status and platform configurations

### **Quality Assessment**
- Validates document hierarchy integrity
- Checks for placeholder completion
- Identifies cross-reference gaps
- Suggests quality improvement actions

### **Framework Evolution**
- Shows available AI system document template updates from madio-start
- Indicates when AI system document framework improvements are available
- Guides AI system document template update integration process
- Preserves custom adaptations during updates

## Notes

- This command works regardless of MADIO project state
- Always provides actionable next steps with exact CLI commands
- Emphasizes MADIO framework capabilities and systematic approach
- Integrates with AI_CONTEXT.md for project continuity
- Supports both Gemini CLI and Claude Code workflows
