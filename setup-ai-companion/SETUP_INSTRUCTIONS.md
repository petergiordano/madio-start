# AI Companion Setup Instructions

## Creating Your MADIO AI Companion

Your MADIO AI Companion works alongside your local CLI tools (Gemini CLI + Claude Code) to provide strategic guidance, context management, and deployment support for your AI systems built with MADIO framework.

## Platform Options

Choose your preferred AI platform for your companion:

### **🎯 Claude Project (Recommended)**
- **Best for:** Strategic analysis, AI system document review, deployment guidance
- **Strengths:** Excellent at understanding MADIO framework and AI system document hierarchy
- **Setup:** Most comprehensive with full project knowledge integration

### **🎯 Google Gemini Gem**  
- **Best for:** AI system document template selection, system generation guidance
- **Strengths:** Native integration with Gemini CLI workflow for AI system documents
- **Setup:** Streamlined for Gemini CLI users

### **🎯 ChatGPT Custom GPT**
- **Best for:** Interactive AI system design, requirement analysis
- **Strengths:** Conversational interface for planning and ideation
- **Setup:** Simple knowledge base upload approach

---

## Setup Instructions by Platform

### **1. Claude Project Setup**

**Create New Claude Project:**
1. Go to [claude.ai](https://claude.ai)
2. Click "Create Project"
3. Name: "MADIO AI System Development"
4. Description: "MADIO framework companion for AI system creation and deployment"

**Project Instructions:**
- Copy the entire contents of `CLAUDE_PROJECT_INSTRUCTIONS.md` and paste as Project Instructions

**Project Knowledge:**
- Upload `../AI_CONTEXT.md` - Your project bridge file (auto-generated after /madio-setup)
- Upload `../madio_core_templates.md` - Template selection guide
- Upload `../CLAUDE.md` - Claude Code workflow context
- Upload `../GEMINI.md` - Gemini CLI workflow context
- **Optional:** Connect your GitHub repository for live project access

**Testing Your Setup:**
```
Test Message: "Working on my MADIO project for [your AI system description]"

Expected Response:
- Loads context from AI_CONTEXT.md
- Shows MADIO framework awareness
- Offers template selection guidance
- Provides deployment recommendations
```

### **2. Google Gemini Gem Setup**

**Create New Gem:**
1. Go to [aistudio.google.com](https://aistudio.google.com)
2. Create new Gem
3. Name: "MADIO Framework Assistant"
4. Description: "AI companion for MADIO system development"

**Gem Instructions:**
- Copy the contents of `GEMINI_GEM_INSTRUCTIONS.md` 
- Combine with your project's `AI_CONTEXT.md` content

**Knowledge Integration:**
- Include `madio_core_templates.md` content in instructions
- Reference your specific template selections and rationale
- Add project-specific context from AI_CONTEXT.md

**Testing Your Setup:**
```
Test Prompt: "Help me expand my MADIO system with additional templates"

Expected Response:
- References your current template selection
- Suggests complementary templates
- Provides specific Gemini CLI commands
```

### **3. ChatGPT Custom GPT Setup**

**Create Custom GPT:**
1. Go to [chat.openai.com](https://chat.openai.com)
2. Click "Create a GPT"
3. Name: "MADIO System Builder"
4. Description: "Assistant for creating AI systems using MADIO framework"

**Instructions:**
- Copy the contents of `CHATGPT_INSTRUCTIONS.md`
- Customize with your project specifics

**Knowledge Base:**
- Upload `../madio_core_templates.md`
- Upload your project's `AI_CONTEXT.md` 
- Upload generated MADIO documents from your project

**Testing Your Setup:**
```
Test Message: "Review my MADIO system architecture and suggest improvements"

Expected Response:
- Analyzes your current document hierarchy
- Identifies potential gaps or improvements
- Suggests deployment optimizations
```

---

## **🔄 Workflow Integration**

### **Local Development (CLI)**
```
Your VS Code Environment:
├── Gemini CLI → MADIO system generation
├── Claude Code → Document refinement (/madio-setup, /orient)
└── AI_CONTEXT.md → Bridge file maintenance
```

### **Strategic Planning (Browser AI)**
```
Your AI Companion:
├── Template selection guidance
├── System architecture review  
├── Deployment planning
├── Quality assurance
└── Context evolution recommendations
```

### **Seamless Handoff Process**
1. **Start in browser AI:** Plan system architecture and select templates
2. **Move to CLI:** Execute generation using Gemini CLI or Claude Code commands
3. **Return to browser AI:** Review results, plan refinements, prepare deployment
4. **Update AI_CONTEXT.md:** Maintain context continuity across sessions

---

## **📋 Context Transfer Protocol**

### **From Local to Browser AI**
When starting a new browser AI session:

```
Copy this from your AI_CONTEXT.md:

=== PROJECT CONTEXT ===
[Paste current AI_CONTEXT.md content]
=== END CONTEXT ===

Then say: "Working on my MADIO project. Please load the above context and help me with [specific task]."
```

### **From Browser AI to Local**
When your AI companion recommends CLI actions:

```
Typical recommendations:
- gemini "Add methodology_framework template to my MADIO system for evaluation capabilities"
- /generate-ai-system "customer support bot with escalation and analytics"
- gemini "Update AI_CONTEXT.md with template selection rationale"
```

---

## **🎯 Common Use Cases**

### **System Planning Session**
```
Browser AI: "I want to create a content generation AI. What MADIO templates should I use?"
Response: Template recommendations with complexity assessment
CLI Action: Execute generation with selected templates
```

### **Quality Review Session**
```
Browser AI: "Review my generated MADIO documents for deployment readiness"  
Response: Document hierarchy analysis, placeholder check, deployment preparation
CLI Action: Refinements and final deployment preparation
```

### **Expansion Planning Session**
```
Browser AI: "My system works well but needs evaluation capabilities. How should I expand it?"
Response: Template addition strategy, integration planning
CLI Action: Add specific templates and update system
```

### **Deployment Guidance Session**
```
Browser AI: "Help me deploy my MADIO system to Claude Project"
Response: Platform-specific deployment instructions, optimization tips
CLI Action: Final document preparation and platform deployment
```

---

## **🔧 Maintenance & Updates**

### **Keeping Your Companion Current**
- **Update AI_CONTEXT.md:** After each development session
- **Sync template knowledge:** When MADIO framework updates arrive
- **Refresh deployment knowledge:** When platform requirements change
- **Context evolution:** As your system grows in complexity

### **Getting MADIO Framework Updates**
```bash
# In your project directory
git pull template main

# Update your AI companion with new:
# - Template descriptions (madio_core_templates.md)
# - Framework capabilities
# - Best practices and patterns
```

### **Context Optimization**
As your MADIO project evolves:
- Archive completed development phases in AI_CONTEXT.md
- Focus companion knowledge on active development areas
- Update template selection rationale based on experience
- Refine deployment workflows based on platform feedback

---

## **🎉 Benefits of AI Companion Integration**

### **Strategic Planning**
- **Template Intelligence:** Smart recommendations based on system requirements
- **Architecture Guidance:** Ensure document hierarchy integrity
- **Complexity Assessment:** Right-size your MADIO system for requirements

### **Development Efficiency**  
- **Context Continuity:** Seamless handoff between planning and implementation
- **Quality Assurance:** Built-in review and validation before deployment
- **Error Prevention:** Catch issues before CLI implementation

### **Deployment Success**
- **Platform Optimization:** Specific guidance for OpenAI, Google, Anthropic
- **Quality Validation:** Ensure deployment readiness
- **Performance Monitoring:** Post-deployment optimization recommendations

### **Learning Acceleration**
- **Framework Mastery:** Understand MADIO patterns and best practices
- **Template Expertise:** Learn when and how to use each template
- **System Evolution:** Grow your AI systems systematically over time

---

Ready to set up your AI companion? Choose your platform and follow the corresponding instructions!
