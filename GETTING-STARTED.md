# 🚀 Getting Started with MADIO

Welcome! You're about to create a professional AI system using the MADIO framework. This guide will walk you through your first project.

## ⚠️ IMPORTANT: Did You Use the Template?

This guide assumes you've already:
1. Used the GitHub template to create YOUR repository
2. Cloned YOUR repository (not madio-start)
3. Opened YOUR project in VS Code

**If not**, go back to the [README](README.md) and follow Step 1 first!

## 📋 Pre-Flight Checklist

Before starting, verify:
- [ ] You're in YOUR project directory: `pwd` shows your-project-name
- [ ] Git is configured: `git remote -v` shows YOUR repository
- [ ] VS Code is open with YOUR project
- [ ] Claude Code CLI is installed and working
- [ ] Gemini CLI installed for ongoing development (optional for initial setup)

## 🏗️ Step 1: Initialize Your MADIO Project

### Option A: Streamlined Onboarding (Recommended for New Users)

```bash
# Interactive setup with validation and guidance
/madio-onboard
```

This comprehensive command will:
- ✅ Check all prerequisites (Python, Git, VS Code)
- ✅ Validate you're in the right directory
- ✅ Configure template inheritance
- ✅ Set up your project structure
- ✅ Generate your AI_CONTEXT.md bridge file
- ✅ Update configuration files
- ✅ Prepare for AI system generation
- ✅ Optionally set up Google Docs sync
- ✅ Validate setup success

### Option B: Core Setup Only (Advanced Users)

```bash
# Interactive setup (prompts for confirmation when needed)
/madio-setup

# Unattended setup (skips all prompts, perfect for automation)
/madio-setup --yes
```

**When to use `--yes` flag:**
- ✅ Automation scripts or CI/CD pipelines
- ✅ You've run setup before and know what to expect
- ✅ Batch processing multiple projects
- ✅ You want fastest possible setup time

**The `--yes` flag will:**
- Skip all confirmation prompts
- Use default values for all options
- Complete setup without user intervention
- Still perform all safety validations

## 🤖 Step 2A: Generate Your AI System (New Documents)

**Use this option if you're starting from scratch:**

**Use Claude Code for initial generation:**

### Option A: Describe What You Want
```bash
/generate-ai-system "customer support bot that helps users with technical issues, has a friendly personality, and can escalate to humans when needed"
```

### Option B: Let MADIO Decide Everything
```bash
/generate-ai-system "[describe your idea] - select appropriate MADIO templates based on complexity"
```

### Option C: Be More Specific
```bash
/generate-ai-system "[describe purpose] using character_voice_authority, content_operations, and methodology_framework templates"
```

**After generation, switch to Gemini CLI for refinement:**

```bash
# Use Gemini CLI for ongoing development
gemini "Review my generated MADIO documents and suggest improvements"
gemini "Add SEO optimization capabilities to my content writer AI"
gemini "Validate my MADIO project structure and check for any issues"
```

## 📥 Step 2B: Import Existing MADIO Documents (Alternative)

**Use this option if you already have MADIO-compliant documents:**

### Option A: Import from Current Directory
```bash
/madio-import-docs
```

### Option B: Import from Specific Location
```bash
/madio-import-docs --source ./my-docs
```

### Option C: Safe Import (Copy Instead of Move)
```bash
/madio-import-docs --copy --no-sync
```

**What the import command does:**
- ✅ **Analyzes** your documents to detect MADIO tier structure
- ✅ **Validates** document compliance and relationships
- ✅ **Generates** AI_CONTEXT.md from your existing content
- ✅ **Organizes** files into `synced_docs/` for Google Docs sync
- ✅ **Creates** folder structure and mapping configurations
- ✅ **Reports** analysis results and compliance scoring

**After import, continue with ongoing development:**
```bash
# Use Gemini CLI for refinement
gemini "Review my imported MADIO documents and suggest improvements"
gemini "Analyze the document structure and identify any gaps"
```

## 📝 Step 3: Review Your Files

Your project now contains MADIO documents (either generated or imported):

**Core Documents (Always Present):**
- `project_system_instructions.md` - Your AI's core identity (Tier 1)
- `orchestrator.md` - Workflow controller (Tier 2)

**Supporting Documents (Tier 3, varies by complexity):**
- `character_voice_authority.md` - Personality and voice guidelines
- `content_operations.md` - Content creation and validation
- `methodology_framework.md` - Analysis and evaluation processes
- Additional specialized documents based on your system's needs

## ✏️ Step 4: Set Up Google Docs Sync (Essential for AI Integration)

**Why sync to Google Docs?**
- Claude Projects can reference Google Docs directly in knowledge base
- Enables seamless handoff between local development and browser AI
- Automatic updates when you edit files locally

### 🚀 Essential Commands for First Success

```bash
# 1. Set up Google Docs sync (one-time setup)
/madio-enable-sync

# 2. Sync your documents to Google Docs  
/push-to-docs

# 3. Troubleshoot any issues
/madio-doctor
```

> 📖 **Complete Setup Guide**: For detailed step-by-step instructions, see [**SYNC_SETUP.md**](SYNC_SETUP.md)

### What happens during first sync:
- ✅ Google Cloud credentials setup
- ✅ Google Docs created for all your MADIO files
- ✅ Google Drive folder organization (interactive)
- ✅ File→doc ID mappings saved for future syncs
- ✅ Links displayed for easy access

## ✏️ Step 5: Customize Your Project

### 1. Replace Placeholders
Search for `[BRACKETED_TEXT]` in all generated files:
```bash
# Find all placeholders
grep -r "\[.*\]" *.md
```

Common placeholders:
- `[PROJECT_NAME]` - Your AI system's name
- `[TARGET_AUDIENCE]` - Who will use this
- `[DOMAIN]` - Your industry/field
- `[SPECIFIC_REQUIREMENTS]` - Your unique needs

### 2. Update .madio Configuration
Edit `.madio` file (see `docs/MADIO_CONFIGURATION.md` for complete documentation):
- Set your project name
- Confirm complexity level
- List your Tier 3 documents

### 3. Validate Document Hierarchy
Ensure:
- All referenced documents exist
- No circular dependencies
- Clear authority chain (Tier 1 → 2 → 3)

## 🚀 Step 6: Deploy Your AI

### For OpenAI CustomGPT:
1. Visit [chat.openai.com](https://chat.openai.com)
2. Click "Create a GPT"
3. Copy entire `project_system_instructions.md` → Instructions
4. Upload other `.md` files → Knowledge
5. Test thoroughly before publishing

### For Google Gemini Gem:
1. Visit [aistudio.google.com](https://aistudio.google.com)
2. Create new Gem
3. Combine documents per `.madio` configuration
4. Set model parameters as specified

### For Claude Project:
1. Visit [claude.ai](https://claude.ai)
2. Create new Project
3. Use `project_system_instructions.md` as instructions
4. Add other documents to project knowledge
   
   **💡 Pro Tip:** If you set up Google Docs sync, you can add the Google Docs URLs directly to Claude Project knowledge instead of uploading files manually.

## 🧪 Step 7: Test Your AI System

### Basic Testing Checklist:
- [ ] AI responds according to defined personality
- [ ] Workflow follows orchestrator steps
- [ ] Quality gates trigger appropriately
- [ ] Error handling works as expected
- [ ] All features function correctly

### Advanced Testing:
```bash
# Generate test scenarios
gemini "Create test cases for my MADIO AI system based on the generated documents"
```

## 🔧 Step 7: Iterate and Improve

### Making Changes:
1. **Update specific documents** - Modify individual components
2. **Regenerate sections** - Use Gemini CLI to revise parts
3. **Add new capabilities** - Include additional Tier 3 templates

### Getting Template Updates:
```bash
# Pull latest MADIO improvements
git pull template main
```

## 📂 Your Final Project Structure

```
your-ai-project/
├── _template_library/              # Keep for reference
├── AI_CONTEXT.md                   # Bridge file for AI collaboration
├── CLAUDE.md                       # Claude Code CLI context
├── GEMINI.md                       # Gemini CLI context
├── project_system_instructions.md  # Your core AI identity
├── orchestrator.md                 # Your workflow controller
├── character_voice_authority.md    # If personality defined
├── content_operations.md           # If content validation
├── [other generated documents]     # Based on your needs
├── .madio                          # Your configuration
├── madio_core_templates.md         # Template guide
├── README.md                       # Your project docs
└── your-project.code-workspace     # VS Code workspace
```

## 💡 Example Projects to Try

### Beginner: Simple Assistant
```bash
# Use Claude Code for setup
/generate-ai-system "helpful AI assistant that answers questions politely and accurately"
```

### Intermediate: Content Creator
```bash
# Use Claude Code for setup
/generate-ai-system "blog writing AI with SEO optimization, tone consistency, and topic research capabilities"
```

### Advanced: Analysis System
```bash
# Use Claude Code for setup
/generate-ai-system "business analysis AI with methodology framework, evaluation rubrics, and strategic recommendations"
```

## 🐛 Common Issues & Solutions

### "Claude Code commands not working"
```bash
# Ensure Claude Code is installed and working
# Try restarting VS Code if commands not recognized
/madio-onboard  # Should work if Claude Code is properly installed
```

### "Generated files seem incomplete"
```bash
# Use Gemini CLI for completion after initial setup
gemini "Complete the [document_name] using the MADIO framework"
gemini "Review my MADIO project and identify any missing components"
```

### "Not sure about document hierarchy"
```bash
# Use Gemini CLI for validation
gemini "Validate the document hierarchy in my MADIO project and identify any issues"
```

### "AI doesn't understand my project context"
```bash
# Update and copy bridge file
gemini "Update AI_CONTEXT.md with current project status"
# Then copy AI_CONTEXT.md contents to your browser-based AI
```

## 🎓 Learning Resources

- **Template Guide**: Read `madio_core_templates.md` for detailed template information
- **Selection Matrix**: See the matrix in `madio_core_templates.md` for choosing templates
- **Quality Checklists**: Each template has validation criteria at the bottom

## 🎉 Next Steps

After completing this guide:

1. **Delete this file** - You don't need it anymore!
   ```bash
   rm GETTING-STARTED.md
   ```

2. **Update README.md** - Add your project-specific documentation

3. **Start building** - Your AI system is ready for production!

## 🚨 Final Reminders

- **Always test** before deploying to production
- **Keep templates** in `_template_library/` for reference
- **Maintain AI_CONTEXT.md** for seamless AI collaboration
- **Use git** for version control and updates
- **Document changes** in your commit messages

---

**Congratulations!** You've successfully created a production-ready AI system using MADIO. 

Remember: The framework handles the complexity so you can focus on your unique value proposition.

**Now go build something amazing!** 🚀