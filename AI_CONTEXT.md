# MADIO Framework - AI Context Bridge

**Generated**: July 8, 2025  
**Purpose**: Context bridge between local CLI tools and browser-based AI systems  
**Status**: Template repository with Google Docs sync capability

## Current Project Status

**MADIO Framework**: Production-ready template repository for AI system development  
**Latest Addition**: Google Docs synchronization system for seamless local-to-cloud workflows  
**Template Library**: 14 production templates covering content, analysis, and implementation use cases

## Major Capabilities

### **Core MADIO System**
- **Hierarchical Architecture**: Tier 1 (Authority) → Tier 2 (Orchestrator) → Tier 3 (Specialist templates)
- **Template-Driven Development**: Systematic approach using 14 validated templates
- **Multi-Platform Deployment**: OpenAI CustomGPT, Google Gemini Gem, Claude Project compatibility
- **Professional Workflow**: VS Code + CLI integration with Git-based template inheritance

### **Google Docs Sync (NEW)**
- **Local Development**: Claude Desktop + MCP filesystem for direct file editing
- **Cloud Integration**: Python-based sync to Google Docs for Claude Project knowledge
- **Command Interface**: `/push-to-docs` for seamless synchronization
- **OAuth2 Security**: Google Cloud project with proper authentication

### **Multi-AI Collaboration**
- **Claude Code**: Initial project setup and MADIO document generation
- **Gemini CLI**: Ongoing development, refinement, and iteration
- **AI Companions**: Browser-based strategic AI for analysis and planning

## Key Architectural Decisions

### **Template Hierarchy**
1. **Tier 1**: `project_system_instructions.md` - Supreme authority, core AI identity
2. **Tier 2**: `orchestrator.md` - Workflow control and step-by-step methodology
3. **Tier 3**: Specialist templates for specific capabilities (content, analysis, implementation)

### **File Organization**
```
madio-start/
├── _template_library/           # 14 production templates
├── .claude/                     # Claude Code commands and scripts
│   ├── commands/               # /madio-setup, /generate-ai-system, /push-to-docs
│   └── scripts/                # Google Docs sync system
├── setup-ai-companion/        # Multi-platform AI setup guides
├── docs/                       # Documentation including Google Cloud setup
└── sync_config.json            # Document mapping configuration
```

### **Security Architecture**
- **Local Credentials**: OAuth2 credentials in `.claude/scripts/credentials.json`
- **Token Management**: Automatic refresh with local caching
- **Access Control**: Principle of least privilege - Google Docs API only
- **Version Control**: Sensitive files excluded from Git

## Recent Development History

### **Google Docs Sync Implementation**
- **Challenge**: Bridge local development (Claude write access) with cloud knowledge (Claude Project)
- **Solution**: Python sync script with OAuth2 authentication and full document replacement
- **Files Added**: 
  - `sync_to_docs.py` - Main synchronization engine
  - `push-to-docs.md` - Claude command documentation
  - `setup.sh` - Automated dependency installation
  - `GOOGLE_CLOUD_SETUP.md` - Complete configuration guide

### **Integration Points**
- **MCP Filesystem**: Claude Desktop can edit local markdown files directly
- **Google Cloud**: OAuth2 project "markdown-to-docs" (testing mode)
- **Document Mapping**: `sync_config.json` maps local files to Google Doc IDs
- **Claude Project**: Google Docs automatically refresh project knowledge

## Workflow Patterns

### **MADIO Development Cycle**
1. **Setup**: `/madio-setup` initializes project structure
2. **Generation**: `/generate-ai-system` creates hierarchical documents
3. **Development**: Gemini CLI for refinement and iteration
4. **Sync**: `/push-to-docs` synchronizes to Google Docs
5. **Deployment**: Claude Project automatically updates knowledge

### **Framework Evolution**
- **Local Innovation**: Claude can directly edit templates and documents
- **Quality Validation**: Built-in validation ensures system integrity
- **Cloud Propagation**: Changes sync to Google Docs for immediate availability
- **Community Distribution**: Template updates flow through Git inheritance

## Technical Specifications

### **Dependencies**
- **Python Packages**: google-api-python-client, google-auth, google-auth-oauthlib
- **CLI Tools**: Claude Code, Gemini CLI (optional), Git
- **Cloud Services**: Google Cloud project with Docs API enabled
- **Local Tools**: VS Code, MCP filesystem server

### **Authentication Flow**
1. **Initial Setup**: User downloads OAuth2 credentials from Google Cloud Console
2. **First Run**: Browser-based consent flow creates local token cache
3. **Subsequent Use**: Automatic token refresh with cached credentials
4. **Security**: Full document replacement strategy eliminates complex sync issues

## Strategic Context

### **Market Position**
- **Problem Solved**: Git barrier prevents business users from leveraging AI development frameworks
- **Unique Solution**: Local development with Claude write access + automatic cloud knowledge sync
- **Target Users**: Technical users (current) + business professionals (enabled by Google Docs sync)

### **Competitive Advantages**
- **No-Code Sync**: Business users can evolve AI systems without technical workflows
- **Framework Evolution**: Continuous improvement through direct Claude editing
- **Multi-Platform**: Works across OpenAI, Google, and Anthropic ecosystems
- **Professional Quality**: Enterprise-grade architecture with proper security

## Future Roadmap

### **Immediate Priorities**
- **User Testing**: Validate Google Docs sync with diverse user scenarios
- **Documentation**: Complete setup guides and troubleshooting resources
- **Template Expansion**: Additional Tier 3 templates based on user feedback

### **Strategic Expansion**
- **Production OAuth**: Move from testing to verified Google app for public access
- **Community Templates**: Enable user-contributed template ecosystem
- **Platform Integration**: Direct integration with AI platform knowledge bases
- **Enterprise Features**: Team collaboration and template governance

## Integration Instructions

### **For Claude Code / VS Code**
- Reference this context when working on MADIO projects
- Use `/push-to-docs` after making local file changes
- Leverage template hierarchy for systematic development
- Follow OAuth setup guide in `docs/GOOGLE_CLOUD_SETUP.md`

### **For Browser-Based AI**
- Copy this context to maintain project continuity
- Reference Google Docs sync capability for strategic planning
- Understand template library structure for recommendation accuracy
- Consider multi-platform deployment requirements

### **For Gemini CLI**
- Use for ongoing refinement and content development
- Integrate with Google Docs sync workflow for seamless iteration
- Reference template selection matrix for appropriate complexity matching
- Update this AI_CONTEXT.md with significant changes

---

**Key Insight**: MADIO's Google Docs sync capability represents a breakthrough in AI development accessibility, enabling non-technical users to leverage sophisticated AI frameworks while maintaining professional development workflows for technical users.
