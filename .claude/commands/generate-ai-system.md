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
3. **Document Generation** - Create hierarchical AI system documents
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
    echo "   ⚠️  Existing AI system documents found:"
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

### Phase 4: Interactive Project Details Collection

```bash
echo ""
echo "📋 Let's gather details about your AI system..."
echo ""

# Collect project details based on complexity and description
echo "Project Name: $PROJECT_NAME"
read -p "Target Audience (e.g., customers, internal team, developers): " TARGET_AUDIENCE
read -p "Primary Domain/Industry (e.g., tech support, marketing, healthcare): " DOMAIN
read -p "Deployment Platform (openai/gemini/claude/all): " PLATFORM

# Collect additional details based on system type
if [[ "$AI_SYSTEM_DESC" =~ (personality|friendly|tone|voice) ]]; then
    echo ""
    echo "🎭 Character & Voice Details:"
    read -p "Personality traits (e.g., friendly, professional, witty): " PERSONALITY_TRAITS
    read -p "Communication style (e.g., formal, casual, technical): " COMM_STYLE
    read -p "Example greeting for users: " EXAMPLE_GREETING
fi

if [[ "$AI_SYSTEM_DESC" =~ (content|writing|blog|article) ]]; then
    echo ""
    echo "✍️ Content Creation Details:"
    read -p "Content types to create (e.g., blog posts, emails, reports): " CONTENT_TYPES
    read -p "Tone variations needed (e.g., professional, casual, persuasive): " TONE_VARIATIONS
    read -p "Any specific formatting requirements? " FORMAT_REQUIREMENTS
fi

if [[ "$AI_SYSTEM_DESC" =~ (analysis|evaluate|assess|methodology) ]]; then
    echo ""
    echo "📊 Analysis Framework Details:"
    read -p "Types of analysis performed (e.g., data, business, risk): " ANALYSIS_TYPES
    read -p "Key evaluation criteria (e.g., ROI, efficiency, accuracy): " EVAL_CRITERIA
    read -p "Deliverable formats (e.g., reports, dashboards, summaries): " DELIVERABLES
fi

if [[ "$AI_SYSTEM_DESC" =~ (support|help|customer) ]]; then
    echo ""
    echo "🤝 Support System Details:"
    read -p "Common issue categories (e.g., technical, billing, account): " ISSUE_CATEGORIES
    read -p "Escalation triggers (e.g., angry customer, complex issue): " ESCALATION_TRIGGERS
    read -p "Available resources/knowledge base: " KNOWLEDGE_BASE
fi

# Quality standards
echo ""
echo "📏 Quality Standards:"
read -p "Critical quality requirements (e.g., accuracy, empathy, speed): " QUALITY_REQUIREMENTS
read -p "Unacceptable behaviors (e.g., giving medical advice, making promises): " FORBIDDEN_ACTIONS

echo ""
echo "   ✅ Project details collected"
```

### Phase 5: AI System Document Generation with Deep Customization

```bash
echo ""
echo "🚀 Generating Customized MADIO Documents..."

PROJECT_NAME=$(basename "$PWD")
CURRENT_DATE=$(date '+%Y-%m-%d')

# Function to escape special characters for sed
escape_for_sed() {
    echo "$1" | sed 's/[[\.*^$()+?{|]/\\&/g'
}

# Generate each selected template with customization
for template in "${SELECTED_TEMPLATES[@]}"; do
    TEMPLATE_PATH="_template_library/$template"
    
    if [ -f "$TEMPLATE_PATH" ]; then
        # Determine output filename
        OUTPUT_NAME=$(echo "$template" | sed 's/madio_template_tier[0-9]_//g')
        
        echo "   🔄 Generating $OUTPUT_NAME..."
        
        # Copy template
        cp "$TEMPLATE_PATH" "$OUTPUT_NAME"
        
        # Replace common placeholders
        sed -i.bak "s/\[PROJECT_NAME\]/$(escape_for_sed "$PROJECT_NAME")/g" "$OUTPUT_NAME"
        sed -i.bak "s/\[DATE\]/$(escape_for_sed "$CURRENT_DATE")/g" "$OUTPUT_NAME"
        sed -i.bak "s/\[CURRENT_DATE\]/$(escape_for_sed "$CURRENT_DATE")/g" "$OUTPUT_NAME"
        sed -i.bak "s/\[TARGET_AUDIENCE\]/$(escape_for_sed "$TARGET_AUDIENCE")/g" "$OUTPUT_NAME"
        sed -i.bak "s/\[DOMAIN\]/$(escape_for_sed "$DOMAIN")/g" "$OUTPUT_NAME"
        
        # Document-specific customization
        case $OUTPUT_NAME in
            "project_system_instructions.md")
                # Customize primary directive
                PRIMARY_DIRECTIVE="You are $PROJECT_NAME, an AI system designed to $AI_SYSTEM_DESC. Your primary mission is to serve $TARGET_AUDIENCE in the $DOMAIN domain with exceptional quality and reliability."
                sed -i.bak "s/\[Define the fundamental purpose and mission of this AI system in 2-3 clear sentences\]/$(escape_for_sed "$PRIMARY_DIRECTIVE")/g" "$OUTPUT_NAME"
                
                # Customize scope
                SCOPE="This system provides: $AI_SYSTEM_DESC. It does not: $FORBIDDEN_ACTIONS"
                sed -i.bak "s/\[Clearly define what this system does and does not do\]/$(escape_for_sed "$SCOPE")/g" "$OUTPUT_NAME"
                
                # Set platform
                case $PLATFORM in
                    "openai") sed -i.bak "s/\[ \] OpenAI CustomGPT/\[x\] OpenAI CustomGPT/g" "$OUTPUT_NAME" ;;
                    "gemini") sed -i.bak "s/\[ \] Google Gemini Gem/\[x\] Google Gemini Gem/g" "$OUTPUT_NAME" ;;
                    "claude") sed -i.bak "s/\[ \] Claude Project/\[x\] Claude Project/g" "$OUTPUT_NAME" ;;
                    "all") sed -i.bak "s/\[ \] Multi-platform deployment/\[x\] Multi-platform deployment/g" "$OUTPUT_NAME" ;;
                esac
                
                # Add quality requirements
                sed -i.bak "s/\[List requirements that, if violated, trigger immediate regeneration\]/$(escape_for_sed "$QUALITY_REQUIREMENTS")/g" "$OUTPUT_NAME"
                
                # Update subordinate documents list
                SUBORDINATE_DOCS="- orchestrator.md (Tier 2) - Main workflow controller"
                for t in "${SELECTED_TEMPLATES[@]}"; do
                    if [[ "$t" =~ tier3 ]]; then
                        DOC_NAME=$(echo "$t" | sed 's/madio_template_tier3_//g' | sed 's/.md//g')
                        SUBORDINATE_DOCS="$SUBORDINATE_DOCS\n- ${DOC_NAME}.md (Tier 3) - Supporting document"
                    fi
                done
                sed -i.bak "s/\[List all other Tier 2 and Tier 3 documents\]/$(escape_for_sed "$SUBORDINATE_DOCS")/g" "$OUTPUT_NAME"
                ;;
                
            "orchestrator.md")
                # Add workflow introduction based on system type
                WORKFLOW_INTRO="This orchestrator controls the workflow for $AI_SYSTEM_DESC, ensuring consistent quality for $TARGET_AUDIENCE."
                sed -i.bak "s/\[Brief description of what this orchestrator controls\]/$(escape_for_sed "$WORKFLOW_INTRO")/g" "$OUTPUT_NAME"
                
                # Reference tier 3 documents
                TIER3_REFS=""
                for t in "${SELECTED_TEMPLATES[@]}"; do
                    if [[ "$t" =~ tier3 ]]; then
                        REF_NAME=$(echo "$t" | sed 's/madio_template_tier3_//g' | sed 's/.md//g')
                        TIER3_REFS="$TIER3_REFS- ${REF_NAME}.md\n"
                    fi
                done
                sed -i.bak "s/\[List all Tier 3 documents this orchestrator will reference\]/$(escape_for_sed "$TIER3_REFS")/g" "$OUTPUT_NAME"
                ;;
                
            "character_voice_authority.md")
                if [ ! -z "$PERSONALITY_TRAITS" ]; then
                    sed -i.bak "s/\[Define the personality traits\]/$(escape_for_sed "$PERSONALITY_TRAITS")/g" "$OUTPUT_NAME"
                fi
                if [ ! -z "$COMM_STYLE" ]; then
                    sed -i.bak "s/\[Describe communication style\]/$(escape_for_sed "$COMM_STYLE")/g" "$OUTPUT_NAME"
                fi
                if [ ! -z "$EXAMPLE_GREETING" ]; then
                    sed -i.bak "s/\[Example greeting or introduction\]/$(escape_for_sed "$EXAMPLE_GREETING")/g" "$OUTPUT_NAME"
                fi
                ;;
                
            "content_operations.md")
                if [ ! -z "$CONTENT_TYPES" ]; then
                    sed -i.bak "s/\[List content types\]/$(escape_for_sed "$CONTENT_TYPES")/g" "$OUTPUT_NAME"
                fi
                if [ ! -z "$TONE_VARIATIONS" ]; then
                    sed -i.bak "s/\[Define tone variations\]/$(escape_for_sed "$TONE_VARIATIONS")/g" "$OUTPUT_NAME"
                fi
                ;;
                
            "methodology_framework.md")
                if [ ! -z "$ANALYSIS_TYPES" ]; then
                    sed -i.bak "s/\[Types of analysis\]/$(escape_for_sed "$ANALYSIS_TYPES")/g" "$OUTPUT_NAME"
                fi
                if [ ! -z "$EVAL_CRITERIA" ]; then
                    sed -i.bak "s/\[Evaluation criteria\]/$(escape_for_sed "$EVAL_CRITERIA")/g" "$OUTPUT_NAME"
                fi
                ;;
        esac
        
        # Final cleanup - replace any remaining generic placeholders
        sed -i.bak "s/\[SYSTEM_CONTEXT\]/$(escape_for_sed "$AI_SYSTEM_DESC")/g" "$OUTPUT_NAME"
        sed -i.bak "s/\[PRIMARY_FUNCTION\]/$(escape_for_sed "$AI_SYSTEM_DESC")/g" "$OUTPUT_NAME"
        sed -i.bak "s/\[QUALITY_STANDARDS\]/$(escape_for_sed "$QUALITY_REQUIREMENTS")/g" "$OUTPUT_NAME"
        
        # Remove backup file
        rm "$OUTPUT_NAME.bak" 2>/dev/null || true
        
        echo "      ✅ Generated and customized $OUTPUT_NAME"
    else
        echo "      ❌ Template not found: $template"
    fi
done

# Scan for remaining placeholders
echo ""
echo "   🔍 Scanning for remaining placeholders..."
REMAINING_PLACEHOLDERS=$(grep -h "\[.*\]" *.md 2>/dev/null | grep -v "^\[x\]" | sort | uniq | head -10)
if [ ! -z "$REMAINING_PLACEHOLDERS" ]; then
    echo "   ⚠️  Some placeholders need manual replacement:"
    echo "$REMAINING_PLACEHOLDERS" | sed 's/^/      /'
else
    echo "   ✅ All major placeholders replaced!"
fi
```

### Phase 6: Template Library Cleanup

```bash
echo ""
echo "🧹 Cleaning up template library..."

# Remove template library after successful generation
if [ -d "_template_library" ]; then
    echo "   ℹ️  The template library served its purpose!"
    echo "   ℹ️  Removing _template_library/ to keep your project clean"
    rm -rf "_template_library"
    echo "   ✅ Template library removed"
else
    echo "   ℹ️  Template library already removed"
fi

# Note: Templates are preserved in the original madio-start repository
# Users can get updates via: git pull template main
```

### Phase 7: AI_CONTEXT.md Update

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

### Phase 8: Validation and Success

```bash
echo ""
echo "✅ MADIO AI System Generation Complete!"
echo ""
echo "📁 Generated Documents:"
GENERATED_FILES=()
for template in "${SELECTED_TEMPLATES[@]}"; do
    OUTPUT_NAME=$(echo "$template" | sed 's/madio_template_tier[0-9]_//g')
    if [ -f "$OUTPUT_NAME" ]; then
        echo "   ✅ $OUTPUT_NAME"
        GENERATED_FILES+=("$OUTPUT_NAME")
    else
        echo "   ❌ $OUTPUT_NAME (generation failed)"
    fi
done

echo ""
echo "🎯 Your AI System: $AI_SYSTEM_DESC"
echo "📊 Complexity: $COMPLEXITY (${#SELECTED_TEMPLATES[@]} documents)"
echo "🌉 Bridge File: AI_CONTEXT.md updated"
echo ""

# Optional: Offer to set up flexible sync
echo "🔗 Google Docs Sync Setup:"
echo ""
echo "Would you like to set up flexible Google Docs sync for your generated files?"
echo "This will:"
echo "• Create a synced_docs/ directory"
echo "• Move your generated AI system documents there"
echo "• Enable automatic Google Docs creation and sync"
echo ""
read -p "Set up flexible sync? (y/N): " SETUP_SYNC

if [[ "$SETUP_SYNC" =~ ^[Yy]$ ]]; then
    echo ""
    echo "📁 Setting up synced_docs/ directory..."
    
    # Create synced_docs directory
    mkdir -p synced_docs
    echo "   ✅ Created synced_docs/ directory"
    
    # Move generated files to synced_docs
    MOVED_COUNT=0
    for file in "${GENERATED_FILES[@]}"; do
        if [ -f "$file" ]; then
            mv "$file" "synced_docs/"
            echo "   📁 Moved $file → synced_docs/"
            ((MOVED_COUNT++))
        fi
    done
    
    echo ""
    echo "✅ Moved $MOVED_COUNT files to synced_docs/ for easy sync!"
    echo ""
    
    # Check if Google credentials are set up
    if [ -f ".claude/scripts/credentials.json" ]; then
        echo "🚀 Google credentials found - ready to sync!"
        echo ""
        echo "🎯 Quick Start (3 simple steps):"
        echo "   1. ✅ Files already moved to synced_docs/ (done!)"
        echo "   2. Run sync command:"
        echo "      /push-to-docs"
        echo "   3. That's it! Google Docs will be created automatically"
        echo ""
        echo "📋 After first sync:"
        echo "   • Edit files locally in synced_docs/"
        echo "   • Run the same sync command to update Google Docs"
        echo "   • All document IDs are saved automatically"
    else
        echo "⚠️  Google credentials needed before first sync:"
        echo ""
        echo "🎯 Quick Setup (one-time only):"
        echo "   1. Enable Google Docs sync: /madio-enable-sync"
        echo "   2. Follow the Google Cloud setup prompts"
        echo "   3. Then sync: /push-to-docs"
        echo ""
        echo "💡 Your files are already organized in synced_docs/ and ready!"
    fi
    
    echo ""
    echo "📊 What's in synced_docs/:"
    ls -la synced_docs/*.md 2>/dev/null | wc -l | xargs echo "   •" && echo " AI system documents ready to sync"
    echo ""
    echo "💡 Benefits of flexible sync:"
    echo "   • Zero configuration - just add AI system documents to synced_docs/"
    echo "   • Automatic Google Doc creation for new files"
    echo "   • Persistent file→doc ID mapping in .synced_docs_mapping.json"
    echo "   • Works with any directory structure"
    echo ""
else
    echo ""
    echo "📋 Files remain in project root. To sync later:"
    echo "   • Option 1: Move to synced_docs/ → /push-to-docs"
    echo "   • Option 2: Configure .claude/scripts/sync_config.json → /push-to-docs"
fi
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
echo "3. 🔗 Set Up Google Docs Sync (if not done already):"
echo "   • Run: ./.claude/scripts/setup.sh (installs dependencies, sets up credentials)"
echo "   • Follow Google Cloud setup prompts"
echo "   • Then sync: /push-to-docs"
echo "   • See GETTING-STARTED.md Step 4 for detailed instructions"
echo ""
echo "4. 🧪 Test Locally:"
echo "   • Validate document hierarchy and cross-references"
echo "   • Test workflow logic and quality gates"
echo "   • Ensure all placeholders are replaced"
echo ""
echo "5. 🚀 Deploy to Platform:"
echo "   • OpenAI CustomGPT: Copy project_system_instructions.md + upload docs"
echo "   • Google Gemini Gem: Combine documents per .madio configuration"
echo "   • Claude Project: Upload to project knowledge with AI_CONTEXT.md"
echo ""
echo "6. 🔄 Update Context:"
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
echo "   □ Google Docs sync configured and tested (recommended for Claude Projects)"
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
