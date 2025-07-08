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
- [ ] You have Gemini CLI installed

## 🏗️ Step 1: Initialize Your MADIO Project

**Run this command in your VS Code terminal:**

```bash
gemini "/madio-setup"
```

This command will:
- ✅ Validate you're in the right directory
- ✅ Configure template inheritance
- ✅ Set up your project structure
- ✅ Generate your AI_CONTEXT.md bridge file
- ✅ Update configuration files
- ✅ Prepare for AI system generation

## 🤖 Step 2: Generate Your AI System

### Option A: Describe What You Want
```bash
gemini "Using MADIO templates, create a customer support bot that helps users with technical issues, has a friendly personality, and can escalate to humans when needed"
```

### Option B: Let MADIO Decide Everything
```bash
gemini "I want to create [describe your idea]. Use the MADIO framework to build this. Determine which templates are needed based on my requirements."
```

### Option C: Specify Exact Templates
```bash
gemini "Create a MADIO project using: project_system_instructions, orchestrator, character_voice_authority, and content_operations templates. This is for a [describe purpose]"
```

## 📝 Step 3: Review Generated Files

Gemini will create several `.md` files in your project:

**Always Generated:**
- `project_system_instructions.md` - Your AI's core identity
- `orchestrator.md` - Workflow controller

**Commonly Added:**
- `character_voice_authority.md` - If personality specified
- `content_operations.md` - If content validation needed
- Additional Tier 3 documents based on complexity

## ✏️ Step 4: Customize Your Project

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

## 🚀 Step 5: Deploy Your AI

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

## 🧪 Step 6: Test Your AI System

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
2. **Regenerate sections** - Use Gemini to revise parts
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
gemini "Create a helpful AI assistant using MADIO that answers questions politely and accurately"
```

### Intermediate: Content Creator
```bash
gemini "Create a blog writing AI using MADIO with SEO optimization, tone consistency, and topic research capabilities"
```

### Advanced: Analysis System
```bash
gemini "Create a business analysis AI using MADIO with methodology framework, evaluation rubrics, and strategic recommendations"
```

## 🐛 Common Issues & Solutions

### "Gemini doesn't understand MADIO"
```bash
# Be explicit about templates
gemini "Use the MADIO templates in _template_library/ to create..."
```

### "Generated files seem incomplete"
```bash
# Request completion
gemini "Complete the [document_name] using the appropriate MADIO template from _template_library/"
```

### "Not sure about document hierarchy"
```bash
# Ask for validation
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
   rm _GETTING-STARTED.md
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