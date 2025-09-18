# Customer Price Sheet Automation

A modern Python automation system for creating Outlook email drafts with customer price sheets. Features a user-friendly GUI dashboard with debugging capabilities, plus CLI alternatives for advanced users.

## Features

### 🎯 Modern GUI Dashboard (v0.3.1)
- **Two-Column Interface**: Intuitive design with draft editor and controls
- **Customer Management**: Complete database management with CRUD operations
- **Multi-layer Verification**: Domain, file path, and recipient verification
- **Live Preview**: Real-time email preview with actual selected month/year
- **Debug Mode**: Comprehensive debugging with timestamped console output
- **Monthly Management**: Load, edit, and save drafts by month/year
- **Critical Bug Fixes**: Resolved month/year consistency and file extraction issues

### 🔧 Core Automation
- **Automated Email Draft Creation**: Creates Outlook drafts with customer-specific content
- **Template Management**: Multiple customizable email templates with placeholders
- **JSON Database**: Modern customer database with comprehensive verification data
- **PDF Attachment Support**: Automatically attaches customer-specific price sheets
- **Safety Features**: Creates drafts only (no automatic sending)

## Quick Start

### Option 1: GUI Dashboard (Recommended)
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Launch the enhanced dashboard:
   ```bash
   python dashboard.py
   ```
   Or double-click: `run_dashboard.vbs`

3. For customer database management:
   ```bash
   # Or double-click: run_customer_system.bat
   ```

### Option 2: CLI Version (Alternative)
```bash
python create_drafts_enhanced.py
```
Or double-click: `run_enhanced_price_sender.vbs`

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

- **Current Version**: 0.3.0
- **Major Features**: Dashboard GUI, bug fixes, comprehensive debugging
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