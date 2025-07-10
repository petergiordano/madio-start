# MADIO Onboard - Streamlined First-Time Setup

**Master onboarding command for new MADIO users - bullet-proof setup in 2-12 minutes**

## Command Purpose

This is the single entry point for all new MADIO users. It provides comprehensive pre-flight validation, progressive setup stages, and smart error recovery to ensure a smooth onboarding experience regardless of user's technical background.

## Onboarding Philosophy

- **Single Entry Point**: One command handles everything
- **Progressive Disclosure**: Core features first, advanced features optional
- **Smart Recovery**: Specific guidance for every error condition
- **Validation First**: Check everything before attempting setup
- **Clear Communication**: User knows exactly what's happening and why

## Usage

```bash
# Standard interactive onboarding (recommended for first-time users)
/madio-onboard

# Note: This command automatically uses --yes flag for madio-setup internally
# to provide streamlined experience while maintaining validation checks
```

## Implementation

### Phase 1: Welcome and Environment Detection

```bash
#!/bin/bash

echo "🚀 MADIO Onboard - Your AI Development Framework"
echo "==============================================="
echo ""
echo "Welcome! This setup will get you building AI systems in 2-12 minutes."
echo ""
echo "📋 What we'll do:"
echo "   ✅ Core Setup (2 min): Python, Git, VS Code basics"
echo "   ⚡ Advanced Setup (10 min): Google Cloud, optional features"
echo "   🎯 Success Validation: Ensure everything works perfectly"
echo ""

# Initialize tracking
SETUP_START_TIME=$(date +%s)
CORE_ISSUES=0
ADVANCED_ISSUES=0
SETUP_STAGE="detection"

# Create onboarding log
mkdir -p .madio-onboard
echo "$(date): Starting MADIO onboarding" > .madio-onboard/setup.log

echo "🔍 Environment Detection"
echo "------------------------"
echo ""

# Detect operating system
OS_TYPE=$(uname -s)
case "$OS_TYPE" in
    Darwin*)
        OS_NAME="macOS"
        PKG_MANAGER="brew"
        ;;
    Linux*)
        OS_NAME="Linux"
        if command -v apt-get &> /dev/null; then
            PKG_MANAGER="apt"
        elif command -v yum &> /dev/null; then
            PKG_MANAGER="yum"
        else
            PKG_MANAGER="unknown"
        fi
        ;;
    CYGWIN*|MINGW32*|MSYS*|MINGW*)
        OS_NAME="Windows"
        PKG_MANAGER="manual"
        ;;
    *)
        OS_NAME="Unknown"
        PKG_MANAGER="unknown"
        ;;
esac

echo "Operating System: $OS_NAME"
echo "Package Manager: $PKG_MANAGER"
echo ""

# Check if in correct directory
PROJECT_NAME=$(basename "$PWD")
if [[ "$PROJECT_NAME" == "madio-start" ]]; then
    echo "❌ CRITICAL: You're in the template repository!"
    echo ""
    echo "🔧 Quick Fix:"
    echo "   1. Go to GitHub.com and create a new repository using madio-start as template"
    echo "   2. Clone YOUR new repository"
    echo "   3. Open YOUR project in VS Code"
    echo "   4. Run /madio-onboard in YOUR project"
    echo ""
    echo "📚 Why: The template is read-only. You need your own copy to build AI systems."
    echo ""
    exit 1
fi

# Check git repository status
if git rev-parse --git-dir &> /dev/null; then
    echo "✅ Git repository detected"
    
    # Check for template usage
    ORIGIN_URL=$(git remote get-url origin 2>/dev/null || echo "none")
    if [[ "$ORIGIN_URL" == *"madio-start"* ]] && [[ "$ORIGIN_URL" != *"$PROJECT_NAME"* ]]; then
        echo "⚠️  Warning: This might be the template repository"
        echo "   Make sure you're in YOUR project, not madio-start"
        echo ""
        read -p "Are you in YOUR project repository? (y/N): " CONFIRM_REPO
        if [[ ! "$CONFIRM_REPO" =~ ^[Yy]$ ]]; then
            echo "Please navigate to your project repository first"
            exit 1
        fi
    fi
else
    echo "❌ Not in a git repository"
    echo "   Initialize git first: git init"
    ((CORE_ISSUES++))
fi

echo "Project Name: $PROJECT_NAME"
echo ""
```

### Phase 2: Core Prerequisites Validation

```bash
echo "🔧 Core Prerequisites Check"
echo "---------------------------"
echo ""

# Python validation
echo "🐍 Python:"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1 | cut -d' ' -f2)
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
    
    if [ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -ge 8 ]; then
        echo "   ✅ Python $PYTHON_VERSION (compatible)"
    else
        echo "   ⚠️  Python $PYTHON_VERSION (may have issues)"
        echo "      Recommended: Python 3.8+"
    fi
else
    echo "   ❌ Python 3 not found"
    echo ""
    echo "🔧 Fix Python Installation:"
    case "$OS_NAME" in
        "macOS")
            echo "   brew install python3"
            ;;
        "Linux")
            case "$PKG_MANAGER" in
                "apt")
                    echo "   sudo apt update && sudo apt install python3 python3-pip python3-venv"
                    ;;
                "yum")
                    echo "   sudo yum install python3 python3-pip"
                    ;;
            esac
            ;;
        "Windows")
            echo "   Download from: https://python.org/downloads"
            echo "   Or use Windows Store: search 'Python'"
            ;;
    esac
    echo ""
    ((CORE_ISSUES++))
fi

# Git validation
echo "📂 Git:"
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | cut -d' ' -f3)
    echo "   ✅ Git $GIT_VERSION"
    
    # Check git configuration
    GIT_NAME=$(git config --global user.name 2>/dev/null || echo "")
    GIT_EMAIL=$(git config --global user.email 2>/dev/null || echo "")
    
    if [[ -z "$GIT_NAME" ]] || [[ -z "$GIT_EMAIL" ]]; then
        echo "   ⚠️  Git not configured"
        echo "      Run: git config --global user.name 'Your Name'"
        echo "      Run: git config --global user.email 'your.email@example.com'"
        ((CORE_ISSUES++))
    else
        echo "   ✅ Git configured ($GIT_NAME <$GIT_EMAIL>)"
    fi
else
    echo "   ❌ Git not installed"
    echo ""
    echo "🔧 Fix Git Installation:"
    case "$OS_NAME" in
        "macOS")
            echo "   brew install git"
            ;;
        "Linux")
            case "$PKG_MANAGER" in
                "apt")
                    echo "   sudo apt update && sudo apt install git"
                    ;;
                "yum")
                    echo "   sudo yum install git"
                    ;;
            esac
            ;;
        "Windows")
            echo "   Download from: https://git-scm.com/download/win"
            ;;
    esac
    echo ""
    ((CORE_ISSUES++))
fi

# VS Code validation
echo "📝 VS Code:"
if command -v code &> /dev/null; then
    echo "   ✅ VS Code CLI available"
    
    # Check if current directory is open in VS Code
    if [ -n "$VSCODE_PID" ] || [ -n "$VSCODE_IPC_HOOK" ]; then
        echo "   ✅ VS Code is running"
    else
        echo "   ℹ️  VS Code not currently running"
        echo "      Tip: Open this project in VS Code for best experience"
    fi
else
    echo "   ⚠️  VS Code CLI not available"
    echo "      Install VS Code and add to PATH"
    echo "      Or continue without VS Code integration"
fi

# Claude Code CLI validation
echo "🤖 Claude Code CLI:"
if [ -d ".claude" ]; then
    echo "   ✅ Claude Code CLI structure detected"
    
    # Check for Claude context
    if [ -f "CLAUDE.md" ]; then
        echo "   ✅ Claude context file present"
    else
        echo "   ⚠️  Claude context file missing"
        echo "      Will be created during setup"
    fi
else
    echo "   ⚠️  No .claude directory"
    echo "      Ensure you're using Claude Code CLI"
    echo "      Or install from: https://docs.anthropic.com/claude-code"
fi

echo ""
```

### Phase 3: Core Setup Decision Point

```bash
echo "📊 Core Setup Summary"
echo "--------------------"
echo ""

if [ "$CORE_ISSUES" -eq 0 ]; then
    echo "🎉 Core prerequisites look good!"
    echo "   Ready for MADIO setup"
    SETUP_STAGE="core_ready"
else
    echo "⚠️  Found $CORE_ISSUES core issues"
    echo "   These need to be resolved first"
    SETUP_STAGE="core_issues"
fi

echo ""
echo "🎯 Next Steps:"
echo ""

if [ "$CORE_ISSUES" -gt 0 ]; then
    echo "❌ RESOLVE CORE ISSUES FIRST:"
    echo "   1. Fix the issues listed above"
    echo "   2. Run /madio-onboard again"
    echo "   3. Continue with MADIO setup"
    echo ""
    echo "💡 Need help? Check the specific fix commands above"
    echo ""
    
    # Log issues
    echo "$(date): Core issues found: $CORE_ISSUES" >> .madio-onboard/setup.log
    exit 1
fi

echo "✅ CORE SETUP (2 minutes):"
echo "   • Initialize MADIO project structure"
echo "   • Set up Python environment"
echo "   • Configure basic commands"
echo "   • Create essential files"
echo ""
echo "⚡ ADVANCED SETUP (10 minutes, optional):"
echo "   • Google Cloud configuration"
echo "   • Google Docs sync capability"
echo "   • Advanced VS Code integration"
echo "   • Performance optimizations"
echo ""

read -p "Start Core Setup now? (Y/n): " START_CORE
if [[ "$START_CORE" =~ ^[Nn]$ ]]; then
    echo "Setup paused. Run /madio-onboard when ready."
    exit 0
fi

echo ""
echo "🚀 Starting Core Setup..."
echo ""
```

### Phase 4: Core Setup Execution

```bash
SETUP_STAGE="core_setup"
CORE_START_TIME=$(date +%s)

echo "📁 Project Structure Setup"
echo "-------------------------"
echo ""

# Run madio-setup if not already done
if [ ! -f ".madio-setup-complete" ]; then
    echo "Initializing MADIO project..."
    
    # Check if madio-setup command exists
    if [ -f ".claude/commands/madio-setup.md" ]; then
        /madio-setup --yes
        if [ $? -eq 0 ]; then
            echo "✅ MADIO project initialized"
        else
            echo "❌ MADIO setup failed"
            echo "   Check the error messages above"
            exit 1
        fi
    else
        echo "❌ MADIO setup command not found"
        echo "   Ensure you're using the correct MADIO template"
        exit 1
    fi
else
    echo "✅ MADIO project already initialized"
fi

# Python environment setup
echo ""
echo "🐍 Python Environment Setup"
echo "---------------------------"
echo ""

# Create virtual environment for MADIO
if [ ! -d ".madio-venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .madio-venv
    
    if [ $? -eq 0 ]; then
        echo "✅ Python virtual environment created"
    else
        echo "❌ Failed to create virtual environment"
        echo "   Check Python installation and try again"
        exit 1
    fi
else
    echo "✅ Python virtual environment already exists"
fi

# Install basic requirements
if [ -f "requirements.txt" ]; then
    echo "Installing Python dependencies..."
    source .madio-venv/bin/activate
    pip install -q -r requirements.txt
    
    if [ $? -eq 0 ]; then
        echo "✅ Python dependencies installed"
    else
        echo "⚠️  Some dependency installation issues"
        echo "   Check requirements.txt and try manual install"
    fi
    deactivate
else
    echo "ℹ️  No requirements.txt found (OK for basic setup)"
fi

# Essential files validation
echo ""
echo "📄 Essential Files Check"
echo "------------------------"
echo ""

ESSENTIAL_FILES=("README.md" "CLAUDE.md" ".gitignore")
for file in "${ESSENTIAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "⚠️  $file missing"
        case "$file" in
            "README.md")
                echo "# $PROJECT_NAME" > README.md
                echo "Created basic README.md"
                ;;
            ".gitignore")
                echo "*.pyc" > .gitignore
                echo "__pycache__/" >> .gitignore
                echo ".venv/" >> .gitignore
                echo ".madio-venv/" >> .gitignore
                echo "Created basic .gitignore"
                ;;
        esac
    fi
done

# Project configuration directory setup
echo ""
echo "📁 Project Configuration Setup"
echo "------------------------------"
echo ""

# Create project-config directory for storing project-specific records
mkdir -p .claude/project-config
echo "✅ Created .claude/project-config/ directory"
echo "   This will store project-specific configuration records"

# Core setup completion
CORE_END_TIME=$(date +%s)
CORE_DURATION=$((CORE_END_TIME - CORE_START_TIME))

echo ""
echo "✅ Core Setup Complete! ($CORE_DURATION seconds)"
echo ""
echo "🎯 What's Ready:"
echo "   • MADIO project structure initialized"
echo "   • Python environment configured"
echo "   • Essential files present"
echo "   • Basic commands available"
echo ""
```

### Phase 5: Advanced Setup Options

```bash
echo "⚡ Advanced Setup Options"
echo "========================"
echo ""
echo "Advanced features are completely optional but unlock powerful capabilities:"
echo ""
echo "🔗 Google Docs Sync (5 minutes):"
echo "   • Automatic sync between local files and Google Docs"
echo "   • Perfect for Claude Project integration"
echo "   • Enables collaborative editing"
echo ""
echo "🔧 Development Tools (3 minutes):"
echo "   • Enhanced VS Code integration"
echo "   • Git hooks and automation"
echo "   • Performance monitoring"
echo ""
echo "🎯 Advanced Templates (2 minutes):"
echo "   • Additional MADIO templates"
echo "   • Industry-specific configurations"
echo "   • Advanced AI system patterns"
echo ""

read -p "Configure Advanced Features? (y/N): " SETUP_ADVANCED
if [[ ! "$SETUP_ADVANCED" =~ ^[Yy]$ ]]; then
    echo ""
    echo "✅ Skipping advanced setup"
    echo "   You can run /madio-enable-sync or /madio-doctor later"
    SETUP_STAGE="core_complete"
else
    echo ""
    echo "🚀 Starting Advanced Setup..."
    echo ""
    
    SETUP_STAGE="advanced_setup"
    ADVANCED_START_TIME=$(date +%s)
    
    # Google Docs Sync Option
    echo "🔗 Google Docs Sync Setup"
    echo "-------------------------"
    echo ""
    
    read -p "Enable Google Docs sync? (y/N): " ENABLE_SYNC
    if [[ "$ENABLE_SYNC" =~ ^[Yy]$ ]]; then
        if [ -f ".claude/commands/madio-enable-sync.md" ]; then
            /madio-enable-sync
            if [ $? -eq 0 ]; then
                echo "✅ Google Docs sync configured"
            else
                echo "⚠️  Google Docs sync setup had issues"
                echo "   You can complete this later with /madio-enable-sync"
                ((ADVANCED_ISSUES++))
            fi
        else
            echo "❌ Google Docs sync command not found"
            echo "   Update your MADIO template for this feature"
            ((ADVANCED_ISSUES++))
        fi
    else
        echo "✅ Skipping Google Docs sync"
    fi
    
    # VS Code Integration
    echo ""
    echo "🔧 VS Code Integration"
    echo "---------------------"
    echo ""
    
    if command -v code &> /dev/null; then
        echo "Installing recommended VS Code extensions..."
        
        # Install essential extensions
        EXTENSIONS=(
            "ms-python.python"
            "davidanson.vscode-markdownlint"
            "yzhang.markdown-all-in-one"
            "eamodio.gitlens"
        )
        
        for ext in "${EXTENSIONS[@]}"; do
            code --install-extension "$ext" --force &> /dev/null
            if [ $? -eq 0 ]; then
                echo "✅ $ext"
            else
                echo "⚠️  $ext (may already be installed)"
            fi
        done
        
        # Create workspace file if it doesn't exist
        WORKSPACE_FILE="${PROJECT_NAME}.code-workspace"
        if [ ! -f "$WORKSPACE_FILE" ]; then
            cat > "$WORKSPACE_FILE" << EOF
{
    "folders": [
        {
            "path": "."
        }
    ],
    "settings": {
        "python.defaultInterpreterPath": "./.madio-venv/bin/python",
        "python.terminal.activateEnvironment": true,
        "markdownlint.config": {
            "MD013": false,
            "MD041": false
        }
    }
}
EOF
            echo "✅ Created VS Code workspace file"
        fi
    else
        echo "⚠️  VS Code CLI not available"
        echo "   Install VS Code for enhanced integration"
        ((ADVANCED_ISSUES++))
    fi
    
    ADVANCED_END_TIME=$(date +%s)
    ADVANCED_DURATION=$((ADVANCED_END_TIME - ADVANCED_START_TIME))
    
    echo ""
    echo "✅ Advanced Setup Complete! ($ADVANCED_DURATION seconds)"
    echo ""
fi
```

### Phase 6: Success Validation & Dashboard

```bash
echo "🎯 Success Validation Dashboard"
echo "==============================="
echo ""

SETUP_STAGE="validation"
VALIDATION_START_TIME=$(date +%s)

# Run comprehensive health check
echo "🏥 Running Health Check..."
echo ""

# Use madio-doctor if available
if [ -f ".claude/commands/madio-doctor.md" ]; then
    /madio-doctor
    HEALTH_STATUS=$?
else
    # Basic health check
    echo "📋 Basic Health Check:"
    echo ""
    
    HEALTH_ISSUES=0
    
    # Check core files
    if [ -f "project_system_instructions.md" ]; then
        echo "✅ Core AI system files present"
    else
        echo "⚠️  Run /generate-ai-system to create your AI"
        ((HEALTH_ISSUES++))
    fi
    
    # Check Python environment
    if [ -d ".madio-venv" ]; then
        echo "✅ Python environment ready"
    else
        echo "❌ Python environment missing"
        ((HEALTH_ISSUES++))
    fi
    
    # Check git status
    if git status --porcelain | grep -q .; then
        echo "ℹ️  Uncommitted changes (normal during setup)"
    else
        echo "✅ Git working directory clean"
    fi
    
    HEALTH_STATUS=$HEALTH_ISSUES
fi

echo ""
echo "📊 Setup Summary"
echo "---------------"
echo ""

SETUP_END_TIME=$(date +%s)
TOTAL_DURATION=$((SETUP_END_TIME - SETUP_START_TIME))

echo "⏱️  Total Setup Time: $TOTAL_DURATION seconds"
echo "🎯 Setup Stage: $SETUP_STAGE"
echo "❌ Core Issues: $CORE_ISSUES"
echo "⚠️  Advanced Issues: $ADVANCED_ISSUES"
echo "🏥 Health Status: $HEALTH_STATUS"
echo ""

# Overall success assessment
if [ "$CORE_ISSUES" -eq 0 ] && [ "$HEALTH_STATUS" -eq 0 ]; then
    echo "🎉 SETUP SUCCESSFUL!"
    echo "   Your MADIO project is ready for AI development"
    SETUP_SUCCESS=true
elif [ "$CORE_ISSUES" -eq 0 ] && [ "$HEALTH_STATUS" -lt 3 ]; then
    echo "✅ SETUP MOSTLY SUCCESSFUL"
    echo "   Minor issues can be resolved later"
    SETUP_SUCCESS=true
else
    echo "⚠️  SETUP NEEDS ATTENTION"
    echo "   Review issues above and run /madio-doctor"
    SETUP_SUCCESS=false
fi

echo ""
```

### Phase 7: Next Steps & Completion

```bash
echo "🚀 What's Next?"
echo "==============="
echo ""

if [ "$SETUP_SUCCESS" = true ]; then
    echo "🎯 Ready to Build AI Systems!"
    echo ""
    echo "Quick Start Commands:"
    echo "   /generate-ai-system \"describe your AI system\""
    echo "   /madio-doctor  # Check project health anytime"
    echo "   /push-to-docs  # Sync to Google Docs (if enabled)"
    echo ""
    echo "📚 Learning Resources:"
    echo "   • Read madio_core_templates.md for template guide"
    echo "   • Check GETTING-STARTED.md for detailed walkthrough"
    echo "   • Use AI_CONTEXT.md for AI collaboration"
    echo ""
    echo "💡 Pro Tips:"
    echo "   1. Start with a simple AI system first"
    echo "   2. Use /madio-doctor regularly for health checks"
    echo "   3. Keep AI_CONTEXT.md updated for better AI help"
    echo "   4. Commit your progress frequently"
    echo ""
    
    # Create completion marker
    echo "$(date): MADIO onboarding completed successfully" > .madio-onboard/complete
    echo "Setup time: $TOTAL_DURATION seconds" >> .madio-onboard/complete
    echo "Core issues: $CORE_ISSUES" >> .madio-onboard/complete
    echo "Advanced issues: $ADVANCED_ISSUES" >> .madio-onboard/complete
    echo "Health status: $HEALTH_STATUS" >> .madio-onboard/complete
    
else
    echo "🔧 Issues to Resolve:"
    echo ""
    echo "Priority Actions:"
    if [ "$CORE_ISSUES" -gt 0 ]; then
        echo "   1. Fix core prerequisite issues (see above)"
        echo "   2. Run /madio-onboard again"
    fi
    if [ "$HEALTH_STATUS" -gt 0 ]; then
        echo "   3. Run /madio-doctor for detailed diagnostics"
        echo "   4. Address any remaining issues"
    fi
    echo ""
    echo "🆘 Need Help?"
    echo "   • Check the specific error messages above"
    echo "   • Run /madio-doctor for comprehensive diagnostics"
    echo "   • Review GETTING-STARTED.md for troubleshooting"
    echo ""
fi

echo "📝 Support Resources:"
echo "   • GitHub: https://github.com/petergiordano/madio-start"
echo "   • Documentation: All AI system documents in this project"
echo "   • Community: Coming soon!"
echo ""

echo "🎓 Remember:"
echo "   MADIO handles the complexity so you can focus on your unique AI value."
echo "   Start building something amazing!"
echo ""

# Final logging
echo "$(date): MADIO onboarding completed" >> .madio-onboard/setup.log
echo "Total time: $TOTAL_DURATION seconds" >> .madio-onboard/setup.log
echo "Success: $SETUP_SUCCESS" >> .madio-onboard/setup.log

echo "⚡ Setup complete! Time to build AI systems with MADIO!"
```

## Error Recovery Patterns

### Smart Recovery System
```bash
# Pattern for handling common errors
handle_error() {
    local error_type=$1
    local context=$2
    
    case "$error_type" in
        "python_missing")
            echo "🔧 Python Installation Guide:"
            echo "   Choose your platform-specific solution above"
            echo "   Then run: /madio-onboard"
            ;;
        "git_not_configured")
            echo "🔧 Git Configuration:"
            echo "   git config --global user.name 'Your Name'"
            echo "   git config --global user.email 'your@email.com'"
            echo "   Then run: /madio-onboard"
            ;;
        "permission_denied")
            echo "🔧 Permission Fix:"
            echo "   Check file permissions: ls -la $context"
            echo "   Fix with: chmod +x $context"
            ;;
        "network_error")
            echo "🔧 Network Issue:"
            echo "   Check internet connection"
            echo "   Try again in a few minutes"
            echo "   Use offline mode if available"
            ;;
    esac
}
```

### Rollback Capability
```bash
# Rollback mechanism for failed setups
rollback_setup() {
    echo "🔄 Rolling back changes..."
    
    # Remove partial setup files
    rm -f .madio-setup-complete
    rm -rf .madio-venv
    rm -rf .madio-onboard
    
    # Restore git state if needed
    if [ -f ".madio-onboard/git-backup" ]; then
        git checkout -- .
    fi
    
    echo "✅ Rollback complete. You can start fresh."
}
```

## Integration Notes

- **Progressive Enhancement**: Works with existing madio-setup command
- **Backward Compatible**: Doesn't break existing MADIO installations
- **Modular Design**: Each phase can be run independently
- **Comprehensive Logging**: Full audit trail of setup process
- **Smart Detection**: Adapts to different environments and configurations

## Usage Examples

```bash
# Fresh installation
/madio-onboard

# Quick health check after setup
/madio-doctor

# Re-run if issues found
/madio-onboard
```

This command transforms the MADIO onboarding experience from a complex multi-step process into a single, guided, bullet-proof setup that works for users of all technical levels.