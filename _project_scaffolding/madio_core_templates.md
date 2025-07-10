# MADIO Core AI System Document Templates

## OVERVIEW
This document serves as the authoritative AI system document template library for the MADIO (Modular AI Declarative Instruction and Orchestration) framework. All MADIO projects must be built using these AI system document templates to ensure consistency, maintainability, and proper hierarchical authority structure.

## CRITICAL USAGE INSTRUCTION
When creating a new MADIO project, the AI system MUST:
1. Reference this AI system document template library located in `_template_library/`
2. Use the appropriate AI system document templates based on project complexity
3. Replace ALL placeholder text `[LIKE_THIS]` with project-specific content
4. Maintain the hierarchical authority structure (Tier 1 → Tier 2 → Tier 3)

## FILE NAMING CONVENTION
All MADIO AI system document template files follow this strict naming pattern:
madio_template_[tier]_[document_name].md

## AI SYSTEM DOCUMENT TEMPLATE LIBRARY LOCATION
All AI system document templates are stored in the `_template_library/` directory:
_template_library/
├── madio_template_tier1_project_system_instructions.md
├── madio_template_tier2_orchestrator.md
├── madio_template_tier3_character_voice_authority.md
├── madio_template_tier3_content_operations.md
├── madio_template_tier3_document_reference_map.md
├── madio_template_tier3_implementation_roadmap.md
├── madio_template_tier3_methodology_framework.md
├── madio_template_tier3_research_protocols.md
├── madio_template_tier3_rubrics_evaluation.md
├── madio_template_tier3_standard_content.md
├── madio_template_tier3_strategic_framework.md
├── madio_template_tier3_visual_asset_generation.md
└── madio_template_tier3_visual_design_standards.md

## HIERARCHICAL AI SYSTEM DOCUMENT TEMPLATE STRUCTURE

### TIER 1: PROJECT AUTHORITY (Mandatory)
**Template:** `madio_template_tier1_project_system_instructions.md`
- **Purpose:** Core AI agent instructions that power the CustomGPT/Gem/Claude Project
- **Authority:** SUPREME - Overrides all other documents
- **Key Sections:**
  - Core Project Identity
  - Operational Authority Structure
  - Non-Negotiable Quality Standards
  - Execution Guardrails
  - Integration Requirements
  - Success Metrics
  - Deployment Configuration

### TIER 2: EXECUTION CONTROL (Mandatory)
**Template:** `madio_template_tier2_orchestrator.md`
- **Purpose:** Main workflow controller with step-by-step methodology
- **Authority:** WORKFLOW - Controls execution sequence and quality gates
- **Version:** 1.1 (Enhanced with cross-document integration and layered reporting)
- **Reports To:** project_system_instructions
- **Key Sections:**
  - Execution Methodology
  - Main Workflow Sequence (8 steps for analysis projects)
  - Cross-Document Integration & Reporting
  - Quality Assurance Framework
  - Decision Logic
  - Error Handling Protocols

### TIER 3: SUPPORTING SPECIFICATIONS (As Needed)

#### Content Generation & Character Templates

##### Character Voice Authority
**Template:** `madio_template_tier3_character_voice_authority.md`
- **Purpose:** Define character personalities, speech patterns, and voice consistency
- **Use When:** Project involves character-driven content or multiple personas
- **Reports To:** orchestrator

##### Content Operations Manual
**Template:** `madio_template_tier3_content_operations.md`
- **Purpose:** Content validation, diversity systems, and approved content directories
- **Use When:** Project requires content curation, validation, or variety enforcement
- **Reports To:** orchestrator

##### Standard Content Template
**Template:** `madio_template_tier3_standard_content.md`
- **Purpose:** Standardized output format for consistent content generation
- **Use When:** Project produces templated content (episodes, reports, articles)
- **Reports To:** orchestrator

#### Analysis & Evaluation Templates

##### Methodology Framework
**Template:** `madio_template_tier3_methodology_framework.md`
- **Purpose:** Systematic 8-step methodology for complex analysis projects
- **Use When:** Conducting comprehensive analysis, evaluation, or assessment
- **Reports To:** orchestrator
- **Key Features:** Discovery → Analysis → Solution → Implementation phases

##### Rubrics Evaluation
**Template:** `madio_template_tier3_rubrics_evaluation.md`
- **Purpose:** Multi-dimensional evaluation framework with 4-level rating system
- **Use When:** Need standardized assessment criteria across multiple dimensions
- **Reports To:** orchestrator
- **Key Features:** Exceptional/Competent/Needs Improvement/Critical Gap ratings

##### Strategic Framework
**Template:** `madio_template_tier3_strategic_framework.md`
- **Purpose:** Identify non-obvious strategic opportunities and breakthrough insights
- **Use When:** Strategic positioning assessment or opportunity identification needed
- **Reports To:** orchestrator
- **Key Features:** 6 core strategic elements for comprehensive assessment

#### Research & Implementation Templates

##### Research Protocols
**Template:** `madio_template_tier3_research_protocols.md`
- **Purpose:** Systematic evidence collection and data gathering procedures
- **Use When:** Research-intensive projects requiring rigorous documentation
- **Reports To:** orchestrator
- **Key Features:** Asset auditing, search queries, AI-guided extraction

##### Implementation Roadmap
**Template:** `madio_template_tier3_implementation_roadmap.md`
- **Purpose:** Phased execution planning with deliverables and metrics
- **Use When:** Translating recommendations into actionable project plans
- **Reports To:** orchestrator
- **Key Features:** Multi-phase structure with owners, dependencies, metrics

#### Visual & System Templates

##### Visual Asset Generation
**Template:** `madio_template_tier3_visual_asset_generation.md`
- **Purpose:** Automated visual content generation specifications
- **Use When:** Project requires AI-generated images, thumbnails, or visual assets
- **Reports To:** orchestrator

##### Visual Design Standards
**Template:** `madio_template_tier3_visual_design_standards.md`
- **Purpose:** Brand identity, visual consistency, and design specifications
- **Use When:** Project has specific visual/brand requirements
- **Reports To:** orchestrator

##### Document Reference Map
**Template:** `madio_template_tier3_document_reference_map.md`
- **Purpose:** Complete system architecture and integration validation
- **Use When:** Complex projects with 5+ documents requiring integration mapping
- **Reports To:** orchestrator

## PROJECT COMPLEXITY GUIDELINES

### Simple Projects (3-4 documents total)
**Required:**
- Tier 1: project_system_instructions
- Tier 2: orchestrator
**Optional (choose 1-2):**
- Tier 3: 1-2 supporting documents based on needs

### Moderate Projects (5-7 documents total)
**Required:**
- Tier 1: project_system_instructions
- Tier 2: orchestrator
**Recommended:**
- Tier 3: content_operations
- Tier 3: 2-4 additional supporting documents

### Complex Projects (8-10 documents total)
**Required:**
- Tier 1: project_system_instructions
- Tier 2: orchestrator (v1.1 recommended for analysis projects)
- Tier 3: document_reference_map
**Recommended:**
- Tier 3: methodology_framework (for analysis projects)
- Tier 3: 4-7 additional supporting documents

### Enterprise Projects (10+ documents)
**Required:**
- All Tier 1 and Tier 2 templates
- Tier 3: document_reference_map (critical for integration)
- Tier 3: content_operations or methodology_framework
**Recommended:**
- All relevant Tier 3 templates
- Custom Tier 3 documents as needed

## TEMPLATE BUNDLES FOR COMMON USE CASES

### Content Generation Bundle
- project_system_instructions + orchestrator
- character_voice_authority
- content_operations
- standard

### Analysis & Evaluation Bundle
- project_system_instructions + orchestrator (v1.1)
- methodology_framework
- rubrics_evaluation
- strategic_framework
- implementation_roadmap

### Research Project Bundle
- project_system_instructions + orchestrator
- research_protocols
- methodology_framework
- document_reference_map

### Visual Content Bundle
- project_system_instructions + orchestrator
- visual_design_standards
- visual_asset_generation
- content_operations

## TEMPLATE USAGE WORKFLOW

### Step 1: Determine Project Complexity
Assess the project requirements to determine complexity level and required documents.

### Step 2: Copy Required Templates
1. Always start with `madio_template_tier1_project_system_instructions.md`
2. Always include `madio_template_tier2_orchestrator.md`
3. Add Tier 3 templates based on project needs

### Step 3: Customize Templates
1. Replace ALL `[PLACEHOLDER]` text with project-specific content
2. Remove unused sections that don't apply
3. Add additional steps/sections as needed
4. Maintain hierarchical references

### Step 4: Validate Integration
1. Ensure all document cross-references are accurate
2. Verify authority hierarchy is maintained
3. Check that orchestrator references all Tier 3 documents
4. Confirm no circular dependencies exist

### Step 5: Platform Deployment
- **OpenAI CustomGPT:** Use project_system_instructions as main instructions
- **Google Gemini Gem:** Combine core documents into Gem's system prompt
- **Claude Project:** Use project_system_instructions as Claude Project instructions
- **All Platforms:** Include all documents in knowledge base

## QUALITY CHECKLIST
Before finalizing any MADIO project:
- [ ] All placeholder text replaced with specific content
- [ ] Document hierarchy properly established
- [ ] All referenced documents exist and are named correctly
- [ ] Quality gates defined with measurable criteria
- [ ] Error handling covers identified risks
- [ ] Integration points clearly specified
- [ ] Success metrics are quantifiable
- [ ] No circular dependencies in document references
- [ ] Authority chain flows correctly (Tier 1 → Tier 2 → Tier 3)

## TEMPLATE MODIFICATION RULES
1. **Never modify** the authority hierarchy structure
2. **Never create** circular references between documents
3. **Always maintain** the reporting relationships
4. **Always ensure** Tier 1 has supreme authority
5. **Always validate** cross-document references

## QUICK REFERENCE: TEMPLATE SELECTION MATRIX

| Project Type | Required Templates | Recommended Tier 3 Templates |
|-------------|-------------------|------------------------------|
| AI Assistant | Tier 1 & 2 | character_voice_authority |
| Content Generator | Tier 1 & 2 | standard, content_operations |
| Visual Content | Tier 1 & 2 | visual_design_standards, visual_asset_generation |
| Complex Workflow | Tier 1 & 2 | document_reference_map, content_operations |
| Character-Driven | Tier 1 & 2 | character_voice_authority, standard |
| Analysis System | Tier 1 & 2 (v1.1) | methodology_framework, rubrics_evaluation, strategic_framework |
| Research Project | Tier 1 & 2 | research_protocols, methodology_framework |
| Implementation | Tier 1 & 2 | implementation_roadmap, methodology_framework |
| Enterprise System | All Tier 1 & 2 | All relevant Tier 3 templates |

## INTEGRATION WITH PROJECT_SYSTEM_INSTRUCTIONS
When the AI system receives a request to create a new MADIO project:
1. It MUST consult this template library
2. It MUST use the templates from `_template_library/`
3. It MUST follow the hierarchical structure defined here
4. It MUST ensure all placeholders are replaced with project-specific content

---

**REMEMBER:** This template library is the foundation of the MADIO framework. Every MADIO project must be built using these templates to ensure systematic design, maintainability, and production-ready quality. The modular approach allows for scalability while maintaining consistency across all implementations.