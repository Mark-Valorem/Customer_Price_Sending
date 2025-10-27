# Customer Price Sheet Automation v4.0.1

A streamlined Python automation system for creating Outlook email drafts with customer price sheets. Version 4.0.1 includes bug fixes for CC emails, recipient names, and font styling.

## 🚀 What's New in Version 4.0.1

### Bug Fixes
- **CC Emails Now Configurable**: Settings tab now actually saves and uses CC email addresses
- **All Recipient Names**: Email greetings now include ALL recipient names, not just the first one
- **Font Styling Fixed**: Emails now use Aptos 11pt instead of defaulting to Times New Roman 12pt
- **Settings Persistence**: CC email configuration saved to `config/app_settings.json`

### Previous Major Updates (v4.0.0)

#### Documentation Overhaul
- **.agent Documentation System**: AI-optimized context management for enhanced development
- **Comprehensive SOPs**: Standard Operating Procedures for all common tasks
- **System Architecture Docs**: Detailed technical documentation for codebase understanding
- **Automated Documentation Updates**: Commands for maintaining documentation hygiene
- **Version Tracking**: All documentation includes semantic versioning

### Previous Bug Fixes (v3.0.1)

### Critical Fixes
- **Verification System Fix**: Resolved "'str' object has no attribute 'get'" error in customer verification
- **Data Structure Compatibility**: Fixed file_generation handling for JSON database format
- **Enhanced Error Handling**: Improved compatibility between dictionary and list data structures
- **Archive Cleanup**: Moved outdated launcher files to Archive for better organization

### Major Features from v3.0
- **Direct Launch**: No terminal selection - application starts immediately
- **User Signatures**: Select between Jason Najm and Mark Anderson with HTML signatures
- **Company Logo**: Valorem branding in the dashboard header
- **Enhanced Verification**: 50/50 split layout with real-time progress for ALL customers
- **Simplified Templates**: Single default template with auto-save functionality
- **Playwright Testing**: Automated UI testing for quality assurance

## Features

### 🎯 Modern GUI Dashboard (v3.0)
- **Direct Launch Interface**: No terminal windows or selection dialogs
- **Customer Management**: Complete database with 50/50 verification console
- **Real-time Verification**: Test ALL customers with comprehensive reporting
- **User Selection**: Choose sender with automatic signature application
- **Live Preview**: Real-time email preview with selected user's signature
- **Company Branding**: Valorem logo integration
- **Auto-Save Templates**: Changes saved automatically as you type

### 🔧 Core Automation
- **Automated Email Draft Creation**: Creates Outlook drafts with customer-specific content
- **Template Management**: Multiple customizable email templates with placeholders
- **JSON Database**: Modern customer database with comprehensive verification data
- **PDF Attachment Support**: Automatically attaches customer-specific price sheets
- **Safety Features**: Creates drafts only (no automatic sending)

## Quick Start

### Installation
```bash
pip install -r requirements.txt
```

### Running the Application

#### Option 1: Direct Launch (Recommended)
Double-click `run_dashboard.vbs` - the application launches immediately without any dialogs.

#### Option 2: Command Line
```bash
python dashboard.py
```

#### Option 3: CLI Version (Legacy)
```bash
python create_drafts_enhanced.py
```

### First Time Setup
1. Ensure HTML signature files are in `data/` folder:
   - `Mark_Anderson_231123.html`
   - `Jason_Najm_250427.html`
2. Ensure `valorem_logo.png` is in the root directory
3. Configure customer database in the Customer Management tab

## Project Structure

```
├── src/                         # Core Python modules
│   ├── __init__.py             # Package initialization
│   ├── main.py                 # Package entry point
│   └── email_generator.py      # Core email generation logic
├── monthly_drafts/             # Monthly draft storage
├── logs/                       # Application logs
├── tests/                      # Test files
├── scripts/                    # Version management utilities
├── Archive/                    # Organized archived files
│   ├── legacy_cli_scripts/    # Original CLI tools
│   ├── development_tests/     # Development phase tests
│   ├── unused_web_interface/  # Placeholder web files
│   ├── sandbox_data/          # Test data files
│   └── generated_files/       # Build artifacts
├── dashboard.py               # 🎯 Main GUI application
├── create_drafts_enhanced.py  # CLI alternative interface
├── manage_templates.py        # Template management utility
├── email_templates.json       # Email template configurations
├── Python_CustomerPricing.xlsx # Production data file
├── pyproject.toml            # Modern Python project config
└── requirements.txt          # Dependencies
```

## Key Components

### Active Applications
- **`dashboard.py`**: Modern GUI with customer management, verification system, and critical bug fixes ⭐ **MAIN INTERFACE**
- **`create_drafts_enhanced.py`**: Enhanced CLI version (backup/alternative interface)
- **`src/email_generator.py`**: Core email generation module (shared by both interfaces)
- **`manage_templates.py`**: Template management utility

### Configuration & Data
- **`email_templates.json`**: Customizable email templates with placeholders
- **`data/customer_database.json`**: Primary customer database with verification data
- **`Python_CustomerPricing.xlsx`**: Legacy Excel data (for reference/migration only)
- **`monthly_drafts/`**: Monthly draft storage and configurations

### Archived Components
- All legacy tools, test files, and unused components organized in `Archive/` by category

## Technologies Used

- **Python 3.8+**: Core automation logic
- **tkinter**: Modern GUI dashboard interface
- **pandas**: Excel file processing and data manipulation
- **pywin32**: Microsoft Outlook COM automation
- **openpyxl**: Excel file reading and manipulation
- **python-dateutil**: Date calculations and formatting

## Version Information

- **Current Version**: 4.0.1
- **Major Features**: Verification system fixes, dashboard GUI, customer management
- **Recent Fix**: Resolved customer verification error with JSON database compatibility
- **Compatibility**: Windows (requires Microsoft Outlook)
- **Python Support**: 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- **HTML/CSS**: Template formatting

## Development and Versioning

This project follows semantic versioning (SemVer) and includes automated development workflows:

### Version Management
- **Semantic Versioning**: MAJOR.MINOR.PATCH format
- **Automated Bumping**: Use `scripts/bump_version.bat` (Windows) or `scripts/bump_version.sh` (Linux/Mac)
- **Git Integration**: Automatic tagging and changelog generation

### Code Quality
- **Pre-commit Hooks**: Automated code formatting, linting, and validation
- **Conventional Commits**: Standardized commit message format
- **CI/CD Pipeline**: GitHub Actions for testing and releases

### Quick Development Setup
```bash
# Install with development dependencies
pip install -e ".[dev]"

# Set up pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

# Bump version (patch/minor/major)
scripts\bump_version.bat patch
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed development guidelines.

## Important Notes

- Requires Outlook to be installed and configured
- Excel files must be closed before running scripts
- PDF files must exist at paths specified in Excel
- Creates drafts only - manual review required before sending
- Customer data is protected via .gitignore patterns

## AI Integration

This project uses `CLAUDE.md` for AI assistance and automated development guidance. The file contains project-specific instructions for Claude Code to understand the codebase structure and requirements.