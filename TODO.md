# To Do.md

- [x] create instructions for the user to set up their companion AI Chat Assistant (Claude or Gemini or ChatGPT), e.g. /Users/petergiordano/Documents/GitHub/ai-new-project-template/setup-claude-chat-ai
- [ ] **Google Cloud OAuth App Production Setup** - Currently in testing mode, limiting to test users only
  - [ ] Review and complete OAuth consent screen for production
  - [ ] Add privacy policy and terms of service if required
  - [ ] Submit app for verification if needed for public use
  - [ ] Add additional users to test user list as needed
  - [ ] Consider publishing app for broader MADIO community access
  - **Context**: Google Docs sync currently requires users to be added as test users. For wider MADIO adoption, may need production OAuth approval.

## Refactor new project setup

### 1. **Automated Setup Script Enhancement**
- [ ] Create automated first-run detection in `/madio-setup`
- [ ] Add workspace file auto-creation if not exists
- [ ] Implement automatic Python dependency installation check
- [ ] Add Google Docs sync optional setup prompt
- [ ] Create post-setup validation and health check

### 2. **Quick Start Improvements**
- [ ] Move _GETTING-STARTED.md to prominent location after setup
- [ ] Create interactive setup wizard for first-time users
- [ ] Add VS Code recommended extensions prompt
- [ ] Implement automatic git remote validation and fix
- [ ] Generate project-specific README template

### 3. **Google Docs Sync Simplification**
- [ ] Make Google Docs sync opt-in during initial setup
- [ ] Create simplified OAuth setup with better error messages
- [ ] Add skip option for users who don't need cloud sync
- [ ] Provide test credentials for demo purposes (if possible)
- [ ] Auto-detect if credentials exist and skip setup

### 4. **Error Prevention & Recovery**
- [ ] Add pre-flight checks before any operations
- [ ] Implement rollback capability for failed setups
- [ ] Create diagnostic command for troubleshooting
- [ ] Add clear error messages with solution steps
- [ ] Implement setup state recovery

### 5. **Documentation Improvements**
- [ ] Create VIDEO_TUTORIAL_SCRIPT.md for screencast
- [ ] Add TROUBLESHOOTING.md with common issues
- [ ] Create QUICK_START.md as 1-page guide
- [ ] Add inline help to all commands
- [ ] Generate context-aware next steps

### 6. **First-Run Experience**
- [ ] Create welcome message on VS Code open
- [ ] Add .vscode/settings.json with helpful defaults
- [ ] Implement smart command suggestions
- [ ] Create progress indicator for setup steps
- [ ] Add success celebration and next steps

### 7. **Template Cleanup**
- [ ] Move test files to `.claude/tests/google-docs-sync/` directory:
  - `test_project_system_instructions.md`
  - `test_orchestrator.md`
  - `test_methodology_framework.md`
  - `test_sync_config.json`
- [ ] Remove other test artifacts from template root
- [ ] Clean up development artifacts
- [ ] Ensure .gitignore covers all test scenarios
- [ ] Remove duplicate documentation
- [ ] Streamline file structure

### 8. **Integration Testing**
- [ ] Test complete flow on Windows/Mac/Linux
- [ ] Verify with/without Gemini CLI installed
- [ ] Test with various Python versions
- [ ] Validate git remote configurations
- [ ] Test offline setup scenarios

## Completed

### AI Companion Setup Instructions
✅ **Complete setup-ai-companion/ directory with:**
- SETUP_INSTRUCTIONS.md - Overview and platform selection guide
- CLAUDE_PROJECT_INSTRUCTIONS.md - Complete Claude Project setup and instructions
- GEMINI_GEM_INSTRUCTIONS.md - Google Gemini Gem setup and workflow
- CHATGPT_INSTRUCTIONS.md - ChatGPT Custom GPT setup and guidance
- WORKFLOW_REFERENCE.md - Three-way collaboration patterns and best practices

✅ **Updated README.md with AI companion integration section**
✅ **Enhanced project structure to show setup-ai-companion/ directory**

### Key Features Implemented
- **Three-way collaboration model**: Local CLI ↔ AI_CONTEXT.md Bridge ↔ Browser AI
- **Platform-specific instructions** for Claude Project, Gemini Gem, and ChatGPT Custom GPT
- **Context transfer protocols** for seamless handoff between local and browser AI
- **Template intelligence guidance** for strategic AI companion recommendations
- **Quality assurance workflows** and deployment optimization
- **Session bridging patterns** for context continuity

The MADIO framework now supports complete AI companion integration! 🎉