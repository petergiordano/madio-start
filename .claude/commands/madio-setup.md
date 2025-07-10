# MADIO Setup

One-time MADIO project initialization after creating project from madio-start template.

## Command Purpose

Run **once only** after creating and cloning a project from the madio-start template to transform scaffolding into a clean MADIO project workspace. Sets up templates, generates bridge files, and configures git for template updates.

**🔄 Note**: This command is automatically called by `/madio-onboard` but can be run independently for advanced users.

## Usage

```bash
# Interactive setup (prompts for confirmation when needed)
/madio-setup

# Unattended setup (skips all prompts, assumes "yes" to all questions)
/madio-setup --yes
```

**Flags:**
- `--yes` or `-y`: Run in unattended mode, automatically accepting all prompts

## Execution Process

### Phase 1: Safety Validation

First, check if this MADIO project has already been set up:

```bash
# Parse command line arguments
YES_FLAG=false
for arg in "$@"; do
    case $arg in
        --yes|-y)
            YES_FLAG=true
            shift
            ;;
    esac
done

# Check for setup completion marker
if [ -f ".madio-setup-complete" ]; then
    echo "❌ MADIO project already set up."
    echo ""
    echo "🔍 Current project state:"
    ls -la | grep -E "(AI_CONTEXT\.md|GEMINI\.md|project_system_instructions\.md)"
    echo ""
    echo "💡 Next steps:"
    echo "   • Generate AI system: Use /generate-ai-system command"
    echo "   • Update context: Read AI_CONTEXT.md for current project status"
    echo "   • Get template updates: git pull template main"
    echo "   • View templates: ls _template_library/"
    echo "   • Run health check: /madio-doctor"
    exit 1
fi

# Check for scaffolding directory (indicates fresh template)
if [ ! -d "_project_scaffolding/" ]; then
    echo "❌ No scaffolding directory found."
    echo "This may not be a fresh madio-start template or setup was already partially completed."
    echo ""
    echo "🔍 Expected structure:"
    echo "   _project_scaffolding/_template_library/"
    echo "   _project_scaffolding/GEMINI.md"
    echo "   _project_scaffolding/madio_core_templates.md"
    exit 1
fi

echo "✅ Fresh MADIO template detected - proceeding with setup..."
```

### Phase 2: Git Configuration and Validation

Configure git remotes properly for MADIO template updates and validate repository setup:

```bash
echo "🔧 Configuring git for MADIO template updates..."

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "❌ Not in a git repository."
    echo "   Please ensure you've cloned your repository from GitHub."
    echo "   If you used the template, clone YOUR repository, not madio-start."
    exit 1
fi

# Get the current remote URL
ORIGIN_URL=$(git remote get-url origin 2>/dev/null)
if [ -z "$ORIGIN_URL" ]; then
    echo "❌ No origin remote found."
    echo "   Please ensure you've cloned your repository from GitHub."
    exit 1
fi

echo "   📡 Current origin: $ORIGIN_URL"

# Check if the remote URL suggests they're using the template repo directly
if echo "$ORIGIN_URL" | grep -q "madio-start"; then
    echo "⚠️  WARNING: You appear to be using the madio-start template repository directly."
    echo "   This is not recommended. You should:"
    echo "   1. Use the GitHub template to create YOUR repository"
    echo "   2. Clone YOUR repository instead of madio-start"
    echo ""
    
    if [ "$YES_FLAG" = true ]; then
        echo "   --yes flag provided, continuing setup anyway..."
    else
        echo "   Continue anyway? (y/N)"
        read -r confirm
        if [ "$confirm" != "y" ] && [ "$confirm" != "Y" ]; then
            echo "   Setup cancelled. Please create your own repository from the template."
            exit 1
        fi
    fi
fi

# Extract project name from remote URL for later use
PROJECT_NAME=$(echo "$ORIGIN_URL" | sed -E 's/.*[\/:]([^\/]+)\/([^\/]+)\.git$/\2/' | sed 's/\.git$//')
if [ -z "$PROJECT_NAME" ]; then
    PROJECT_NAME=$(basename "$PWD")
fi

echo "   ✅ Git repository validated"
echo "   📦 Project: $PROJECT_NAME"

# Test connectivity to origin
echo "   🌐 Testing remote connectivity..."
if git ls-remote origin >/dev/null 2>&1; then
    echo "      ✅ Origin remote accessible"
else
    echo "      ⚠️  Origin remote not accessible (check network/credentials)"
fi

# Add MADIO template remote (if not already exists)
if ! git remote get-url template 2>/dev/null; then
    echo "   🔗 Adding MADIO template remote for updates..."
    git remote add template https://github.com/petergiordano/madio-start.git
    echo "   ✅ MADIO template remote added"
else
    echo "   ✅ MADIO template remote already configured"
fi

# Test template remote connectivity
if git ls-remote template >/dev/null 2>&1; then
    echo "      ✅ Template remote accessible"
else
    echo "      ⚠️  Template remote not accessible (check network)"
fi

# Verify remote configuration
echo "   📋 Git remote configuration:"
git remote -v | sed 's/^/      /'

# Fetch template to enable template updates
echo "   ⬇️  Fetching template for future updates..."
if git fetch template --quiet; then
    echo "   ✅ MADIO template update capability configured"
else
    echo "   ⚠️  Failed to fetch template (check network connectivity)"
fi
```

### Phase 3: MADIO Project Structure Setup

Transform scaffolding into MADIO project workspace:

```bash
echo "📁 Setting up MADIO project workspace..."

# Copy template library to project root
if [ -d "_project_scaffolding/_template_library" ]; then
    cp -r "_project_scaffolding/_template_library" "_template_library"
    echo "   ✅ Copied _template_library/ (14 MADIO templates)"
else
    echo "   ❌ Template library not found in scaffolding"
    exit 1
fi

# Copy core templates documentation
if [ -f "_project_scaffolding/madio_core_templates.md" ]; then
    cp "_project_scaffolding/madio_core_templates.md" "madio_core_templates.md"
    echo "   ✅ Copied madio_core_templates.md (template selection guide)"
else
    echo "   ❌ Core templates documentation not found"
    exit 1
fi

# Copy Gemini CLI context
if [ -f "_project_scaffolding/GEMINI.md" ]; then
    cp "_project_scaffolding/GEMINI.md" "GEMINI.md"
    echo "   ✅ Copied GEMINI.md (Gemini CLI context)"
else
    echo "   ❌ Gemini context file not found"
    exit 1
fi

# Copy Claude Code CLI context
if [ -f "_project_scaffolding/CLAUDE.md" ]; then
    cp "_project_scaffolding/CLAUDE.md" "CLAUDE.md"
    echo "   ✅ Copied CLAUDE.md (Claude Code CLI context)"
else
    echo "   ❌ Claude context file not found"
    exit 1
fi
```

### Phase 4: Generate AI_CONTEXT.md Bridge File

Create the bridge file from template with project-specific details:

```bash
echo "🌉 Generating AI_CONTEXT.md bridge file..."

# Get project name from directory
PROJECT_NAME=$(basename "$PWD")
CURRENT_DATE=$(date '+%Y-%m-%d %H:%M:%S')
PROJECT_PATH="$PWD"

# Check if AI_CONTEXT template exists
if [ -f "_template_library/madio-template-AI_CONTEXT.md" ]; then
    # Generate AI_CONTEXT.md from template
    cp "_template_library/madio-template-AI_CONTEXT.md" "AI_CONTEXT.md"
    
    # Replace placeholders with project-specific information
    sed -i.bak "s/\[PROJECT_NAME\]/$PROJECT_NAME/g" "AI_CONTEXT.md"
    sed -i.bak "s/\[PROJECT_TYPE\]/MADIO AI System/g" "AI_CONTEXT.md"
    sed -i.bak "s/\[CREATION_DATE\]/$CURRENT_DATE/g" "AI_CONTEXT.md"
    sed -i.bak "s/\[CURRENT_DATE\]/$CURRENT_DATE/g" "AI_CONTEXT.md"
    sed -i.bak "s|\[PROJECT_PATH\]|$PROJECT_PATH|g" "AI_CONTEXT.md"
    sed -i.bak "s/\[setup\|generation\|customization\|testing\|deployment\|production\]/setup/g" "AI_CONTEXT.md"
    
    # Remove backup file
    rm "AI_CONTEXT.md.bak" 2>/dev/null || true
    
    echo "   ✅ Generated AI_CONTEXT.md with project details"
    echo "      Project: $PROJECT_NAME"
    echo "      Date: $CURRENT_DATE"
    echo "      Phase: setup"
else
    echo "   ❌ AI_CONTEXT template not found"
    exit 1
fi
```

### Phase 5: Update .madio Configuration

Update project configuration with current details:

```bash
echo "⚙️ Updating .madio configuration..."

if [ -f ".madio" ]; then
    # Update project name in .madio file
    sed -i.bak "s/\"name\": \"\[PROJECT_NAME\]\"/\"name\": \"$PROJECT_NAME\"/g" ".madio"
    sed -i.bak "s/\"created\": \"\[TIMESTAMP\]\"/\"created\": \"$CURRENT_DATE\"/g" ".madio"
    sed -i.bak "s/\"lastModified\": \"\[TIMESTAMP\]\"/\"lastModified\": \"$CURRENT_DATE\"/g" ".madio"
    
    # Remove backup file
    rm ".madio.bak" 2>/dev/null || true
    
    echo "   ✅ Updated .madio configuration"
    echo "      Project: $PROJECT_NAME"
    echo "      Setup: $CURRENT_DATE"
else
    echo "   ⚠️  .madio configuration file not found (optional)"
fi
```

### Phase 6: Generate Project-Specific README

Create a customized README.md for this specific project:

```bash
echo "📝 Generating project-specific README..."

# Backup current README if it exists
if [ -f "README.md" ]; then
    cp "README.md" "README.md.template-backup"
    echo "   📋 Backed up template README to README.md.template-backup"
fi

# Generate project-specific README
cat > "README.md" << EOF
# $PROJECT_NAME

### **Your AI System Built with MADIO Framework**

This project uses the MADIO (Modular AI Declarative Instruction and Orchestration) framework to create a production-ready AI system for ChatGPT Custom GPTs, Gemini Gems, or Claude Projects.

## 🚀 Project Status

**Setup Complete** ✅ - Ready for AI system generation

## 📁 Project Structure

\`\`\`
$PROJECT_NAME/
├── _template_library/          # 14 MADIO templates for AI system creation
├── madio_core_templates.md     # Template selection guide
├── CLAUDE.md                   # Claude Code CLI context
├── GEMINI.md                   # Gemini CLI context  
├── AI_CONTEXT.md              # Project bridge file
├── GETTING-STARTED.md         # Detailed setup guide
├── .vscode/                   # VS Code workspace configuration
├── .claude/                   # Claude Code commands and scripts
└── setup-ai-companion/       # AI companion setup instructions
\`\`\`

## 🎯 Next Steps

### 1. Generate Your AI System
\`\`\`bash
# Using Claude Code CLI
/generate-ai-system "describe your AI system here"

# Examples:
/generate-ai-system "customer support bot with friendly personality"
/generate-ai-system "content writing AI with SEO optimization"
/generate-ai-system "data analysis AI with evaluation frameworks"
\`\`\`

### 2. Customize and Deploy
- Review generated documents in your project
- Customize for your specific use case
- Deploy to your chosen platform (ChatGPT/Gemini/Claude)

### 3. Ongoing Development
\`\`\`bash
# Switch to Gemini CLI for refinement
gemini "review my MADIO documents and suggest improvements"
\`\`\`

## 🔧 Available Commands

| Command | Description |
|---------|-------------|
| \`/generate-ai-system\` | Generate complete AI system from templates |
| \`/madio-doctor\` | Diagnose project issues |
| \`/madio-enable-sync\` | Set up Google Docs synchronization |
| \`/push-to-docs\` | Sync documents to Google Docs (traditional config mode) |
| **NEW:** Directory sync | \`python .claude/scripts/sync_to_docs.py --directory synced_docs\` |

## 📚 Documentation

- **[GETTING-STARTED.md](GETTING-STARTED.md)** - Complete setup and usage guide
- **[madio_core_templates.md](madio_core_templates.md)** - Template selection guide
- **[setup-ai-companion/](setup-ai-companion/)** - AI companion integration guides

## 🌐 Template Updates

This project maintains connection to the MADIO template for updates:

\`\`\`bash
# Get latest template improvements
git pull template main
\`\`\`

## 🔗 Links

- **Template Repository**: [madio-start](https://github.com/petergiordano/madio-start)
- **Framework Documentation**: See template repository for full documentation
- **Created**: $CURRENT_DATE
- **Origin**: $ORIGIN_URL

---

*Generated by MADIO Framework - Modular AI Declarative Instruction and Orchestration*
EOF

echo "   ✅ Generated project-specific README.md"
echo "      Project: $PROJECT_NAME"
echo "      Created: $CURRENT_DATE"
echo "      Origin: $ORIGIN_URL"
```

### Phase 7: Clean Up and Finalize

Clean up scaffolding and create setup completion marker:

```bash
echo "🧹 Finalizing MADIO setup..."

# Remove scaffolding directory (contents now copied to root)
rm -rf "_project_scaffolding/"
echo "   ✅ Removed _project_scaffolding/ (contents copied to root)"

# Clean up any test files that shouldn't be in user projects
if [ -d ".claude/tests" ]; then
    echo "   🧹 Removing framework test files..."
    rm -rf ".claude/tests"
    echo "   ✅ Cleaned up test directory"
fi

# Create setup completion marker
touch ".madio-setup-complete"
echo "   ✅ Created setup completion marker"

# Commit the MADIO setup
echo "💾 Creating MADIO setup commit..."
git add -A
git commit -m "feat: initialize MADIO project workspace

- Copy _template_library/ (14 MADIO templates)
- Copy madio_core_templates.md (template selection guide)
- Copy GEMINI.md (Gemini CLI context)
- Copy CLAUDE.md (Claude Code CLI context)  
- Generate AI_CONTEXT.md (project bridge file)
- Update .madio configuration
- Remove _project_scaffolding/ (contents copied)
- Configure template remote for updates

Project: $PROJECT_NAME
Setup: $CURRENT_DATE
Template: $(git remote get-url template)"

echo "   ✅ MADIO project setup committed to git history"
```

### Phase 8: VS Code Configuration and Getting Started

```bash
echo "🔧 Setting up VS Code workspace..."

# Check if VS Code is available
if command -v code >/dev/null 2>&1; then
    echo "   ✅ VS Code detected"
    
    # Check if extensions are available for installation
    if [ -f ".vscode/extensions.json" ]; then
        echo "   📦 VS Code extensions configured:"
        echo "      • Python support (ms-python.python)"
        echo "      • Markdown editing (davidanson.vscode-markdownlint)"
        echo "      • Git integration (eamodio.gitlens)"
        echo "      • Enhanced markdown preview (shd101wyy.markdown-preview-enhanced)"
        echo ""
        echo "   💡 To install recommended extensions:"
        echo "      1. Open VS Code Extensions panel (Ctrl+Shift+X / Cmd+Shift+X)"
        echo "      2. Click 'Install Workspace Recommended Extensions'"
        echo "      3. Or run: code --install-extension <extension-id>"
    else
        echo "   ❌ VS Code extensions configuration not found"
    fi
    
    # Check if workspace settings are applied
    if [ -f ".vscode/settings.json" ]; then
        echo "   ⚙️  VS Code workspace settings configured"
    else
        echo "   ❌ VS Code workspace settings not found"
    fi
else
    echo "   ⚠️  VS Code not detected in PATH"
    echo "      Install VS Code and add 'code' command to PATH for full MADIO experience"
fi

# Move getting started file to prominent location
if [ -f "GETTING-STARTED.md" ]; then
    echo "   📖 Getting started guide is ready at: GETTING-STARTED.md"
    echo "      Open this file after setup for detailed next steps"
else
    echo "   ❌ Getting started guide not found"
fi

echo ""
```

### Phase 9: Success Message and Next Steps

```bash
echo ""
echo "🎉 MADIO project setup complete!"
echo ""
echo "📁 Your MADIO project structure:"
echo "   ✅ _template_library/ (14 MADIO templates)"
echo "   ✅ madio_core_templates.md (template selection guide)"
echo "   ✅ GEMINI.md (Gemini CLI context)"
echo "   ✅ CLAUDE.md (Claude Code CLI context)"
echo "   ✅ AI_CONTEXT.md (project bridge file)"
echo "   ✅ .madio (project configuration)"
echo "   ✅ .vscode/ (VS Code workspace configuration)"
echo "   ✅ GETTING-STARTED.md (detailed next steps guide)"
echo "   ✅ README.md (project-specific documentation)"
echo "   🔗 Git remotes configured (origin + template)"
echo ""
echo "🔄 Template Update Capability:"
echo "   📡 Origin: $(git remote get-url origin)"
echo "   🔗 Template: $(git remote get-url template)"
echo "   💡 Get updates anytime: git pull template main"
echo ""
echo "🚀 Your MADIO Development Journey:"
echo ""
echo "   1. ✅ Use template on GitHub → your-username/your-project-name"
echo "   2. ✅ Clone YOUR repository → local development"
echo "   3. ✅ /madio-setup (workspace setup + template remote) ← YOU ARE HERE"
echo "   4. 🔄 Generate AI system using MADIO templates"
echo "   5. 🔄 Customize & Deploy to production platforms"
echo ""
echo "💡 Next Steps - Generate Your AI System:"
echo ""
echo "   📖 FIRST: Read GETTING-STARTED.md for detailed guidance"
echo "   📖 File: $(pwd)/GETTING-STARTED.md"
echo ""
echo "   🎯 New Users: Use /madio-onboard for complete setup"
echo "   /madio-onboard"
echo ""
echo "   🎯 Generate AI System:"
echo "   /generate-ai-system \"[describe your AI system]\""
echo ""
echo "   🎯 Examples:"
echo "   /generate-ai-system \"customer support bot with friendly personality\""
echo "   /generate-ai-system \"content writing AI with SEO optimization\""
echo "   /generate-ai-system \"data analysis AI with evaluation frameworks\""
echo ""
echo "   🎯 After initial generation, switch to Gemini CLI:"
echo "   gemini \"Review my generated MADIO documents and suggest improvements\""
echo "   gemini \"Add [feature] capability to my AI system\""
echo "   gemini \"Validate my MADIO project structure\""
echo ""
echo "🧭 Navigation Commands:"
echo "   • Update AI_CONTEXT.md: Use Gemini CLI during development"
echo "   • Check project status: Read AI_CONTEXT.md"
echo "   • View available templates: Check madio_core_templates.md"
echo "   • Get template updates: git pull template main"
echo ""
echo "🌉 AI Collaboration Bridge:"
echo "   • Local CLI tools use project files directly"
echo "   • Browser AI gets context via AI_CONTEXT.md transfer"
echo "   • Seamless handoff between development and deployment"
echo ""
echo "Ready to create your AI system with MADIO! 🚀"
```

## Template Update Workflow

### **How Users Get MADIO Updates:**

1. **Automatic template configuration** - `/madio-setup` adds template remote
2. **Simple update command** - `git pull template main`
3. **Smart conflict resolution** - Git preserves user customizations
4. **Selective updates** - Users can review changes before merging

### **What Gets Updated:**
- **Template library** (`_template_library/`) - New and improved MADIO templates
- **Documentation** (`madio_core_templates.md`) - Updated template guidance
- **CLI context** (`GEMINI.md`, `CLAUDE.md`) - Enhanced command workflows
- **Framework files** - Latest MADIO framework improvements

### **What Stays Custom:**
- **Generated documents** (project-specific MADIO files) - User's AI system
- **Project context** (`AI_CONTEXT.md`) - User's bridge file
- **Configuration** (`.madio`) - User's project settings
- **Customizations** - User's modifications and adaptations

## Safety Features

### **Prevents Double Execution**
- Checks for `.madio-setup-complete` marker file
- Verifies scaffolding directory exists
- Clear error messages with appropriate next steps

### **Git Safety & Template Preservation**
- **Preserves fork relationship** - Keeps connection to user's GitHub repo
- **Adds template remote** - Enables MADIO template updates
- **Maintains git history** - Proper lineage for template evolution
- **Smart remote detection** - Verifies and reports git configuration

### **MADIO Framework Validation**
- **Template integrity checks** - Verifies all required templates exist
- **File transformation validation** - Ensures successful setup
- **Configuration updates** - Proper .madio file updating
- **Bridge file generation** - AI_CONTEXT.md with project specifics

## Error Handling

### **Template Validation**
```bash
# Verify MADIO template integrity
if [ ! -d "_project_scaffolding/_template_library" ]; then
    echo "❌ Error: MADIO template library not found"
    echo "This may not be a valid madio-start template"
    exit 1
fi

# Count expected templates (should be 14)
TEMPLATE_COUNT=$(find "_project_scaffolding/_template_library" -name "*.md" | wc -l)
if [ "$TEMPLATE_COUNT" -lt 14 ]; then
    echo "⚠️ Warning: Only $TEMPLATE_COUNT templates found (expected 14)"
    echo "Template library may be incomplete"
fi
```

### **Bridge File Generation**
```bash
# Verify AI_CONTEXT.md generation
if [ ! -f "AI_CONTEXT.md" ]; then
    echo "❌ Error: Failed to generate AI_CONTEXT.md bridge file"
    echo "Check template availability and permissions"
    exit 1
fi

# Verify placeholder replacement
if grep -q "\[PROJECT_NAME\]" "AI_CONTEXT.md"; then
    echo "⚠️ Warning: Some placeholders may not have been replaced"
    echo "Check AI_CONTEXT.md for any remaining [BRACKETED_TEXT]"
fi
```

## Command Positioning

### **MADIO Framework Setup**
- Transforms madio-start template into working MADIO project
- Configures template remote for framework evolution
- Generates project-specific bridge file
- **Enables continuous MADIO improvement inheritance**

### **MADIO Workflow Integration**
```
User journey:
Use madio-start template → Clone YOUR repository → cd your-project → /madio-setup → Generate AI system
                                                                    ↓
                                                          Configures MADIO framework
```

### **MADIO Evolution Support**
- **`/madio-setup`** = One-time MADIO workspace preparation
- **`git pull template main`** = Get latest MADIO framework improvements
- **Gemini CLI** = AI system generation using MADIO templates
- **AI_CONTEXT.md** = Bridge for browser AI deployment

## Key Benefits

### **Complete MADIO Framework Access**
- 14 production-ready templates immediately available
- Template selection guidance and examples
- CLI context for both Gemini and Claude Code
- Bridge file for seamless AI collaboration

### **Framework Evolution Inheritance**
- Template improvements flow to existing projects
- New templates become available automatically
- Framework bug fixes reach users immediately
- Quality improvements benefit all MADIO projects

### **Professional MADIO Workflow**
- Proper template relationship maintained
- GitHub integration preserved for MADIO community
- Standard framework evolution model
- Clean git history with template attribution
