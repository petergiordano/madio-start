# MADIO Configuration File (.madio)

## **📋 Overview**

The `.madio` file is the **central configuration file** for MADIO projects. It stores project metadata, framework settings, and deployment preferences to ensure consistent and systematic AI system development.

## **🎯 Purpose**

The `.madio` configuration file serves multiple critical functions:

### **Project Identity & Tracking**
- Stores project name, type, and complexity level
- Maintains creation and modification timestamps
- Tracks development history and current phase

### **Framework Configuration**
- Defines template library location and version
- References core documentation files
- Manages framework compatibility settings

### **AI Provider Integration**
- Configures default AI provider (Gemini CLI, Claude Code)
- Sets model parameters and generation preferences
- Defines system prompt mode and interaction patterns

### **Document Management**
- Lists mandatory documents (always required)
- Tracks Tier 3 templates currently in use
- Manages custom template additions and modifications

### **Quality & Validation**
- Enforces hierarchical document structure
- Enables cross-reference validation
- Requires placeholder replacement verification
- Sets quality gate enforcement levels

### **Deployment Settings**
- Specifies target deployment platforms
- Configures export format preferences
- Manages metadata inclusion settings

## **📂 File Structure**

```json
{
  "version": "1.0.0",
  "project": {
    "name": "[PROJECT_NAME]",           // Set during /madio-setup
    "type": "[PROJECT_TYPE]",           // e.g., "AI Assistant", "Analysis System"
    "complexity": "simple|moderate|complex|enterprise",
    "created": "[TIMESTAMP]",           // Auto-set during initialization
    "lastModified": "[TIMESTAMP]"      // Updated during development
  },
  "framework": {
    "version": "1.0.0",                 // MADIO framework version
    "templateLibrary": "_template_library",
    "coreTemplatesDoc": "madio_core_templates.md"
  },
  "ai": {
    "provider": "gemini",               // Default CLI tool
    "model": "gemini-2.0-flash-exp",   // Default model
    "temperature": 0.7,                // Generation parameters
    "maxTokens": 8192,
    "systemPromptMode": "hierarchical" // MADIO-specific mode
  },
  "documents": {
    "mandatory": [                      // Always required
      "project_system_instructions.md",
      "orchestrator.md"
    ],
    "tier3": [],                       // Updated during generation
    "customTemplates": []              // User-added templates
  },
  "generation": {
    "autoValidate": true,              // Enable quality checks
    "preservePlaceholders": false,     // Replace [BRACKETED_TEXT]
    "generateComments": true,          // Include helpful comments
    "outputFormat": "markdown"
  },
  "validation": {
    "enforceHierarchy": true,          // Require Tier 1→2→3 structure
    "checkCrossReferences": true,      // Validate document links
    "validatePlaceholders": true,      // Ensure replacement
    "requireSuccessMetrics": true      // Include quality metrics
  },
  "deployment": {
    "targets": [                       // Supported platforms
      "openai-customgpt", 
      "gemini-gem", 
      "claude-project"
    ],
    "exportFormat": "unified|platform-specific",
    "includeMetadata": true
  }
}
```

## **🔧 Usage During Development**

### **During `/madio-setup` (Initialization)**
```bash
# The setup command automatically:
# 1. Replaces [PROJECT_NAME] with directory name
# 2. Sets creation timestamp
# 3. Initializes document tracking arrays
# 4. Configures default settings
```

### **During System Generation**
```bash
# CLI tools reference .madio to:
# 1. Determine template library location
# 2. Apply generation preferences
# 3. Update tier3 array with selected templates
# 4. Enforce validation rules
```

### **During Deployment**
```bash
# Deployment processes use .madio to:
# 1. Identify target platforms
# 2. Determine export format strategy
# 3. Include appropriate metadata
# 4. Validate deployment readiness
```

## **📝 Manual Configuration**

### **Common Customizations**

**Project Information:**
```json
"project": {
  "name": "Customer Support AI",      // Descriptive name
  "type": "Support System",          // System category
  "complexity": "moderate"           // Complexity level
}
```

**AI Provider Preferences:**
```json
"ai": {
  "provider": "gemini",              // "gemini" or "claude"
  "model": "gemini-2.0-flash-exp",   // Preferred model
  "temperature": 0.3                 // Lower for consistency
}
```

**Platform Targeting:**
```json
"deployment": {
  "targets": ["claude-project"],     // Focus on specific platform
  "exportFormat": "platform-specific",
  "includeMetadata": true
}
```

## **🎯 Integration Points**

### **CLI Tools Integration**
- **Gemini CLI:** Reads template library path and generation settings
- **Claude Code:** Uses validation settings and document tracking
- **Both:** Reference deployment targets for platform optimization

### **AI Companion Integration**
- **Template Selection:** Uses complexity level for recommendations
- **Quality Assurance:** References validation settings
- **Deployment Guidance:** Uses target platforms for specific instructions

### **Framework Evolution**
- **Template Updates:** Version tracking enables compatibility checks
- **Feature Additions:** Custom commands section allows extensions
- **Quality Improvements:** Validation settings enable framework-wide improvements

## **🔍 Troubleshooting**

### **Common Issues**

**Missing or Corrupted .madio:**
```bash
# Regenerate during setup
/madio-setup
```

**Incorrect Template Paths:**
```json
// Check these settings
"framework": {
  "templateLibrary": "_template_library",  // Must match actual directory
  "coreTemplatesDoc": "madio_core_templates.md"
}
```

**Validation Failures:**
```json
// Adjust validation settings if needed
"validation": {
  "enforceHierarchy": true,     // Set to false if testing
  "checkCrossReferences": false // Disable for development
}
```

## **📈 Best Practices**

### **Version Control**
- **Commit .madio file** with your project
- **Update lastModified** when making significant changes
- **Track complexity evolution** as system grows

### **Team Development**
- **Standardize AI provider** settings across team
- **Align deployment targets** with project requirements
- **Sync validation settings** for consistent quality

### **Framework Updates**
- **Check version compatibility** when updating templates
- **Review new configuration options** in framework updates
- **Test changes** before deploying to production

## **🚀 Advanced Configuration**

### **Custom Commands** (Future Enhancement)
```json
"customCommands": {
  "validate": "madio validate --all",
  "export": "madio export --target {platform}",
  "test": "madio test --coverage"
}
```

### **Feature Flags** (Extensible)
```json
"features": {
  "autoSave": true,
  "versionControl": true,
  "templateSync": true,
  "liveValidation": true
}
```

---

**The `.madio` file is the control center of your MADIO project - it coordinates all tools, maintains quality standards, and ensures systematic development from initialization through deployment.**
