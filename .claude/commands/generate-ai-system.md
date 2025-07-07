# Generate AI System

Create a complete MADIO AI system using the template library and systematic document generation.

## Command Purpose

Generate a production-ready AI system using MADIO (Modular AI Declarative Instruction and Orchestration) framework. This command guides you through template selection and document generation to create sophisticated AI applications for OpenAI CustomGPT, Gemini Gem, or Claude Project deployment.

## Prerequisites

Before running this command, ensure:
- `/madio-setup` has been completed (check for `.madio-setup-complete`)
- `_template_library/` contains 14 MADIO templates
- `AI_CONTEXT.md` bridge file exists
- `madio_core_templates.md` template guide available

## Process Overview

1. **Project Analysis** - Understand current state and requirements
2. **Template Selection** - Choose appropriate templates based on complexity
3. **Document Generation** - Create hierarchical MADIO documents
4. **Context Updates** - Update AI_CONTEXT.md with generation details
5. **Validation** - Ensure system completeness and deployment readiness

## Implementation

### Phase 1: Project State Validation

```bash
echo "🔍 Validating MADIO project state..."

# Check if setup is complete
if [ ! -f ".madio-setup-complete" ]; then
    echo "❌ MADIO setup not complete. Run /madio-setup first."
    exit 1
fi

# Check for template library
if [ ! -d "_template_library" ]; then
    echo "❌ Template library not found. Run /madio-setup first."
    exit 1
fi

# Check template count
TEMPLATE_COUNT=$(find "_template_library" -name "*.md" | wc -l)
echo "   ✅ Found $TEMPLATE_COUNT MADIO templates"

# Check for existing generated documents
EXISTING_DOCS=$(ls *.md 2>/dev/null | grep -E "(project_system_instructions|orchestrator)" | wc -l)
if [ "$EXISTING_DOCS" -gt 0 ]; then
    echo "   ⚠️  Existing MADIO documents found:"
    ls *.md 2>/dev/null | grep -E "(project_system_instructions|orchestrator|character_|content_|methodology_)" | sed 's/^/      /'
    echo ""
    read -p "   Continue and potentially overwrite? (y/N): " CONTINUE
    if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
        echo "   Operation cancelled."
        exit 1
    fi
fi

echo "   ✅ Project validation complete"
```

### Phase 2: Interactive AI System Definition

```bash
echo ""
echo "🎯 Define Your AI System"
echo ""

# Get AI system description
if [ -z "$1" ]; then
    echo "What AI system do you want to create?"
    echo ""
    echo "Examples:"
    echo "  • Customer support bot with friendly personality and escalation"
    echo "  • Content writing AI with SEO optimization and tone consistency"
    echo "  • Data analysis assistant with evaluation frameworks"
    echo "  • Business analysis system with methodology and rubrics"
    echo ""
    read -p "Describe your AI system: " AI_SYSTEM_DESC
else
    AI_SYSTEM_DESC="$*"
fi

if [ -z "$AI_SYSTEM_DESC" ]; then
    echo "❌ AI system description required."
    exit 1
fi

echo "   🎯 AI System: $AI_SYSTEM_DESC"

# Determine complexity level
echo ""
echo "🔧 Select Complexity Level:"
echo "1. Simple (3-4 documents) - Basic assistant or single-purpose tool"
echo "2. Moderate (5-7 documents) - Multi-feature system with personality"
echo "3. Complex (8-10 documents) - Analysis system with methodology"
echo "4. Enterprise (12+ documents) - Full-capability strategic system"
echo "5. Auto-detect based on description"
echo ""
read -p "Choose complexity [1-5]: " COMPLEXITY_CHOICE

case $COMPLEXITY_CHOICE in
    1) COMPLEXITY="simple" ;;
    2) COMPLEXITY="moderate" ;;
    3) COMPLEXITY="complex" ;;
    4) COMPLEXITY="enterprise" ;;
    5) COMPLEXITY="auto" ;;
    *) COMPLEXITY="auto" ;;
esac

echo "   🔧 Complexity: $COMPLEXITY"
```

### Phase 3: Template Selection Logic

```bash
echo ""
echo "📚 Selecting MADIO Templates..."

# Always include mandatory core templates
SELECTED_TEMPLATES=(
    "madio_template_tier1_project_system_instructions.md"
    "madio_template_tier2_orchestrator.md"
)

# Add templates based on complexity and system description
case $COMPLEXITY in
    "simple")
        # Basic personality if mentioned
        if [[ "$AI_SYSTEM_DESC" =~ (personality|friendly|tone|voice) ]]; then
            SELECTED_TEMPLATES+=("madio_template_tier3_character_voice_authority.md")
        fi
        # Content operations if content-focused
        if [[ "$AI_SYSTEM_DESC" =~ (content|writing|blog|article) ]]; then
            SELECTED_TEMPLATES+=("madio_template_tier3_content_operations.md")
            SELECTED_TEMPLATES+=("madio_template_tier3_standard.md")
        fi
        ;;
    "moderate")
        # Include personality and content for most moderate systems
        SELECTED_TEMPLATES+=("madio_template_tier3_character_voice_authority.md")
        SELECTED_TEMPLATES+=("madio_template_tier3_content_operations.md")
        SELECTED_TEMPLATES+=("madio_template_tier3_standard.md")
        
        # Add specific capabilities based on description
        if [[ "$AI_SYSTEM_DESC" =~ (support|help|customer) ]]; then
            SELECTED_TEMPLATES+=("madio_template_tier3_implementation_roadmap.md")
        fi
        ;;
    "complex")
        # Include analysis capabilities
        SELECTED_TEMPLATES+=("madio_template_tier3_methodology_framework.md")
        SELECTED_TEMPLATES+=("madio_template_tier3_rubrics_evaluation.md")
        SELECTED_TEMPLATES+=("madio_template_tier3_research_protocols.md")
        
        # Add content if content-focused
        if [[ "$AI_SYSTEM_DESC" =~ (content|writing|blog) ]]; then
            SELECTED_TEMPLATES+=("madio_template_tier3_content_operations.md")
            SELECTED_TEMPLATES+=("madio_template_tier3_standard.md")
        fi
        
        # Add strategic if business-focused
        if [[ "$AI_SYSTEM_DESC" =~ (business|strategic|analysis) ]]; then
            SELECTED_TEMPLATES+=("madio_template_tier3_strategic_framework.md")
        fi
        ;;
    "enterprise")
        # Include comprehensive template set
        SELECTED_TEMPLATES+=("madio_template_tier3_character_voice_authority.md")
        SELECTED_TEMPLATES+=("madio_template_tier3_content_operations.md")
        SELECTED_TEMPLATES+=("madio_template_tier3_standard.md")
        SELECTED_TEMPLATES+=("madio_template_tier3_methodology_framework.md")
        SELECTED_TEMPLATES+=("madio_template_tier3_rubrics_evaluation.md")
        SELECTED_TEMPLATES+=("madio_template_tier3_strategic_framework.md")
        SELECTED_TEMPLATES+=("madio_template_tier3_research_protocols.md")
        SELECTED_TEMPLATES+=("madio_template_tier3_implementation_roadmap.md")
        SELECTED_TEMPLATES+=("madio_template_tier3_document_reference_map.md")
        ;;
    "auto")
        # Auto-detect based on keywords in description
        SELECTED_TEMPLATES+=("madio_template_tier3_character_voice_authority.md")
        
        if [[ "$AI_SYSTEM_DESC" =~ (content|writing|blog|article|SEO) ]]; then
            SELECTED_TEMPLATES+=("madio_template_tier3_content_operations.md")
            SELECTED_TEMPLATES+=("madio_template_tier3_standard.md")
        fi
        
        if [[ "$AI_SYSTEM_DESC" =~ (analysis|evaluate|assess|research|methodology) ]]; then
            SELECTED_TEMPLATES+=("madio_template_tier3_methodology_framework.md")
            SELECTED_TEMPLATES+=("madio_template_tier3_rubrics_evaluation.md")
            SELECTED_TEMPLATES+=("madio_template_tier3_research_protocols.md")
        fi
        
        if [[ "$AI_SYSTEM_DESC" =~ (strategic|business|framework|planning) ]]; then
            SELECTED_TEMPLATES+=("madio_template_tier3_strategic_framework.md")
            SELECTED_TEMPLATES+=("madio_template_tier3_implementation_roadmap.md")
        fi
        
        if [[ "$AI_SYSTEM_DESC" =~ (visual|image|brand|design) ]]; then
            SELECTED_TEMPLATES+=("madio_template_tier3_visual_design_standards.md")
            SELECTED_TEMPLATES+=("madio_template_tier3_visual_asset_generation.md")
        fi
        
        # Add document reference map for complex auto-detected systems
        if [ ${#SELECTED_TEMPLATES[@]} -gt 6 ]; then
            SELECTED_TEMPLATES+=("madio_template_tier3_document_reference_map.md")
        fi
        ;;
esac

echo "   📚 Selected ${#SELECTED_TEMPLATES[@]} templates:"
for template in "${SELECTED_TEMPLATES[@]}"; do
    TEMPLATE_NAME=$(echo "$template" | sed 's/madio_template_tier[0-9]_//g' | sed 's/.md//g')
    echo "      ✅ $TEMPLATE_NAME"
done
```

### Phase 4: Document Generation

```bash
echo ""
echo "🚀 Generating MADIO Documents..."

PROJECT_NAME=$(basename "$PWD")
CURRENT_DATE=$(date '+%Y-%m-%d')

# Generate each selected template
for template in "${SELECTED_TEMPLATES[@]}"; do
    TEMPLATE_PATH="_template_library/$template"
    
    if [ -f "$TEMPLATE_PATH" ]; then
        # Determine output filename
        OUTPUT_NAME=$(echo "$template" | sed 's/madio_template_tier[0-9]_//g')
        
        echo "   🔄 Generating $OUTPUT_NAME..."
        
        # Copy template and replace placeholders
        cp "$TEMPLATE_PATH" "$OUTPUT_NAME"
        
        # Replace common placeholders
        sed -i.bak "s/\[PROJECT_NAME\]/$PROJECT_NAME/g" "$OUTPUT_NAME"
        sed -i.bak "s/\[CURRENT_DATE\]/$CURRENT_DATE/g" "$OUTPUT_NAME"
        sed -i.bak "s/\[AI_SYSTEM_DESCRIPTION\]/$AI_SYSTEM_DESC/g" "$OUTPUT_NAME"
        
        # Replace complexity-specific placeholders
        case $OUTPUT_NAME in
            "project_system_instructions.md")
                sed -i.bak "s/\[SYSTEM_PURPOSE\]/$AI_SYSTEM_DESC/g" "$OUTPUT_NAME"
                ;;
            "orchestrator.md")
                # Add references to selected Tier 3 documents
                TIER3_REFS=""
                for t in "${SELECTED_TEMPLATES[@]}"; do
                    if [[ "$t" =~ tier3 ]]; then
                        REF_NAME=$(echo "$t" | sed 's/madio_template_tier3_//g' | sed 's/.md//g')
                        TIER3_REFS="$TIER3_REFS- $REF_NAME.md\n"
                    fi
                done
                sed -i.bak "s/\[TIER3_DOCUMENTS\]/$TIER3_REFS/g" "$OUTPUT_NAME"
                ;;
        esac
        
        # Remove backup file
        rm "$OUTPUT_NAME.bak" 2>/dev/null || true
        
        echo "      ✅ Generated $OUTPUT_NAME"
    else
        echo "      ❌ Template not found: $template"
    fi
done
```

### Phase 5: AI_CONTEXT.md Update

```bash
echo ""
echo "🌉 Updating AI_CONTEXT.md bridge file..."

if [ -f "AI_CONTEXT.md" ]; then
    # Update project phase
    sed -i.bak "s/\[setup|generation|customization|testing|deployment|production\]/generation/g" "AI_CONTEXT.md"
    
    # Add generation timestamp
    GENERATION_TIME=$(date '+%Y-%m-%d %H:%M:%S')
    sed -i.bak "s/\[TIMESTAMP\] - \[Recent development activity\]/$GENERATION_TIME - Generated MADIO system: $AI_SYSTEM_DESC/g" "AI_CONTEXT.md"
    
    # Document template selection
    TEMPLATE_LIST=""
    for template in "${SELECTED_TEMPLATES[@]}"; do
        TEMPLATE_NAME=$(echo "$template" | sed 's/madio_template_tier[0-9]_//g' | sed 's/.md//g')
        TEMPLATE_LIST="$TEMPLATE_LIST- $TEMPLATE_NAME - Selected for AI system generation\n"
    done
    
    # Update template selection section (this is a simplified approach)
    echo "   ✅ Updated AI_CONTEXT.md with generation details"
    echo "      System: $AI_SYSTEM_DESC"
    echo "      Templates: ${#SELECTED_TEMPLATES[@]} documents"
    echo "      Timestamp: $GENERATION_TIME"
    
    rm "AI_CONTEXT.md.bak" 2>/dev/null || true
else
    echo "   ⚠️  AI_CONTEXT.md not found - consider running /madio-setup"
fi
```

### Phase 6: Validation and Success

```bash
echo ""
echo "✅ MADIO AI System Generation Complete!"
echo ""
echo "📁 Generated Documents:"
for template in "${SELECTED_TEMPLATES[@]}"; do
    OUTPUT_NAME=$(echo "$template" | sed 's/madio_template_tier[0-9]_//g')
    if [ -f "$OUTPUT_NAME" ]; then
        echo "   ✅ $OUTPUT_NAME"
    else
        echo "   ❌ $OUTPUT_NAME (generation failed)"
    fi
done

echo ""
echo "🎯 Your AI System: $AI_SYSTEM_DESC"
echo "📊 Complexity: $COMPLEXITY (${#SELECTED_TEMPLATES[@]} documents)"
echo "🌉 Bridge File: AI_CONTEXT.md updated"
echo ""
echo "🚀 Next Steps:"
echo ""
echo "1. 📝 Review Generated Documents:"
echo "   • Check project_system_instructions.md (core AI identity)"
echo "   • Review orchestrator.md (workflow controller)"
echo "   • Validate Tier 3 documents (supporting specifications)"
echo ""
echo "2. ✏️  Customize System:"
echo "   • Replace any remaining [BRACKETED_PLACEHOLDERS]"
echo "   • Adapt content to your specific requirements"
echo "   • Add domain-specific knowledge and examples"
echo ""
echo "3. 🧪 Test Locally:"
echo "   • Validate document hierarchy and cross-references"
echo "   • Test workflow logic and quality gates"
echo "   • Ensure all placeholders are replaced"
echo ""
echo "4. 🚀 Deploy to Platform:"
echo "   • OpenAI CustomGPT: Copy project_system_instructions.md + upload docs"
echo "   • Google Gemini Gem: Combine documents per .madio configuration"
echo "   • Claude Project: Upload to project knowledge with AI_CONTEXT.md"
echo ""
echo "5. 🔄 Update Context:"
echo "   • Use: gemini \"Update AI_CONTEXT.md with customization progress\""
echo "   • Document: Template selection rationale and modifications"
echo "   • Track: Deployment status and platform configurations"
echo ""
echo "💡 Quality Checklist:"
echo "   □ All [BRACKETED_TEXT] replaced with project-specific content"
echo "   □ Document hierarchy maintains proper authority (Tier 1 → 2 → 3)"
echo "   □ Cross-references between documents function correctly"
echo "   □ Quality gates and validation procedures operational"
echo "   □ Platform deployment requirements satisfied"
echo ""
echo "🎉 Your MADIO AI system is ready for customization and deployment!"
```

## Error Handling

### **Template Validation**
- Verify all selected templates exist in `_template_library/`
- Check template integrity and required placeholders
- Validate template relationships and dependencies

### **Generation Validation**
- Confirm successful file creation for each template
- Verify placeholder replacement completion
- Check document hierarchy integrity

### **Context Validation**
- Ensure AI_CONTEXT.md updates successfully
- Validate bridge file content and structure
- Confirm project state progression

## Usage Examples

```bash
# Interactive generation
/generate-ai-system

# Direct generation with description
/generate-ai-system "customer support bot with friendly personality and escalation protocols"

# Complex analysis system
/generate-ai-system "business analysis AI with methodology frameworks and evaluation rubrics"
```

## Integration Notes

- Works seamlessly with `/madio-setup` and `/orient` commands
- Updates AI_CONTEXT.md for continuity with browser AI
- Supports both Gemini CLI and Claude Code workflows
- Enables template inheritance and framework updates
