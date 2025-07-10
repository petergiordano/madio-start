<!-- 
MADIO TEMPLATE FILE - Contains placeholder values in square brackets
These are intentionally incomplete markdown links that get replaced during setup
-->

# AI_CONTEXT.md - Project Bridge File

> **Purpose:** This file provides seamless context transfer between local CLI development and deployed AI systems.

## PROJECT OVERVIEW

**Project Name:** [PROJECT_NAME]
**Project Type:** [PROJECT_TYPE]
**Complexity Level:** [simple|moderate|complex|enterprise]
**Created:** [CREATION_DATE]
**Last Updated:** [CURRENT_DATE]

**Project Description:**
[Brief description of what this AI system does and its primary purpose]

**Target Deployment:**
- [ ] OpenAI CustomGPT
- [ ] Google Gemini Gem  
- [ ] Claude Project
- [ ] Other: [SPECIFY]

## CURRENT STATUS

**Development Phase:** [setup|generation|customization|testing|deployment|production]

**Recent Activity:**
- [TIMESTAMP] - [Recent development activity]
- [TIMESTAMP] - [Recent changes or decisions]
- [TIMESTAMP] - [Important updates or modifications]

**Next Steps:**
1. [Immediate next action needed]
2. [Following priority task]
3. [Future consideration]

## DOCUMENT ARCHITECTURE

### Generated AI System Documents
**Tier 1 (Authority):**
- `project_system_instructions.md` - [Status: generated|customized|finalized]

**Tier 2 (Orchestration):**
- `orchestrator.md` - [Status: generated|customized|finalized]

**Tier 3 (Supporting AI System Documents):**
- `[document_name].md` - [Purpose] - [Status]
- `[document_name].md` - [Purpose] - [Status]
- `[document_name].md` - [Purpose] - [Status]

### Document Relationships
```
project_system_instructions (Tier 1)
├── orchestrator (Tier 2)
│   ├── [supporting_doc_1] (Tier 3)
│   ├── [supporting_doc_2] (Tier 3)
│   └── [supporting_doc_3] (Tier 3)
└── Quality Gates & Validation
```

## KEY DECISIONS & ARCHITECTURE

### Design Decisions Made
1. **[Decision Topic]**: [Decision made and rationale]
2. **[Decision Topic]**: [Decision made and rationale]
3. **[Decision Topic]**: [Decision made and rationale]

### Template Selection Rationale
**Chosen Templates:**
- `[template_name]` - Selected because [reason]
- `[template_name]` - Selected because [reason]
- `[template_name]` - Selected because [reason]

**Templates Considered but Not Used:**
- `[template_name]` - Not needed because [reason]
- `[template_name]` - Complexity doesn't warrant inclusion

### Custom Adaptations
- **[Adaptation Area]**: [What was customized and why]
- **[Adaptation Area]**: [What was customized and why]

## DEVELOPMENT NOTES

### Challenges Encountered
1. **[Challenge]**: [How it was addressed]
2. **[Challenge]**: [How it was addressed]

### Lessons Learned
1. **[Insight]**: [What was learned and implications]
2. **[Insight]**: [What was learned and implications]

### Technical Considerations
- **Integration Points**: [Key areas where documents interconnect]
- **Quality Gates**: [Validation mechanisms implemented]
- **Error Handling**: [How errors and edge cases are managed]

## DEPLOYMENT CONFIGURATION

### Platform-Specific Notes

**OpenAI CustomGPT Deployment:**
- Main Instructions: Use `project_system_instructions.md`
- Knowledge Base: Upload [list of documents]
- Special Considerations: [Any platform-specific adaptations]

**Google Gemini Gem Deployment:**
- System Prompt: Combine [specify documents]
- Context Window: [Token considerations]
- Model Settings: [Temperature, max tokens, etc.]

**Claude Project Deployment:**
- Project Instructions: Use `project_system_instructions.md`
- Project Knowledge: Upload [list of documents]
- Integration Notes: [Claude-specific considerations]

### Quality Validation Checklist
- [ ] All placeholders replaced with project-specific content
- [ ] Document hierarchy maintains clear authority chain
- [ ] Cross-references between documents function correctly
- [ ] Quality gates operational and tested
- [ ] Error handling covers identified edge cases

## CONTEXT FOR AI COLLABORATION

### For Local CLI Tools (Gemini CLI, Claude Code)
**Current Working Directory:** `[PROJECT_PATH]`
**Available Commands:**
- `gemini "[request]"` - Document generation and updates
- Claude Desktop - File reading, validation, refinement

**Key Files to Reference:**
- `_template_library/` - Template reference materials
- `madio_core_templates.md` - Template selection guide
- `.madio` - Project configuration
- Generated MADIO documents in project root

### For Browser/App AI Systems
**When copying this context to deployed AI:**

1. **Project Understanding**: [Summarize what this AI system does]
2. **Document Hierarchy**: [Explain the relationship between documents]
3. **Key Constraints**: [Important limitations or requirements]
4. **Quality Standards**: [Expected output quality and validation]
5. **User Interaction Model**: [How users should interact with the system]

### Recent Conversation Context
**Last CLI Session Focus:**
[Summary of recent development work, decisions made, or issues resolved]

**Outstanding Questions:**
1. [Question that needs resolution]
2. [Decision point requiring input]
3. [Area needing further development]

## SYSTEM METADATA

**MADIO Framework Version:** 1.0.0
**Template Library Version:** [VERSION]
**Git Repository:** [REPO_URL]
**Local Path:** [LOCAL_PROJECT_PATH]

**Last CLI Update:** [TIMESTAMP]
**Last Deployment:** [TIMESTAMP] - [PLATFORM]

---

**Usage Instructions:**
1. **Local Development**: Keep this file updated via CLI tools
2. **Deployment Transfer**: Copy relevant sections to deployed AI context
3. **Continuity**: Use this file to maintain context across sessions
4. **Collaboration**: Share with team members for project understanding

**Auto-Update Commands:**
```bash
# Update with recent changes
gemini "Update AI_CONTEXT.md with recent project changes and current status"

# Prepare for deployment
gemini "Generate deployment summary for AI_CONTEXT.md"
```