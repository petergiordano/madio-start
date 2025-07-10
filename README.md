# MADIO Framework - Start Building AI Systems

### **Build production-ready AI systems using structured English**

The MADIO (Modular AI Declarative Instruction and Orchestration) framework enables you to create sophisticated AI applications for ChatGPT Custom GPTs, Gemini Gems, or Claude Projects using **AI system documents** - structured markdown files containing declarations, instructions, orchestration logic, methodology frameworks, and other specifications that drive AI agents.

MADIO uses a systematic, template-driven approach with these AI system documents.

## 🚀 Getting Started (5 minutes)

### **Prerequisites: Desktop/CLI Access Required**

**⚠️ IMPORTANT: Filesystem Access Required**

MADIO requires filesystem access for true collaboration between your local development environment and AI assistants. You'll need:

**For Initial Setup (Required):**
- **Claude Code CLI** (research preview) in VS Code
- **Claude Desktop App** (not browser version)
- Local filesystem access for document reading/writing

**For Ongoing Development (Recommended):**
- **Gemini CLI** installed and configured
- **VS Code** with integrated terminal
- Command: `gemini "your request"` from project directory

**Complete Workflow:**
- **Claude Code** for initial project setup and MADIO generation
- **Gemini CLI** for ongoing development, refinement, and content creation
- **VS Code** as your IDE with terminal access
- **Git** for template inheritance and version control

### **Step 1: Use This Template**

**Create your project repository on GitHub:**

1. **Use this template:**
   - Click the **"Use this template"** button at the top of this GitHub page
   - Choose **"Create a new repository"**
   - Select your GitHub account as the owner
   - Name your repository (e.g., `my-ai-assistant`, `customer-support-bot`)
   - Choose public or private as needed
   - Click **"Create repository"**

2. **Clone YOUR new repository locally:**
   ```bash
   git clone https://github.com/YOUR-USERNAME/YOUR-PROJECT-NAME.git
   cd YOUR-PROJECT-NAME
   ```

3. **Open in VS Code:**
   ```bash
   code .
   ```

4. **Save workspace for your project:**
   - In VS Code: File → Save Workspace As...
   - Name it: `your-project-name.code-workspace`
   - Save it in your project root directory
   - When prompted, choose "Open Workspace"

5. **Import Claude Desktop MCP Servers:**
   - Do this on the terminal, NOT within Claude Code!
```bash
claude mcp add-from-claude-desktop
```


### **Step 2: Set Up Your MADIO Project**

**For new users, use the streamlined onboarding (recommended):**

```bash
# Complete setup with validation and guidance (2-12 minutes)
/madio-onboard
```

**For advanced users, use individual commands:**

```bash
# Initialize your MADIO project (one-time setup)
/madio-setup

# Generate your AI system
/generate-ai-system "[describe your AI system]"
```

**Essential Commands for First Success:**

```bash
# 1. Set up Google Docs sync (one-time setup for AI integration)
/madio-enable-sync

# 2. Sync your documents to Google Docs (for Claude Projects, ChatGPT, etc.)
/push-to-docs

# 3. Troubleshoot any issues
/madio-doctor
```

> 📖 **Need help with sync setup?** See the complete [**SYNC_SETUP.md**](SYNC_SETUP.md) guide

**After setup, switch to Gemini CLI for ongoing development:**

```bash
# Use Gemini CLI for refinement and iteration
gemini "Review my generated AI system documents and suggest improvements"
gemini "Update the project_system_instructions.md AI system document to include [specific feature]"
gemini "Validate my AI system documents and identify any issues"
```

> 📋 **Quick Start Path:** `/madio-setup` → `/madio-import-docs` (existing AI docs) OR `/generate-ai-system` (new AI system) → `/madio-enable-sync` → `/push-to-docs` → Success!

**What `/madio-onboard` does:**
1. ✅ Validates prerequisites (Python, Git, VS Code)
2. ✅ Confirms you're in YOUR project (not the template)
3. ✅ Configures git remote for template updates
4. ✅ Sets up Python virtual environment
5. ✅ Moves templates from `_project_scaffolding/` to your project root
6. ✅ Updates `.madio` configuration with your project name
7. ✅ Creates initial project structure
8. ✅ Optionally sets up Google Docs sync
9. ✅ Validates setup success with health checks
10. ✅ Commits the setup changes
11. ✅ Enables template inheritance via `git pull template main`

## 🎯 Complete User Journey

```
1. Use template on GitHub → Creates your-username/your-project-name
2. Clone YOUR repository → Local development environment
3. cd your-project-name → Enter YOUR project directory
4. Open in VS Code → Professional IDE environment
5. /madio-onboard → Streamlined setup with validation (recommended)
   OR /madio-setup → Advanced users only
6. Generate AI system → Creates hierarchical AI system documents
7. Customize & Deploy → Ready for production use
```

## 🤝 AI Collaboration Architecture

### **Local Development (Filesystem Access)**
```
VS Code Project
├── Claude Code → Initial setup & MADIO generation
├── Gemini CLI → Ongoing development & refinement  
└── Your Files → Direct filesystem access
```

### **Deployment (Browser/App Based)**
```
Generated Documents → Platform Deployment
├── OpenAI CustomGPT → Copy project_system_instructions.md
├── Google Gemini Gem → Combine documents per .madio config
└── Claude Project → Upload to project knowledge
```

### **AI_CONTEXT.md Bridge File**

**Purpose:** Provides seamless context transfer between local CLI tools and deployed AI systems.

**Location:** Auto-generated in project root after `/madio-setup`

**Contains:**
- Project overview and current status
- Key decisions and architectural choices  
- Document hierarchy and relationships
- Recent changes and development notes
- Deployment configuration summary

**Usage:**
```bash
# Initially created by Claude Code during setup
/madio-setup  # Creates AI_CONTEXT.md

# Updated by Gemini CLI during development
gemini "Update AI_CONTEXT.md with recent changes"

# Copy to browser-based AI for continuity
# Paste into Claude Project knowledge or Gemini Gem context
```

### **CLI Context Files**

**GEMINI.md** - Gemini CLI specific context and commands
- MADIO template selection guidance
- Auto-update triggers for AI_CONTEXT.md
- Setup and validation workflows

**CLAUDE.md** - Claude Code CLI specific context and workflow
- Initial setup and MADIO document generation
- Plan Mode integration for complex tasks
- Handoff procedures to Gemini CLI for ongoing development

**Both files are copied to user projects** and reference AI_CONTEXT.md as the primary source of project-specific context.

## 📂 Project Structure

After `/madio-setup`, your project will have:

```
your-project/
├── .claude/                    # Claude Code CLI integration
│   ├── commands/               # Available slash commands
│   │   ├── madio-setup.md      # One-time project initialization
│   │   ├── generate-ai-system.md # AI system generation with customization
│   │   ├── madio-import-docs.md # Import existing AI system documents
│   │   ├── madio-doctor.md     # Project health diagnostics
│   │   ├── madio-enable-sync.md # Optional Google Docs sync setup
│   │   ├── push-to-docs.md     # Sync documents to Google Docs
│   │   └── orient.md           # Check project status
│   ├── scripts/                # Optional Google Docs sync (if enabled)
│   │   ├── sync_to_docs.py     # Sync script
│   │   ├── requirements.txt    # Python dependencies
│   │   ├── setup.sh           # Sync setup script
│   │   └── sync_config.json   # Document mapping config
│   └── settings.local.json     # Claude Code settings
├── setup-ai-companion/         # AI companion setup guides
│   ├── SETUP_INSTRUCTIONS.md
│   ├── CLAUDE_PROJECT_INSTRUCTIONS.md
│   ├── GEMINI_GEM_INSTRUCTIONS.md
│   ├── CHATGPT_INSTRUCTIONS.md
│   └── WORKFLOW_REFERENCE.md
├── docs/                       # Documentation
│   ├── GOOGLE_CLOUD_SETUP.md  # Google Docs sync setup guide
│   ├── MADIO_CONFIGURATION.md # Configuration reference
│   └── AI_INTEGRATION_SUMMARY.md
├── AI_CONTEXT.md               # Bridge file for AI collaboration
├── CLAUDE.md                   # Claude Code CLI context
├── GEMINI.md                   # Gemini CLI context
├── .madio                      # Project configuration
├── madio_core_templates.md     # Template selection guide
├── your-project.code-workspace # VS Code workspace
├── README.md                   # Your project documentation
└── [Generated AI system documents after /generate-ai-system]
    ├── project_system_instructions.md # Core AI identity (Tier 1)
    ├── orchestrator.md                # Workflow controller (Tier 2)
    └── [Additional documents based on complexity]
        ├── character_voice_authority.md
        ├── content_operations.md
        ├── methodology_framework.md
        └── [...other Tier 3 documents]
```

**Note:** `_template_library/` is automatically removed after document generation to keep your project clean. Templates remain available via `git pull template main`.

## 🏗️ Building Your AI System

### **Quick Start Examples (Using Claude Code)**

**AI Writing Assistant:**
```bash
/generate-ai-system "AI writing assistant that helps with blog posts, maintains consistent tone, and includes SEO optimization"
```

**Customer Support Bot:**
```bash
/generate-ai-system "customer support bot with friendly personality, FAQ handling, and escalation protocols"
```

**Data Analysis Assistant:**
```bash
/generate-ai-system "data analysis AI that can evaluate datasets, generate insights, and create reports"
```

**Let MADIO Choose Templates:**
```bash
/generate-ai-system "[describe your idea] - select appropriate MADIO templates based on complexity"
```

### **Claude Code Commands Available:**

**Setup & Navigation:**
- `/madio-setup` - One-time project initialization (add `--yes` for unattended mode)
- `/orient` - Check current project status and next steps
- `/madio-doctor` - Comprehensive project health check and diagnostics

**AI System Generation:**
- `/generate-ai-system` - Interactive MADIO system creation with deep customization
- `/generate-ai-system "[description]"` - Direct system generation
- `/madio-import-docs` - Import existing AI system documents with automatic context generation

**Optional Features:**
- `/madio-enable-sync` - Set up Google Docs sync (optional, most users don't need this)
- `/push-to-docs` - Sync documents to Google Docs (requires sync setup)

**Examples:**
```bash
# Generate new AI system from templates
/generate-ai-system "customer support bot with friendly personality"
/generate-ai-system "content writing AI with SEO optimization" 
/generate-ai-system "data analysis system with evaluation frameworks"

# Import existing AI system documents
/madio-import-docs                    # Import from current directory
/madio-import-docs --source ./docs    # Import from specific directory
/madio-import-docs --copy --no-sync   # Import safely without Google sync

# Unattended setup for automation
/madio-setup --yes                    # Skip all prompts for CI/CD pipelines
```

## 📚 MADIO Templates

### **Always Required (Tier 1 & 2)**
- `project_system_instructions` - Core AI identity and rules
- `orchestrator` - Step-by-step workflow controller

### **Content & Character (Tier 3)**
- `character_voice_authority` - Personality and voice consistency
- `content_operations` - Content validation and curation
- `standard` - Templated output formats

### **Analysis & Evaluation (Tier 3)**
- `methodology_framework` - Complex analysis processes
- `rubrics_evaluation` - Multi-dimensional scoring
- `strategic_framework` - Strategic assessment
- `research_protocols` - Evidence collection

### **Visual & Brand (Tier 3)**
- `visual_design_standards` - Brand consistency
- `visual_asset_generation` - Automated image creation

### **Implementation (Tier 3)**
- `implementation_roadmap` - Phased execution plans
- `document_reference_map` - Complex project mapping

## 🚀 Deployment

After generating and customizing your AI system documents:

### **OpenAI CustomGPT**
1. Copy `project_system_instructions.md` content
2. Paste as GPT instructions
3. Upload other documents to Knowledge base
4. Copy `AI_CONTEXT.md` for continuity

### **Google Gemini Gem**
1. Combine core documents into Gem instructions
2. Configure according to your `.madio` settings
3. Include `AI_CONTEXT.md` in context

### **Claude Project**
1. Use `project_system_instructions.md` as project instructions
2. Upload supporting documents to project knowledge
3. Add `AI_CONTEXT.md` to project knowledge

## 🤝 Set Up Your AI Companion

Enhance your MADIO development with a strategic AI companion that works alongside your local CLI tools:

### **Companion Options:**
- **Claude Project** (Recommended) - Strategic analysis and deployment guidance
- **Google Gemini Gem** - Native integration with Gemini CLI workflow  
- **ChatGPT Custom GPT** - Interactive system design and planning

### **Three-Way Collaboration:**
```
Local CLI (Development) ↔ AI_CONTEXT.md Bridge ↔ Browser AI (Strategy)
```

**Setup Instructions:** See `setup-ai-companion/` directory for complete setup guides for each platform.

**Benefits:**
- Strategic template selection guidance
- Quality assurance and architecture review
- Platform-specific deployment optimization
- Context continuity across development sessions

## 🔄 Google Docs Sync Integration (Optional)

### **Advanced Feature: Local Development + Cloud Knowledge**

**⚠️ IMPORTANT: This is an OPTIONAL feature that most users don't need.**

For users who want automatic synchronization between local AI system documents and Google Docs:

**When You Might Want This:**
- Using Claude Projects as your primary AI platform
- Want automatic document updates in Claude Project knowledge
- Collaborating with business users who prefer Google Docs

**When You DON'T Need This:**
- Using OpenAI CustomGPT or Gemini Gems only
- Prefer manual document uploads
- Want to keep things simple

**Setup (Optional):**
```bash
# Only run if you specifically need Google Docs sync
/madio-enable-sync
```

**What This Enables (If You Choose to Use It):**
- **Automatic Sync**: Local file changes automatically update Google Docs
- **Claude Project Integration**: Documents auto-refresh in Claude Project knowledge
- **No Manual Uploads**: Skip the copy-paste step for document updates

### **Available Commands (If Sync Enabled):**
- `/madio-enable-sync` - One-time setup for Google Docs sync (optional)
- `/push-to-docs` - Sync all configured files to Google Docs
- `/push-to-docs --file file.md doc-id` - Sync specific file

**💡 Remember: MADIO works perfectly without Google Docs sync!**

## 🔄 Getting Template Updates

```bash
# Pull latest MADIO improvements (after /madio-setup)
git pull template main

# Your customizations remain intact
# Resolve any conflicts if needed
```

## ⚡ Advanced Features

- **AI_CONTEXT.md Bridge** - Seamless context transfer between local and deployed AI
- **Template Inheritance** - Get framework improvements while keeping your changes
- **Hierarchical Authority** - Clear document precedence prevents conflicts
- **Quality Gates** - Built-in validation ensures production readiness
- **Multi-Platform Export** - Same system works on OpenAI, Google, and Anthropic
- **Modular Architecture** - Update components without breaking the system

## 🆘 Troubleshooting

**"Claude Code not working"**
- Ensure Claude Desktop app is installed (not browser version)
- Enable filesystem permissions in Claude Desktop
- Install Claude Code CLI in VS Code terminal
- Try restarting VS Code if commands not recognized

**"Gemini CLI not working"**
- Install: `pip install google-generativeai` 
- Configure: Set API key in environment
- Verify: `gemini --version`

**"I'm getting git errors"**
- Ensure you're in YOUR project: `pwd` should show your-project-name
- Check remotes: `git remote -v` should show YOUR repository

**"AI doesn't understand my project context"**
- Ensure `AI_CONTEXT.md` is up to date
- Copy its contents to your browser-based AI
- Run `gemini "Update AI_CONTEXT.md with current project status"`

**"Commands not working after setup"**
- Ensure you used Claude Code for initial setup: `/madio-setup`
- For ongoing development, switch to Gemini CLI
- Reference generated documents: "Use the AI system documents in my project"

**"Which templates should I use?"**
- Let Claude Code decide during `/generate-ai-system`
- Check the Template Selection Matrix in `madio_core_templates.md`
- Use Gemini CLI for refinements: "Suggest additional templates for my use case"

**"Import command not working with my documents"**
- Ensure documents follow MADIO naming conventions (e.g., `project_system_instructions.md`, `orchestrator.md`)
- Check documents contain tier markers in content (`Tier 1`, `Tier 2`, etc.)
- Use `--copy` flag to preserve originals during testing: `/madio-import-docs --copy`
- Run `/madio-doctor` for comprehensive project diagnostics

## 📈 Why MADIO Works

- **Systematic Design** - Hierarchical documents prevent conflicts
- **Production Ready** - Built-in quality control and error handling
- **Platform Agnostic** - Deploy anywhere, maintain once
- **Scalable Architecture** - From simple bots to complex systems
- **Template-Driven** - Consistent, professional results every time
- **AI Collaboration** - Seamless handoff between local development and deployment

---

**Ready to build? Install Claude Code → Use Template → Clone → `/madio-setup` → `/generate-ai-system` → Switch to Gemini CLI**