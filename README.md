# MADIO Framework - Start Building AI Systems

### **Build production-ready AI systems using structured English**

The MADIO (Modular AI Declarative Instruction and Orchestration) framework enables you to create sophisticated AI applications for ChatGPT Custom GPTs, Gemini Gems, or Claude Projects using a systematic, template-driven approach.

## 🚀 Getting Started (5 minutes)

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

**Open terminal in VS Code and run:**

```bash
# Initialize your MADIO project (one-time setup)
gemini "/madio-setup"

# Generate your AI system
gemini "Create a [describe your AI system] using the MADIO framework"
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

## 📂 Project Structure

After `/madio-setup`, your project will have:

```
your-project/
├── _template_library/          # MADIO templates (reference)
│   ├── madio_template_tier1_project_system_instructions.md
│   ├── madio_template_tier2_orchestrator.md
│   └── madio_template_tier3_*.md (12 supporting templates)
├── .madio                      # Project configuration
├── madio_core_templates.md     # Template selection guide
├── README.md                   # Your project documentation
├── GEMINI.md                   # Gemini context instructions
└── [Your generated MADIO documents will go here]
```

## 🏗️ Building Your AI System

### **Quick Start Examples**

**AI Writing Assistant:**
```bash
gemini "Create an AI writing assistant using MADIO that helps with blog posts, maintains consistent tone, and includes SEO optimization"
```

**Customer Support Bot:**
```bash
gemini "Create a customer support bot using MADIO with friendly personality, FAQ handling, and escalation protocols"
```

**Data Analysis Assistant:**
```bash
gemini "Create a data analysis AI using MADIO that can evaluate datasets, generate insights, and create reports"
```

### **Let MADIO Choose Templates:**
```bash
gemini "I want to create [describe your idea]. Use the MADIO framework to build this, selecting appropriate templates based on complexity."
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

### **Google Gemini Gem**
1. Combine core documents into Gem instructions
2. Configure according to your `.madio` settings

### **Claude Project**
1. Use `project_system_instructions.md` as project instructions
2. Upload supporting documents to project knowledge

## 🔄 Getting Template Updates

```bash
# Pull latest MADIO improvements (after /madio-setup)
git pull template main

# Your customizations remain intact
# Resolve any conflicts if needed
```

## ⚡ Advanced Features

- **Template Inheritance** - Get framework improvements while keeping your changes
- **Hierarchical Authority** - Clear document precedence prevents conflicts
- **Quality Gates** - Built-in validation ensures production readiness
- **Multi-Platform Export** - Same system works on OpenAI, Google, and Anthropic
- **Modular Architecture** - Update components without breaking the system

## 🆘 Troubleshooting

**"I'm getting git errors"**
- Ensure you're in YOUR project: `pwd` should show your-project-name
- Check remotes: `git remote -v` should show YOUR repository

**"Gemini doesn't see the templates"**
- Run `/madio-setup` first
- Reference: "Use the MADIO templates in _template_library/"

**"Which templates should I use?"**
- Check the Template Selection Matrix in `madio_core_templates.md`
- Or let Gemini decide based on your requirements

## 📈 Why MADIO Works

- **Systematic Design** - Hierarchical documents prevent conflicts
- **Production Ready** - Built-in quality control and error handling
- **Platform Agnostic** - Deploy anywhere, maintain once
- **Scalable Architecture** - From simple bots to complex systems
- **Template-Driven** - Consistent, professional results every time

---

**Ready to build? Use Template → Clone → `/madio-setup` → Generate Your AI System**