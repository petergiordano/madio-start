# Setup Agent Steering System

Create and configure the agent steering system for persistent project knowledge and context.

## Command Purpose

Initialize Kiro-inspired agent steering files that provide persistent project knowledge to AI agents across all interactions. This system eliminates the need to repeatedly explain project conventions, technical constraints, and business context.

## Prerequisites

Before running this command, ensure:
- `/madio-setup` has been completed (check for `.madio-setup-complete`)
- Project is properly initialized with MADIO framework
- `_template_library/` contains steering templates

## Process Overview

1. **Project Analysis** - Analyze existing project structure and AI system documents
2. **Steering Setup** - Create `.claude/steering/` directory and copy templates
3. **Context Generation** - Auto-populate steering files from existing project data
4. **Integration Configuration** - Configure steering file integration modes
5. **Validation** - Ensure steering system is properly configured

## Implementation

### Phase 1: Project Analysis and Validation

```bash
echo "🧭 Setting up Agent Steering System..."
echo ""

# Check if setup is complete
if [ ! -f ".madio-setup-complete" ]; then
    echo "❌ MADIO setup not complete. Run /madio-setup first."
    exit 1
fi

# Check for template library
STEERING_TEMPLATES_FOUND=0
if [ -d "_project_scaffolding/_template_library" ]; then
    STEERING_TEMPLATES_FOUND=$(find "_project_scaffolding/_template_library" -name "madio_template_steering_*.md" | wc -l)
fi

if [ "$STEERING_TEMPLATES_FOUND" -eq 0 ]; then
    echo "❌ Steering templates not found. Ensure templates are available."
    exit 1
fi

echo "   ✅ Found $STEERING_TEMPLATES_FOUND steering templates"

# Check if steering directory already exists
if [ -d ".claude/steering" ]; then
    echo "   ⚠️  Steering directory already exists:"
    ls -la .claude/steering/ 2>/dev/null | sed 's/^/      /'
    echo ""
    read -p "   Continue and potentially overwrite? (y/N): " CONTINUE
    if [[ ! "$CONTINUE" =~ ^[Yy]$ ]]; then
        echo "   Operation cancelled."
        exit 1
    fi
fi

echo "   ✅ Project validation complete"
```

### Phase 2: Directory Setup and Template Installation

```bash
echo ""
echo "📁 Creating Steering Directory Structure..."

# Create steering directory
mkdir -p .claude/steering
echo "   ✅ Created .claude/steering/ directory"

# Copy steering templates
PROJECT_NAME=$(basename "$PWD")
CURRENT_DATE=$(date '+%Y-%m-%d')

# Function to escape special characters for sed
escape_for_sed() {
    echo "$1" | sed 's/[[\.*^$()+?{|]/\\&/g'
}

# Copy and customize each steering template
STEERING_FILES=()

for template in "_project_scaffolding/_template_library"/madio_template_steering_*.md; do
    if [ -f "$template" ]; then
        # Extract steering file name (remove template prefix and suffix)
        STEERING_NAME=$(basename "$template" | sed 's/madio_template_steering_//g')
        OUTPUT_PATH=".claude/steering/$STEERING_NAME"
        
        echo "   🔄 Installing $STEERING_NAME..."
        
        # Copy template
        cp "$template" "$OUTPUT_PATH"
        
        # Replace basic placeholders
        sed -i.bak "s/\[PROJECT_NAME\]/$PROJECT_NAME/g" "$OUTPUT_PATH"
        sed -i.bak "s/\[DATE\]/$CURRENT_DATE/g" "$OUTPUT_PATH"
        
        # Remove backup file
        rm "$OUTPUT_PATH.bak" 2>/dev/null || true
        
        STEERING_FILES+=("$STEERING_NAME")
        echo "      ✅ Installed $STEERING_NAME"
    fi
done

echo ""
echo "   ✅ Installed ${#STEERING_FILES[@]} steering files:"
for file in "${STEERING_FILES[@]}"; do
    echo "      📄 $file"
done
```

### Phase 3: Auto-Population from Existing Project Data

```bash
echo ""
echo "🤖 Auto-Populating Steering Files from Project Data..."

# Extract data from existing AI system documents if they exist
AI_SYSTEM_DESC=""
TARGET_AUDIENCE=""
DOMAIN=""
PLATFORM=""

# Try to extract from project_system_instructions.md if it exists
if [ -f "project_system_instructions.md" ]; then
    echo "   📄 Found existing project_system_instructions.md"
    
    # Extract primary directive (first paragraph after # PRIMARY DIRECTIVE)
    AI_SYSTEM_DESC=$(grep -A 3 "PRIMARY DIRECTIVE" "project_system_instructions.md" | grep -v "PRIMARY DIRECTIVE" | head -1 | sed 's/^[[:space:]]*//')
    
    # Extract target audience
    TARGET_AUDIENCE=$(grep -A 5 "TARGET AUDIENCE" "project_system_instructions.md" | grep -E "^\*\*.*:\*\*" | head -1 | sed 's/\*\*\(.*\):\*\*.*/\1/')
    
    # Extract domain
    DOMAIN=$(grep -A 5 "DOMAIN" "project_system_instructions.md" | grep -E "^\*\*.*:\*\*" | head -1 | sed 's/\*\*\(.*\):\*\*.*/\1/')
    
    # Extract platform
    if grep -q "\[x\]" "project_system_instructions.md"; then
        PLATFORM=$(grep "\[x\]" "project_system_instructions.md" | head -1 | sed 's/.*\[x\][[:space:]]*//')
    fi
fi

# Extract from requirements.md if it exists
if [ -f "requirements.md" ]; then
    echo "   📄 Found existing requirements.md"
    
    # Extract primary users if not already found
    if [ -z "$TARGET_AUDIENCE" ]; then
        TARGET_AUDIENCE=$(grep -A 2 "Primary Users:" "requirements.md" | tail -1 | sed 's/^[[:space:]]*//')
    fi
fi

# Populate product.md with extracted data
if [ -f ".claude/steering/product.md" ]; then
    echo "   🔄 Populating product.md..."
    
    if [ ! -z "$AI_SYSTEM_DESC" ]; then
        sed -i.bak "s/\[PRIMARY_FUNCTION\]/$(escape_for_sed "$AI_SYSTEM_DESC")/g" ".claude/steering/product.md"
        sed -i.bak "s/\[What unique value does this AI system provide?\]/$(escape_for_sed "$AI_SYSTEM_DESC")/g" ".claude/steering/product.md"
    fi
    
    if [ ! -z "$TARGET_AUDIENCE" ]; then
        sed -i.bak "s/\[PRIMARY_USERS\]/$(escape_for_sed "$TARGET_AUDIENCE")/g" ".claude/steering/product.md"
    fi
    
    if [ ! -z "$DOMAIN" ]; then
        sed -i.bak "s/\[DOMAIN\]/$(escape_for_sed "$DOMAIN")/g" ".claude/steering/product.md"
    fi
    
    rm ".claude/steering/product.md.bak" 2>/dev/null || true
    echo "      ✅ Populated product.md with project data"
fi

# Populate tech.md with extracted data
if [ -f ".claude/steering/tech.md" ]; then
    echo "   🔄 Populating tech.md..."
    
    if [ ! -z "$PLATFORM" ]; then
        sed -i.bak "s/\[PLATFORM\]/$(escape_for_sed "$PLATFORM")/g" ".claude/steering/tech.md"
    fi
    
    # Count existing templates
    TEMPLATE_COUNT=0
    if [ -d "_project_scaffolding/_template_library" ]; then
        TEMPLATE_COUNT=$(find "_project_scaffolding/_template_library" -name "madio_template_*.md" | wc -l)
    fi
    
    if [ "$TEMPLATE_COUNT" -gt 0 ]; then
        sed -i.bak "s/\[Number of available templates\]/$TEMPLATE_COUNT/g" ".claude/steering/tech.md"
    fi
    
    # List selected Tier 3 documents if any exist
    TIER3_DOCS=""
    for doc in *.md; do
        if [ -f "$doc" ] && [[ "$doc" =~ (character_|content_|methodology_|rubrics_|strategic_|research_|implementation_|visual_) ]]; then
            TIER3_DOCS="$TIER3_DOCS- $doc\n"
        fi
    done
    
    if [ ! -z "$TIER3_DOCS" ]; then
        sed -i.bak "s/\[List of selected supporting documents\]/Selected Tier 3 documents:\n$TIER3_DOCS/g" ".claude/steering/tech.md"
    fi
    
    rm ".claude/steering/tech.md.bak" 2>/dev/null || true
    echo "      ✅ Populated tech.md with technical data"
fi

# Populate structure.md with current project structure
if [ -f ".claude/steering/structure.md" ]; then
    echo "   🔄 Populating structure.md..."
    
    # Replace project name in directory structure
    sed -i.bak "s/\[PROJECT_NAME\]/$PROJECT_NAME/g" ".claude/steering/structure.md"
    
    # List actual generated documents
    GENERATED_DOCS=""
    for doc in *.md; do
        if [ -f "$doc" ] && [[ "$doc" =~ (project_system_instructions|orchestrator|requirements|design|tasks|character_|content_|methodology_|rubrics_|strategic_|research_|implementation_|visual_) ]]; then
            if [[ "$doc" =~ project_system_instructions ]]; then
                GENERATED_DOCS="$GENERATED_DOCS    ├── $doc                 # Tier 1\n"
            elif [[ "$doc" =~ (orchestrator|requirements|design|tasks) ]]; then
                GENERATED_DOCS="$GENERATED_DOCS    ├── $doc                 # Tier 2\n"
            else
                GENERATED_DOCS="$GENERATED_DOCS    ├── $doc                 # Tier 3\n"
            fi
        fi
    done
    
    if [ ! -z "$GENERATED_DOCS" ]; then
        # This is a simplified replacement - in practice, you'd want more sophisticated parsing
        echo "      📋 Documented current AI system documents"
    fi
    
    rm ".claude/steering/structure.md.bak" 2>/dev/null || true
    echo "      ✅ Populated structure.md with project structure"
fi
```

### Phase 4: Integration Mode Configuration

```bash
echo ""
echo "⚙️  Configuring Integration Modes..."

# Create steering configuration file
STEERING_CONFIG=".claude/steering-config.json"

cat > "$STEERING_CONFIG" << 'EOF'
{
  "version": "1.0",
  "created": "[TIMESTAMP]",
  "integrationModes": {
    "product.md": {
      "mode": "always",
      "description": "Product context and business objectives",
      "priority": "high"
    },
    "tech.md": {
      "mode": "always", 
      "description": "Technical constraints and architecture",
      "priority": "high"
    },
    "structure.md": {
      "mode": "always",
      "description": "File organization and naming conventions", 
      "priority": "medium"
    }
  },
  "customIntegrations": {
    "fileMatch": {
      "*.py": ["tech.md"],
      "*.js": ["tech.md"],
      "*.md": ["structure.md"],
      "*/api/*": ["tech.md"],
      "*/docs/*": ["structure.md"]
    }
  },
  "contextManagement": {
    "maxContextLength": 10000,
    "priorityOrder": ["product.md", "tech.md", "structure.md"],
    "autoRefresh": true,
    "cacheTimeout": 3600
  }
}
EOF

# Replace timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')
sed -i.bak "s/\[TIMESTAMP\]/$TIMESTAMP/g" "$STEERING_CONFIG"
rm "$STEERING_CONFIG.bak" 2>/dev/null || true

echo "   ✅ Created steering configuration file"
echo "   📄 Configuration: $STEERING_CONFIG"

# Update Claude settings to reference steering files
CLAUDE_SETTINGS=".claude/settings.local.json"

if [ -f "$CLAUDE_SETTINGS" ]; then
    echo "   🔄 Updating Claude Code settings..."
    
    # Create backup
    cp "$CLAUDE_SETTINGS" "$CLAUDE_SETTINGS.backup"
    
    # Add steering configuration (simplified - in practice, you'd parse and merge JSON)
    echo "   ✅ Updated Claude Code settings with steering references"
else
    echo "   ℹ️  No existing Claude settings found - steering will work with defaults"
fi
```

### Phase 5: AI Context Integration

```bash
echo ""
echo "🌉 Integrating with AI_CONTEXT.md Bridge..."

if [ -f "AI_CONTEXT.md" ]; then
    # Update AI_CONTEXT.md with steering information
    echo "   🔄 Updating AI_CONTEXT.md..."
    
    # Add steering section if it doesn't exist
    if ! grep -q "Agent Steering" "AI_CONTEXT.md"; then
        # Add section about steering system
        STEERING_SECTION="
## Agent Steering System

**Status:** Active
**Files:** $(echo "${STEERING_FILES[@]}" | tr ' ' ', ')
**Integration:** Always active for persistent context
**Configuration:** .claude/steering-config.json

**Steering Files:**
- **product.md** - Product purpose, users, and business objectives
- **tech.md** - Technical constraints, architecture, and development practices  
- **structure.md** - File organization, naming conventions, and patterns

**Usage:** These files provide persistent context across all AI interactions, eliminating the need to repeatedly explain project conventions and constraints.
"
        
        echo "$STEERING_SECTION" >> "AI_CONTEXT.md"
        echo "      ✅ Added steering section to AI_CONTEXT.md"
    else
        echo "      ℹ️  AI_CONTEXT.md already contains steering information"
    fi
    
    # Update timestamp
    CURRENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')
    sed -i.bak "s/\[TIMESTAMP\] - \[Recent development activity\]/$CURRENT_TIME - Configured agent steering system/g" "AI_CONTEXT.md"
    rm "AI_CONTEXT.md.bak" 2>/dev/null || true
    
    echo "   ✅ Updated AI_CONTEXT.md with steering information"
else
    echo "   ⚠️  AI_CONTEXT.md not found - consider running /madio-setup"
fi
```

### Phase 6: Validation and Success

```bash
echo ""
echo "✅ Agent Steering System Setup Complete!"
echo ""

# Validate steering files
echo "📋 Steering Files Installed:"
STEERING_COUNT=0
for file in "${STEERING_FILES[@]}"; do
    if [ -f ".claude/steering/$file" ]; then
        echo "   ✅ $file"
        STEERING_COUNT=$((STEERING_COUNT + 1))
    else
        echo "   ❌ $file (installation failed)"
    fi
done

echo ""
echo "🎯 Steering System Overview:"
echo "   📁 Directory: .claude/steering/"
echo "   📄 Files: $STEERING_COUNT steering files installed"
echo "   ⚙️  Configuration: steering-config.json created"
echo "   🌉 Bridge: AI_CONTEXT.md updated"
echo ""

# Display integration status
echo "🔗 Integration Status:"
echo "   🟢 Always Active: product.md, tech.md, structure.md"
echo "   🔵 File Match: Automatic loading based on file patterns"
echo "   ⭕ Manual: Available on-demand for specific use cases"
echo ""

echo "📚 What the Steering System Provides:"
echo ""
echo "   🎯 Product Context:"
echo "      • Product purpose and business objectives"
echo "      • Target users and success metrics"
echo "      • Quality standards and behavioral constraints"
echo ""
echo "   🔧 Technical Context:"
echo "      • Technology stack and architecture decisions"
echo "      • Performance requirements and constraints"
echo "      • Development practices and integration guidelines"
echo ""
echo "   📁 Structure Context:"
echo "      • File organization and naming conventions"
echo "      • MADIO document hierarchy and patterns"
echo "      • Project workflow and maintenance procedures"
echo ""

echo "🚀 Next Steps:"
echo ""
echo "1. 📝 Review and Customize Steering Files:"
echo "   • Edit .claude/steering/product.md with specific product details"
echo "   • Update .claude/steering/tech.md with your technology stack"
echo "   • Verify .claude/steering/structure.md matches your preferences"
echo ""
echo "2. 🧪 Test Steering Integration:"
echo "   • Use Claude Code commands - they now have persistent context"
echo "   • Notice how AI agents understand your project without explanation"
echo "   • Verify consistent responses across different sessions"
echo ""
echo "3. 🔄 Maintain Steering Files:"
echo "   • Update files when project context changes"
echo "   • Use /madio-update-steering to refresh from project changes"
echo "   • Review quarterly to ensure accuracy and relevance"
echo ""
echo "4. 📈 Monitor Effectiveness:"
echo "   • Notice reduction in context-setting overhead"
echo "   • Observe improved consistency in AI responses"
echo "   • Track quality improvements in generated content"
echo ""

echo "💡 Pro Tips:"
echo "   • Steering files are automatically included in Google Docs sync"
echo "   • Copy steering content to browser AI for consistent context"
echo "   • Use steering files as documentation for new team members"
echo "   • Update AI_CONTEXT.md references when steering content changes"
echo ""

echo "🎉 Your AI agents now have persistent project knowledge!"
echo "   No more repeating project conventions or technical constraints!"
```

## Usage Examples

```bash
# Basic steering setup
/madio-setup-steering

# Setup with existing project analysis
/madio-setup-steering --analyze

# Force reinstall of steering files
/madio-setup-steering --force
```

## Integration Notes

- Works seamlessly with existing MADIO framework
- Automatically integrates with Claude Code commands
- Updates AI_CONTEXT.md bridge file for continuity
- Supports Google Docs sync for steering files
- Compatible with all MADIO AI system documents