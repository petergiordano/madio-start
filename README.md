# MADIO Framework - Start Building AI Systems

### **Build production-ready AI systems using structured English**

The MADIO (Modular AI Declarative Instruction and Orchestration) framework enables you to create sophisticated AI applications for ChatGPT Custom GPTs, Gemini Gems, or Claude Projects using a systematic, template-driven approach.

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

### **Step 2: Set Up Your MADIO Project**

**Open terminal in VS Code and run (using Claude Code):**

```bash
# Initialize your MADIO project (one-time setup)
/madio-setup

# Generate your AI system
/generate-ai-system "[describe your AI system]"
```

**After setup, switch to Gemini CLI for ongoing development:**

```bash
# Use Gemini CLI for refinement and iteration
gemini "Review my generated MADIO documents and suggest improvements"
gemini "Update the project_system_instructions.md to include [specific feature]"
gemini "Validate my MADIO project structure and identify any issues"
```

**What `/madio-setup` does:**
1. Validates you're in YOUR project (not the template)
2. Configures git remote for template updates
3. Moves templates from `_project_scaffolding/` to your project root
4. Updates `.madio` configuration with your project name
5. Creates initial project structure
6. Commits the setup changes
7. Enables template inheritance via `git pull template main`

## 🎯 Complete User Journey

```
1. Use template on GitHub → Creates your-username/your-project-name
2. Clone YOUR repository → Local development environment
3. cd your-project-name → Enter YOUR project directory
4. Open in VS Code → Professional IDE environment
5. /madio-setup → One-time project initialization
6. Generate AI system → Creates hierarchical MADIO documents
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
├── _template_library/          # MADIO templates (reference)
│   ├── madio_template_tier1_project_system_instructions.md
│   ├── madio_template_tier2_orchestrator.md
│   └── madio_template_tier3_*.md (12 supporting templates)
├── .claude/                    # Claude Code commands
│   ├── commands/
│   │   ├── madio-setup.md
│   │   ├── generate-ai-system.md
│   │   └── orient.md
│   └── settings.local.json
├── setup-ai-companion/         # AI companion setup guides
│   ├── SETUP_INSTRUCTIONS.md
│   ├── CLAUDE_PROJECT_INSTRUCTIONS.md
│   ├── GEMINI_GEM_INSTRUCTIONS.md
│   ├── CHATGPT_INSTRUCTIONS.md
│   └── WORKFLOW_REFERENCE.md
├── AI_CONTEXT.md               # Bridge file for AI collaboration
├── CLAUDE.md                   # Claude Code CLI context
├── GEMINI.md                   # Gemini CLI context
├── .madio                      # Project configuration (see docs/MADIO_CONFIGURATION.md)
├── madio_core_templates.md     # Template selection guide
├── README.md                   # Your project documentation
└── [Your generated MADIO documents will go here]
```

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
- `/madio-setup` - One-time project initialization
- `/orient` - Check current project status and next steps

**AI System Generation:**
- `/generate-ai-system` - Interactive MADIO system creation
- `/generate-ai-system "[description]"` - Direct system generation

**Examples:**
```bash
/generate-ai-system "customer support bot with friendly personality"
/generate-ai-system "content writing AI with SEO optimization" 
/generate-ai-system "data analysis system with evaluation frameworks"
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

After generating and customizing your MADIO documents:

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
- Reference generated documents: "Use the MADIO documents in my project"

**"Which templates should I use?"**
- Let Claude Code decide during `/generate-ai-system`
- Check the Template Selection Matrix in `madio_core_templates.md`
- Use Gemini CLI for refinements: "Suggest additional templates for my use case"

## 📈 Why MADIO Works

- **Systematic Design** - Hierarchical documents prevent conflicts
- **Production Ready** - Built-in quality control and error handling
- **Platform Agnostic** - Deploy anywhere, maintain once
- **Scalable Architecture** - From simple bots to complex systems
- **Template-Driven** - Consistent, professional results every time
- **AI Collaboration** - Seamless handoff between local development and deployment

---

**Ready to build? Install Claude Code → Use Template → Clone → `/madio-setup` → `/generate-ai-system` → Switch to Gemini CLI**