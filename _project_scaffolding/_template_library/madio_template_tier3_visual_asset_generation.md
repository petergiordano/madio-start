# [PROJECT_NAME]: Visual Asset Generation Authority

**Document Authority:** TIER 3 - SUPPORTING SPECIFICATION
**Document Type:** visual_asset_generation
**Version:** 1.0
**Created:** [DATE]
**Last Modified:** [DATE]
**Reports To:** orchestrator

---

## SYSTEM INTEGRATION PROTOCOL

### Orchestrator Call Interface
**When Called:** [Specific orchestrator step - e.g., "After Step X completion"]
**Data Required:** [Content metadata needed including:]
- [CONTENT_ELEMENT_1] and [ATTRIBUTE]
- [CONTENT_ELEMENT_2] and [ATTRIBUTE]
- [SETTING/ENVIRONMENT] description
- [HOOK/TITLE] text
- [IDENTIFIER] ([FORMAT] format)

**Output Delivered:** Complete [ASSET_TYPE] generation prompt ready for AI [GENERATION_TYPE]

### Data Extraction Protocol
**From [SOURCE_1]:**

- [DATA_FIELD_1]: [Extract specific information]
- [DATA_FIELD_2]: [Extract specific information]
- [DATA_FIELD_3]: [Extract specific information]


**From [SOURCE_2]:**

- [DATA_FIELD_4]: [Extract specific information]
- [DATA_FIELD_5]: [Extract specific information]
- [DATA_FIELD_6]: [Extract specific information]


---

## [CONTENT_TYPE] SPECIFICATION DATABASE

### [CATEGORY_1] FAMILY

**Anatomical/Structural Requirements:**
- **[COMPONENT_1]:** [Detailed specifications - size, position, characteristics]
- **[COMPONENT_2]:** [Detailed specifications - size, position, characteristics]
- **[COMPONENT_3]:** [Detailed specifications - size, position, characteristics]
- **[COMPONENT_4]:** [Detailed specifications - size, position, characteristics]
- **PROHIBITED:** [List forbidden elements - incorrect features, incompatible characteristics]
- **[DISTINCTIVE_FEATURE]:** [Unique identifying characteristics]
- **[POSITIONING_RULE]:** [How element should be positioned/oriented]

**[SUBCATEGORY] Variants:**
- **[VARIANT_1]:** [Specific modifications to base requirements]
- **[VARIANT_2]:** [Specific modifications to base requirements]
- **[VARIANT_3]:** [Specific modifications to base requirements]

### [CATEGORY_2] FAMILY

[Repeat same structure for each major category]

### [CATEGORY_N] FAMILY

**General Requirements:**
- **[UNIVERSAL_COMPONENT_1]:** [Specifications applying to all variants]
- **[UNIVERSAL_COMPONENT_2]:** [Specifications applying to all variants]
- **[SIZE_PARAMETER]:** [Size specifications appropriate to type/variant]
- **PROHIBITED:** [Universal forbidden elements for this category]

**By [CLASSIFICATION_SYSTEM]:**
- **[TYPE_1]:** [Specific characteristics and requirements]
- **[TYPE_2]:** [Specific characteristics and requirements]
- **[TYPE_3]:** [Specific characteristics and requirements]

---

## MASTER PROMPT TEMPLATE

### Template Structure

Create [ASSET_TYPE] for [PROJECT_NAME] following these EXACT specifications:

**[CONTENT] DETAILS:**
- [IDENTIFIER]: "[IDENTIFIER_FORMAT]"
- [CONTENT_ELEMENTS]: [ELEMENT_A] vs. [ELEMENT_B]
- [SETTING]: [ENVIRONMENT_DESCRIPTION]

**TECHNICAL SPECS:**
- [DIMENSION_1]x[DIMENSION_2] pixels, [OPTIMIZATION_TARGET] design
- [ART_STYLE] ([QUALITY_REFERENCE])
- [COLOR_CHARACTERISTICS]
- [DEPTH_REQUIREMENTS]

**LAYOUT REQUIREMENTS:**
- [SECTION_1] [PERCENTAGE]%: [CONTENT_DESCRIPTION] - no text overlap
- [SECTION_2] [PERCENTAGE]%: [CONTENT_DESCRIPTION] with [BACKGROUND_TREATMENT]
- [SEPARATOR_ELEMENT]: [VISUAL_SEPARATOR_DESCRIPTION]

**CRITICAL [CONTENT_TYPE] SPECIFICATIONS ([SECTION] Only):**

**[CONTENT_ELEMENT_A] ([POSITION]):**
[CONTENT_A_SPECIFICATIONS]

**[CONTENT_ELEMENT_B] ([POSITION]):**
[CONTENT_B_SPECIFICATIONS]

**TYPOGRAPHY ([SECTION] Only):**
- [TEXT_TYPE_1]: "[TEXT_CONTENT]" - [SIZE]pt [STYLE] [COLOR] with [TREATMENT]
- [TEXT_TYPE_2]: "[TEXT_CONTENT]" - [SIZE]pt [STYLE] [COLOR]
- [TEXT_TYPE_3]: "[TEXT_CONTENT]" - [SIZE]pt [STYLE], [POSITION]
- ALL text must have [ENHANCEMENT] for [READABILITY_TARGET]

**[ENVIRONMENT] ([SECTION] Background):**
[ENVIRONMENT_SPECIFICATIONS]
- [LIGHTING_REQUIREMENTS]
- [ATMOSPHERIC_ELEMENTS]
- [DEPTH_CREATION_RULES]

**COLOR PALETTE:**
- [COLOR_CATEGORY_1]: [COLOR_SPECIFICATIONS]
- [COLOR_CATEGORY_2]: [COLOR_SPECIFICATIONS]
- [COLOR_CATEGORY_3]: [COLOR_SPECIFICATIONS]
- [EFFECTS_COLORS]: [SPECIAL_COLOR_REQUIREMENTS]

**QUALITY VALIDATION:**
- [CONTENT_ELEMENT_A] MUST follow exact [SPECIFICATION_TYPE] - [CRITICAL_CONSTRAINT_A]
- [CONTENT_ELEMENT_B] MUST follow exact [SPECIFICATION_TYPE] - [CRITICAL_CONSTRAINT_B]
- [READABILITY_REQUIREMENT] with [ENHANCEMENT_SPECIFICATION]
- [POSITIONING_REQUIREMENT] with clear separation
- [VISUAL_QUALITY_REQUIREMENT]
- [SEPARATOR_REQUIREMENT]


### Variable Substitution System

**[CONTENT] Data Variables:**
- `[IDENTIFIER_VARIABLE]` → "[EXAMPLE_FORMAT]"
- `[HOOK_VARIABLE]` → "[EXAMPLE_HOOK_TEXT]"
- `[CONTENT_ELEMENT_A]` → "[EXAMPLE_ELEMENT_A]"
- `[CONTENT_ELEMENT_B]` → "[EXAMPLE_ELEMENT_B]"
- `[ENVIRONMENT_VARIABLE]` → "[EXAMPLE_ENVIRONMENT_DESCRIPTION]"

**[SPECIFICATION] Variables:**
- `[CONTENT_A_SPECS_VARIABLE]` → Pull from [Content Database]
- `[CONTENT_B_SPECS_VARIABLE]` → Pull from [Content Database]
- `[CRITICAL_CONSTRAINT_A]` → Key [requirement] for [Content Element A]
- `[CRITICAL_CONSTRAINT_B]` → Key [requirement] for [Content Element B]

**Environment Variables:**
- `[ENVIRONMENT_DETAILS_VARIABLE]` → Extracted from [source]
- `[ENVIRONMENT_COLORS_VARIABLE]` → Color palette matching environment type
- `[LIGHTING_SOURCE_VARIABLE]` → Primary light source for scene
- `[CONTENT_LIGHTING_VARIABLE]` → Special lighting effects for each [content element]

---

## GENERATION EXECUTION PROTOCOL

### Step 1: Data Extraction
1. **Extract [Content] Metadata:** Pull [identifier], [hook], [content] names
2. **Extract Environment Data:** Pull [setting] location and atmospheric details
3. **Validate Data Completeness:** Ensure all required variables present

### Step 2: [Content] Specification Lookup
1. **Identify [Content] Types:** Match [content] names to [specification] database entries
2. **Retrieve [Structural] Requirements:** Pull complete specifications for both [content elements]
3. **Generate Constraint Lists:** Create critical requirement lists for validation
4. **Handle Unknown [Content]:** Flag for manual review if [content] not in database

### Step 3: Prompt Assembly
1. **Load Master Template:** Use complete prompt template structure
2. **Substitute Variables:** Replace all placeholder variables with extracted data
3. **Apply Design Standards:** Ensure compliance with [visual_design_standards]
4. **Format for Generation:** Prepare final prompt for AI [asset] generation

### Step 4: Quality Pre-Validation
1. **Template Completeness:** Verify no placeholder variables remain
2. **[Specification] Accuracy:** Confirm [content] specifications are [standard] compliant
3. **Brand Consistency:** Validate design elements match visual standards
4. **[Optimization] Requirements:** Ensure [sizing/contrast/formatting] requirements met

### Step 5: Prompt Delivery
1. **Format Output:** Provide complete, ready-to-use generation prompt
2. **Include Validation Checklist:** Provide post-generation quality criteria
3. **Document Source Data:** Note which [content] data was used for traceability

---

## ENVIRONMENT SPECIFICATION SYSTEM

### [ENVIRONMENT_TYPE_1] Environments
**Color Palette:** [COLOR_DESCRIPTIONS_WITH_HEX_CODES]
**Lighting:** [LIGHTING_CHARACTERISTICS]
**Details:** [ENVIRONMENTAL_ELEMENTS]
**Atmosphere:** [ATMOSPHERIC_EFFECTS]

### [ENVIRONMENT_TYPE_2] Environments
**Color Palette:** [COLOR_DESCRIPTIONS_WITH_HEX_CODES]
**Lighting:** [LIGHTING_CHARACTERISTICS]
**Details:** [ENVIRONMENTAL_ELEMENTS]
**Atmosphere:** [ATMOSPHERIC_EFFECTS]

### [ENVIRONMENT_TYPE_3] Environments
**Color Palette:** [COLOR_DESCRIPTIONS_WITH_HEX_CODES]
**Lighting:** [LIGHTING_CHARACTERISTICS]
**Details:** [ENVIRONMENTAL_ELEMENTS]
**Atmosphere:** [ATMOSPHERIC_EFFECTS]

### [ENVIRONMENT_TYPE_4] Environments
**Color Palette:** [COLOR_DESCRIPTIONS_WITH_HEX_CODES]
**Lighting:** [LIGHTING_CHARACTERISTICS]
**Details:** [ENVIRONMENTAL_ELEMENTS]
**Atmosphere:** [ATMOSPHERIC_EFFECTS]

### [ENVIRONMENT_TYPE_5] Environments
**Color Palette:** [COLOR_DESCRIPTIONS_WITH_HEX_CODES]
**Lighting:** [LIGHTING_CHARACTERISTICS]
**Details:** [ENVIRONMENTAL_ELEMENTS]
**Atmosphere:** [ATMOSPHERIC_EFFECTS]

---

## [ASSET_TYPE] QUALITY VALIDATION

### Technical Compliance Checklist
- [ ] Resolution exactly [DIMENSION_1]x[DIMENSION_2] pixels
- [ ] [SPLIT_RATIO] layout split maintained precisely
- [ ] [SEPARATOR_ELEMENT] prominent and positioned correctly
- [ ] [OVERLAY_ELEMENT] at [OPACITY]% opacity for readability
- [ ] All text elements properly sized for [TARGET_VIEWING]

### Brand Consistency Checklist
- [ ] "[SERIES_IDENTIFIER]" [brand_element] in [style_specification]
- [ ] [IDENTIFIER_ELEMENT] in correct "[FORMAT]" format
- [ ] Color palette matches [visual_design_standards] specifications
- [ ] [ART_STYLE] maintained
- [ ] [CONTRAST_REQUIREMENT] achieved for [optimization_target]

### [CONTENT_TYPE] Accuracy Checklist
- [ ] [Content Element A] matches exact [specification] requirements from database
- [ ] [Content Element B] matches exact [specification] requirements from database
- [ ] No prohibited features present on either [content element]
- [ ] [Content] positioning and scale appropriate to types
- [ ] All critical constraints verified against generation output

### Environmental Quality Checklist
- [ ] Background shows clear [depth/perspective] effects
- [ ] Environment matches [content setting] accurately
- [ ] Lighting effects support mood and [content] visibility
- [ ] [Environmental elements] visible but not overwhelming
- [ ] [Thematic elements] appropriate to [project setting]

### Production Readiness Checklist
- [ ] [Asset] ready for immediate [usage context]
- [ ] No manual corrections required for brand compliance
- [ ] Consistent with previous [assets] in series
- [ ] Professional [quality level] achieved
- [ ] [Optimization target] optimized for maximum [effectiveness metric]

---

## ERROR HANDLING PROTOCOLS

### Missing [Content] in Database
**Detection:** [Content] name not found in [specification] database
**Response:**
1. Flag for manual review and database update
2. Use generic [category] constraints as temporary measure
3. Document new [content] requirements for database expansion
4. Escalate to [content_operations] for [content] verification

### Environment Data Insufficient
**Detection:** [Setting] location lacks detailed environmental description
**Response:**
1. Use [content]'s [context] location as basis
2. Apply standard environment template for location type
3. Default to [default_environment] template if unclear
4. Ensure [depth/atmospheric] requirements met regardless

### [Content] Data Incomplete
**Detection:** Required variables missing from [content] metadata
**Response:**
1. Check [content] sections [X-Y] for missing information
2. Generate placeholder values maintaining format consistency
3. Flag incomplete data for quality review process
4. Proceed with available data to avoid generation failure

### Template Variable Errors
**Detection:** Placeholder variables remain after substitution
**Response:**
1. Identify which data extraction failed
2. Apply default values for missing variables
3. Document error for system improvement
4. Complete generation with best available information

---

## INTEGRATION TESTING PROTOCOL

### System Integration Validation
1. **Call Interface Test:** Verify orchestrator can successfully call [visual_asset_generation]
2. **Data Flow Test:** Confirm [content] metadata flows correctly into [asset] generation
3. **Output Format Test:** Ensure generated prompts are properly formatted
4. **Quality Gate Test:** Validate [asset] output meets all compliance criteria

### Cross-Document Consistency Test
1. **Visual Standards Compliance:** Verify adherence to [visual_design_standards]
2. **Brand Element Consistency:** Confirm [series] logo and layout specifications
3. **Technical Specification Accuracy:** Check all technical requirements met
4. **[Content] Accuracy Validation:** Verify [content_standard] compliance against [content_operations]

### Automation Readiness Test
1. **No Manual Intervention Required:** Confirm fully automated operation
2. **Error Recovery Functional:** Test all error handling protocols
3. **Quality Assurance Automatic:** Verify validation checklists work correctly
4. **Production Pipeline Ready:** Confirm integration with [orchestrator step] workflow

---

## FUTURE ENHANCEMENT FRAMEWORK

### [Content] Database Expansion
- **Addition Protocol:** New [content] added with complete [specification] requirements
- **Verification Process:** Cross-reference with [authoritative_source] for accuracy
- **Testing Requirements:** Validate new entries with generation tests
- **Documentation Standards:** Maintain consistent specification format

### Environment Library Growth
- **New Location Templates:** Additional [project_setting] locations with detailed specifications
- **[Variation] Considerations:** [Context variations] like weather, time, seasonal effects
- **[Feature] Library:** Reusable [environmental elements] for different environments
- **[Effect] Database:** Standard [effect] setups for various conditions

### Template Evolution
- **Version Control:** Track changes to master template for consistency
- **A/B Testing Framework:** Test template improvements against current standards
- **Performance Optimization:** Refine prompts for better AI generation accuracy
- **Quality Metric Tracking:** Monitor generation success rates and consistency

---

**Remember:** This document ensures every [PROJECT_NAME] [asset] maintains professional consistency while automatically adapting to [content]-specific requirements. The modular approach allows for system growth and refinement while preserving the brand integrity essential for audience recognition and automation success.

---
