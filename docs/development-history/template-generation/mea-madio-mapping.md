# MEA to MADIO Reference Mapping

## Document Mapping

### File Locations
All MEA reference documents are located in: `/reference-docs/mea/`

### Document Name Mappings

| MEA Document Name | MEA Filename | MADIO Template It Becomes | MADIO Tier |
|------------------|--------------|---------------------------|------------|
| System Instructions | System_Instructions.md | madio_template_tier1_project_system_instructions.md | Tier 1 |
| Instruct_Marketing_Analysis | Instruct_Marketing_Analysis.md | madio_template_tier2_orchestrator.md | Tier 2 |
| Marketing Analysis Methodology | Marketing_Analysis_Methodology.md | madio_template_tier3_methodology_framework.md | Tier 3 |
| Marketing Analysis Rubrics | Marketing_Analysis_Rubrics.md | madio_template_tier3_rubrics_evaluation.md | Tier 3 |
| Strategic Elements Framework | Strategic_Elements_Framework.md | madio_template_tier3_strategic_framework.md | Tier 3 |

## Cross-Reference Translation Guide

When you see these references in MEA documents, translate them for MADIO templates:

### Document References
- "Marketing Analysis Methodology document" → "Methodology Framework document"
- "Marketing Analysis Rubrics document" → "Evaluation Rubrics document"
- "Strategic Elements Framework document" → "Strategic Framework document"
- "Instruct_Marketing_Analysis" → "orchestrator"
- "System Instructions" → "project_system_instructions"

### Section References to Preserve
- Step numbers (e.g., "Step 3 of the methodology")
- Section numbers (e.g., "Section 3.1.5")
- Process phases (e.g., "between Steps 3 and 4")

### Hierarchy References
- MEA has implicit hierarchy → MADIO makes it explicit with Tiers
- "Primary guide" → "Tier 1 authority"
- "Supporting document" → "Tier 3 specification"

## Generalization Rules

When creating MADIO templates from MEA documents:

1. **Replace domain-specific terms:**
   - "marketing effectiveness" → "[DOMAIN] effectiveness"
   - "marketing dimensions" → "[EVALUATION_DIMENSIONS]"
   - "B2B SaaS" → "[INDUSTRY/DOMAIN]"
   - "CMO" → "[TARGET_ROLE]"

2. **Maintain structural patterns:**
   - 8-step methodology → [N]-step methodology
   - 9 dimensions → [N] dimensions
   - 4-level rubrics → [N]-level rubrics

3. **Preserve integration patterns:**
   - Cross-document references
   - Authority hierarchies
   - Quality checkpoints
   - Validation requirements

## Key Patterns to Extract

### From System_Instructions.md:
- Role definition structure
- Authority establishment
- Knowledge integration approach
- Web search requirements
- Output quality standards

### From Instruct_Marketing_Analysis.md:
- Step-by-step orchestration
- Cross-document coordination
- Layered reporting structure
- Evidence requirements
- Business impact focus

### From Marketing_Analysis_Methodology.md:
- Systematic process flow
- Evidence collection protocols
- Synthesis approaches
- Root cause analysis
- Implementation planning

### From Marketing_Analysis_Rubrics.md:
- Multi-level evaluation criteria
- Dimension definition approach
- Cross-dimensional analysis
- Cascade effect documentation

### From Strategic_Elements_Framework.md:
- Strategic opportunity identification
- Cross-functional assessment
- Verification processes
- Integration checkpoints