# Gemini Context: Creating MADIO Templates from MEA

## Your Role
You are helping build the MADIO (Modular AI Declarative Instruction and Orchestration) framework by generalizing patterns from a Marketing Effectiveness Analysis (MEA) project into reusable templates.

## What is MADIO?
MADIO is a framework that enables anyone to program complex AI applications using structured English. It creates hierarchical document systems that power:
- OpenAI CustomGPTs
- Google Gemini Gems  
- Claude Projects

## MADIO's Hierarchical Structure
- **Tier 1**: Project Authority (supreme authority, overrides all)
- **Tier 2**: Execution Orchestrator (controls workflow and quality gates)
- **Tier 3**: Supporting Specifications (detailed rules, templates, validation)

## The MEA Reference Project
The Marketing Effectiveness Analysis (MEA) is a complex project we're using as a template source. It:
- Analyzes B2B SaaS marketing across 9 dimensions
- Uses an 8-step systematic methodology
- Includes detailed rubrics, frameworks, and cross-references
- Demonstrates best practices for complex analysis projects

## Your Task
Transform MEA's specific patterns into generalized MADIO templates that work for ANY type of project, not just marketing analysis.

## Key Principles
1. **Generalize, Don't Copy**: Replace marketing-specific content with [PLACEHOLDERS]
2. **Preserve Structure**: Keep the systematic approach and cross-references
3. **Maintain Hierarchy**: Respect Tier 1 → Tier 2 → Tier 3 authority
4. **Enable Reuse**: Templates must work for analysis, implementation, or evaluation projects

## Template Requirements
Every MADIO template must include:
```markdown
# [TEMPLATE_NAME]

## OVERVIEW
This document serves as [PURPOSE]. It is a Tier [N] document in the MADIO framework hierarchy.

## CRITICAL USAGE INSTRUCTION
When creating a new [PROJECT_TYPE] project, the AI system MUST:
1. Reference this template
2. Replace ALL placeholder text `[LIKE_THIS]` with project-specific content
3. Maintain the hierarchical authority structure

## HIERARCHICAL CONTEXT
- **Document Type**: Tier [N] - [Authority Level]
- **Reports To**: [Superior Document] (if Tier 2 or 3)
- **Authority Over**: [Subordinate Documents] (if Tier 1 or 2)

## WHEN TO USE
This template is appropriate when:
- [Use case 1]
- [Use case 2]
- [Use case 3]

## INTEGRATION REQUIREMENTS
This document integrates with:
- [Document 1]: [How they work together]
- [Document 2]: [Integration points]

## [MAIN CONTENT SECTIONS]
[Template specific content with [PLACEHOLDERS]]

## SUCCESS METRICS
- [Metric 1]
- [Metric 2]
- [Metric 3]

## QUALITY CHECKLIST
Before finalizing:
- [ ] All placeholders replaced
- [ ] Cross-references verified
- [ ] Authority hierarchy maintained
- [ ] Integration points documented
```

## File Naming Convention
All templates must be named: `madio_template_tier[N]_[description].md`

Examples:
- madio_template_tier1_project_system_instructions.md
- madio_template_tier2_orchestrator.md
- madio_template_tier3_methodology_framework.md

## Reference Files Location
MEA reference documents are in: `/reference-docs/mea/`
- System_Instructions.md → Becomes Tier 1 template
- Instruct_Marketing_Analysis.md → Becomes Tier 2 template
- Marketing_Analysis_Methodology.md → Becomes Tier 3 template
- Marketing_Analysis_Rubrics.md → Becomes Tier 3 template
- Strategic_Elements_Framework.md → Becomes Tier 3 template

## Remember
You're building a framework that enables natural language programming through AI. Every template should advance this goal by being:
- Clear and systematic
- Reusable across domains
- Properly integrated with other templates
- Focused on producing production-ready results