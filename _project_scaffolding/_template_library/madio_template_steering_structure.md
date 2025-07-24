# Project Structure Steering Guide

**File:** `structure.md`
**Integration Mode:** `always`
**Purpose:** Provide persistent knowledge about file organization, naming conventions, and architectural patterns
**Created:** [DATE]
**Last Modified:** [DATE]

---

## PROJECT ORGANIZATION

### **Root Directory Structure**
```
[PROJECT_NAME]/
├── .claude/                    # Claude Code CLI integration
│   ├── commands/               # Available slash commands
│   ├── steering/              # Agent steering files (this directory)
│   ├── scripts/               # Automation scripts
│   └── settings.local.json    # Claude Code settings
├── _project_scaffolding/      # Template system (removed after setup)
│   ├── _template_library/     # MADIO templates
│   ├── CLAUDE.md             # Claude Code context
│   └── GEMINI.md             # Gemini CLI context
├── docs/                      # Project documentation
├── synced_docs/              # Google Docs sync directory (optional)
├── setup-ai-companion/       # AI companion setup guides
├── AI_CONTEXT.md             # Bridge file for AI collaboration
├── CLAUDE.md                 # Claude Code CLI context
├── GEMINI.md                 # Gemini CLI context
├── .madio                    # Project configuration
├── madio_core_templates.md   # Template selection guide
├── [project].code-workspace  # VS Code workspace
└── [Generated AI system documents]
    ├── project_system_instructions.md  # Tier 1
    ├── orchestrator.md                 # Tier 2
    ├── requirements.md                 # Tier 2
    ├── design.md                      # Tier 2
    ├── tasks.md                       # Tier 2
    └── [Additional Tier 3 documents]
```

### **MADIO Document Hierarchy**
**Authority Levels:**
- **Tier 1:** Supreme authority - `project_system_instructions.md`
- **Tier 2:** Execution control - `orchestrator.md`, `requirements.md`, `design.md`, `tasks.md`
- **Tier 3:** Supporting documents - Character, content, methodology, etc.

**Hierarchy Rules:**
1. Higher tiers have authority over lower tiers
2. Conflicts are resolved by consulting higher-tier documents
3. All documents must maintain consistency with Tier 1
4. Cross-references must respect the hierarchy

---

## NAMING CONVENTIONS

### **File Naming Standards**
**MADIO AI System Documents:**
- Format: `[document_type].md`
- Examples: `project_system_instructions.md`, `orchestrator.md`, `requirements.md`
- Case: Lowercase with underscores
- Extensions: Always `.md` for MADIO documents

**Template Files:**
- Format: `madio_template_tier[X]_[document_type].md`
- Examples: `madio_template_tier1_project_system_instructions.md`
- Location: `_project_scaffolding/_template_library/`

**Steering Files:**
- Format: `[category].md`
- Examples: `product.md`, `tech.md`, `structure.md`
- Location: `.claude/steering/`

### **Directory Naming Standards**
**Standard Directories:**
- `.claude/` - Claude Code integration files
- `docs/` - Project documentation
- `synced_docs/` - Google Docs sync files (optional)
- `setup-ai-companion/` - AI companion guides

**Custom Directories:**
- Use lowercase with hyphens: `my-custom-feature/`
- Avoid spaces and special characters
- Keep directory names descriptive but concise

### **Variable and Placeholder Naming**
**Template Placeholders:**
- Format: `[PLACEHOLDER_NAME]`
- Case: UPPERCASE with underscores
- Examples: `[PROJECT_NAME]`, `[TARGET_AUDIENCE]`, `[DATE]`

**Configuration Variables:**
- Format: `VARIABLE_NAME`
- Case: UPPERCASE with underscores
- Examples: `AI_SYSTEM_DESC`, `COMPLEXITY_LEVEL`

---

## ARCHITECTURAL PATTERNS

### **MADIO Framework Patterns**
**Document Authority Pattern:**
```
Tier 1 (Authority)
    ↓ controls
Tier 2 (Orchestration)
    ↓ references
Tier 3 (Support)
```

**Cross-Reference Pattern:**
- Higher tiers reference lower tiers for detailed implementation
- Lower tiers acknowledge authority of higher tiers
- Circular references are prohibited
- All references must be explicit and documented

### **Command Structure Pattern**
**Claude Code Commands:**
- Location: `.claude/commands/[command-name].md`
- Format: Markdown files with executable bash sections
- Naming: Kebab-case with descriptive names
- Examples: `generate-ai-system.md`, `madio-setup.md`

**Command Integration:**
- Commands should reference steering files for context
- Commands should update AI_CONTEXT.md bridge file
- Commands should maintain MADIO document hierarchy

### **Configuration Pattern**
**Centralized Configuration:**
- Main config: `.madio` file in project root
- Local overrides: `.claude/settings.local.json`
- Environment-specific: Environment variables

**Configuration Hierarchy:**
1. Environment variables (highest priority)
2. Local settings file
3. Project configuration file
4. Default values (lowest priority)

---

## CODE ORGANIZATION

### **Script Organization**
**Shell Scripts:**
- Location: `.claude/scripts/`
- Naming: `[purpose].sh`
- Permissions: Executable (`chmod +x`)
- Documentation: Header comments with purpose and usage

**Python Scripts:**
- Location: `.claude/scripts/`
- Naming: `[purpose].py`
- Dependencies: Listed in `requirements.txt`
- Virtual Environment: `.claude/scripts/venv/`

### **Documentation Organization**
**Core Documentation:**
- `README.md` - Project overview and quick start
- `AI_CONTEXT.md` - Bridge file for AI collaboration
- `CLAUDE.md` / `GEMINI.md` - AI-specific context files

**Extended Documentation:**
- `docs/` directory for detailed documentation
- `setup-ai-companion/` for deployment guides
- Inline documentation in AI system documents

### **Asset Organization**
**Static Assets:**
- Images: `docs/images/` or `assets/images/`
- Templates: `_project_scaffolding/_template_library/`
- Backups: `backups/` (gitignored)

**Generated Assets:**
- AI system documents: Project root
- Sync files: `synced_docs/` (if using Google Docs sync)
- Build artifacts: `build/` or `dist/` (gitignored)

---

## DEVELOPMENT WORKFLOW

### **File Lifecycle**
**Template to Production:**
1. **Template Creation** - In `_template_library/`
2. **Template Selection** - Via `/generate-ai-system`
3. **Document Generation** - Copy to project root
4. **Customization** - Replace placeholders with project-specific content
5. **Validation** - Ensure hierarchy and cross-references
6. **Deployment** - Upload to target AI platform

### **Update Workflow**
**Document Updates:**
1. **Change Identification** - What needs to be updated?
2. **Impact Analysis** - Which documents are affected?
3. **Hierarchy Validation** - Maintain authority structure
4. **Cross-Reference Updates** - Update related documents
5. **Validation Testing** - Ensure system integrity

### **Version Control**
**Git Practices:**
- **Branching:** Feature branches for major changes
- **Commits:** Atomic commits with descriptive messages
- **Tags:** Version tags for releases
- **Ignores:** `.gitignore` for generated and sensitive files

**File Tracking:**
- **Track:** AI system documents, templates, configuration
- **Ignore:** Build artifacts, temporary files, credentials
- **Optional:** `synced_docs/` (depends on team preference)

---

## INTEGRATION PATTERNS

### **AI Platform Integration**
**OpenAI CustomGPT Pattern:**
```
project_system_instructions.md (Instructions)
    +
Supporting Documents (Knowledge Base)
    =
Deployed CustomGPT
```

**Google Gemini Gem Pattern:**
```
Combined Document (All instructions merged)
    =
Deployed Gem
```

**Claude Project Pattern:**
```
project_system_instructions.md (Project Instructions)
    +
All Documents (Project Knowledge)
    +
AI_CONTEXT.md (Bridge Context)
    =
Deployed Claude Project
```

### **Sync Integration Patterns**
**Google Docs Sync Pattern:**
```
Local Files (synced_docs/)
    ↔ sync_to_docs.py
    ↔ Google Docs API
    ↔ Google Drive Storage
```

**Configuration Management:**
```
sync_config.json (File mappings)
    +
credentials.json (API access)
    +
Document IDs (Persistent mapping)
    =
Automated Sync
```

---

## QUALITY ASSURANCE

### **File Validation Rules**
**MADIO Document Validation:**
- All placeholders replaced with actual content
- Proper markdown formatting and structure
- Valid cross-references to other documents
- Compliance with tier authority rules

**Template Validation:**
- All required placeholders present
- Proper tier classification
- Complete documentation sections
- Valid example content

### **Structure Validation**
**Directory Structure:**
- Required directories exist
- Naming conventions followed
- Proper file permissions set
- No unauthorized files in restricted directories

**Hierarchy Validation:**
- Tier 1 document exists and is complete
- All Tier 2 documents reference Tier 1
- Tier 3 documents properly reference higher tiers
- No circular references in document hierarchy

### **Integration Validation**
**Command Integration:**
- All commands reference appropriate steering files
- Commands update AI_CONTEXT.md correctly
- Command outputs follow naming conventions
- Error handling follows established patterns

**Platform Integration:**
- Documents formatted correctly for target platforms
- File sizes within platform limits
- Context length within platform constraints
- All required metadata present

---

## MAINTENANCE PROCEDURES

### **Regular Maintenance Tasks**
**Weekly:**
- Validate all cross-references in AI system documents
- Check for placeholder completion
- Verify file organization compliance

**Monthly:**
- Review and update steering files
- Validate template library completeness
- Check integration configurations

**Quarterly:**
- Complete structure review and optimization
- Update naming conventions if needed
- Review and update architectural patterns

### **Structure Evolution**
**Adding New Components:**
1. **Assess Impact** - How does this affect existing structure?
2. **Plan Integration** - Where does this fit in the hierarchy?
3. **Update Documentation** - Modify this steering file
4. **Validate Changes** - Ensure compliance with patterns
5. **Communicate Changes** - Update team and AI agents

### **Refactoring Guidelines**
**When to Refactor:**
- Structure becomes difficult to navigate
- Naming conventions become inconsistent
- File organization doesn't match current needs
- Integration patterns become overly complex

**Refactoring Process:**
1. **Document Current State** - Understand existing structure
2. **Plan New Structure** - Design improved organization
3. **Migration Strategy** - Plan transition steps
4. **Execute Migration** - Implement changes incrementally
5. **Validate Results** - Ensure nothing is broken
6. **Update Documentation** - Reflect new structure

---

## TROUBLESHOOTING

### **Common Structure Issues**
**File Not Found Errors:**
- Check file naming conventions
- Verify directory structure
- Ensure proper case sensitivity
- Validate file permissions

**Cross-Reference Failures:**
- Check document hierarchy compliance
- Verify all referenced files exist
- Ensure proper relative path usage
- Validate markdown link syntax

**Integration Problems:**
- Verify steering file locations
- Check configuration file syntax
- Ensure proper file encoding (UTF-8)
- Validate template placeholder replacement

### **Diagnostic Procedures**
**Structure Validation:**
```bash
# Check directory structure
find . -type d -name ".*" | head -10

# Validate file naming
find . -name "*.md" | grep -v node_modules

# Check for placeholders
grep -r "\[.*\]" *.md
```

**Cross-Reference Validation:**
```bash
# Find broken markdown links
grep -r "\]\(" *.md | grep -v "http"

# Check tier compliance
grep -r "Tier [123]" *.md
```

---

## CHANGE MANAGEMENT

### **Structure Change Process**
**Change Categories:**
- **Minor Changes:** File naming, directory organization
- **Major Changes:** Hierarchy modifications, new patterns
- **Breaking Changes:** Fundamental structure overhaul

**Approval Process:**
1. **Proposal** - Document proposed changes
2. **Impact Assessment** - Analyze effects on existing structure
3. **Review** - Team and stakeholder review
4. **Implementation** - Execute changes with validation
5. **Documentation** - Update this steering file

### **Communication Protocol**
**Change Notifications:**
- Update this steering file with change details
- Communicate to AI agents via context updates
- Notify team members of structural changes
- Update integration documentation as needed

**Training Requirements:**
- New team members: Complete structure overview
- Existing team: Updates on structural changes
- AI agents: Context updates via steering files
- Stakeholders: High-level structure changes only