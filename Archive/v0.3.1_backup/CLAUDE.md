# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose
This codebase automates the creation of Outlook email drafts for sending monthly customer price sheets. It reads customer data from an Excel workbook and creates personalized drafts with PDF attachments.

## Key Commands

### Running the application
```bash
# Modern GUI Dashboard (RECOMMENDED)
python dashboard.py
# Or double-click: run_dashboard.vbs

# Enhanced CLI version (alternative interface)
python create_drafts_enhanced.py
# Or double-click: run_enhanced_price_sender.vbs

# Template management utility
python manage_templates.py
```

### Legacy/Archived scripts
```bash
# These scripts are now in Archive/ for reference only:
# Archive/legacy_cli_scripts/create_drafts.py       # Original CLI version
# Archive/legacy_cli_scripts/check_columns.py       # Column verification
# Archive/legacy_cli_scripts/diagnose_excel.py      # Excel diagnostics
```

### Installing dependencies
```bash
# Production dependencies only
pip install -r requirements.txt

# Development dependencies (includes testing, linting, versioning tools)
pip install -e ".[dev]"

# Manual installation of core dependencies
pip install pandas pywin32 openpyxl python-dateutil
```

### Version management
```bash
# Bump patch version (0.1.0 → 0.1.1)
scripts\bump_version.bat patch

# Bump minor version (0.1.0 → 0.2.0)
scripts\bump_version.bat minor

# Bump major version (0.1.0 → 1.0.0)
scripts\bump_version.bat major

# Preview changes without making them
scripts\bump_version.bat patch --dry-run
```

### Development workflow
```bash
# Set up development environment
pip install -e ".[dev]"
pre-commit install
pre-commit install --hook-type commit-msg

# Run code quality checks
pre-commit run --all-files

# Run tests
pytest tests/ -v --cov=src
```

## Architecture

### Core Components
- **dashboard.py**: Modern GUI application with customer management, two-column layout, debugging features, and comprehensive bug fixes (CURRENT MAIN INTERFACE)
- **src/email_generator.py**: Core email generation module used by dashboard and CLI versions
- **create_drafts_enhanced.py**: Enhanced CLI script with customizable templates (backup/alternative interface)
- **email_templates.json**: Template configuration file containing multiple email templates, signature, and default values
- **manage_templates.py**: Interactive template management utility for creating/editing email templates
- **Python_CustomerPricing.xlsx**: Legacy Excel file for reference (system now uses JSON database)
- **data/customer_database.json**: Primary customer database with comprehensive verification data
- **monthly_drafts/**: Directory for storing monthly draft templates and configurations
- **VBS launchers**: Double-click scripts for easy execution (run_dashboard.vbs, run_enhanced_price_sender.vbs)

### Archived Components (in Archive/)
- **legacy_cli_scripts/**: Original CLI scripts (create_drafts.py, check_columns.py, diagnose_excel.py)
- **development_tests/**: Test files used during development (test_*.py)
- **unused_web_interface/**: Placeholder web templates (not implemented)
- **sandbox_data/**: Test data files
- **generated_files/**: Python cache and build artifacts

### Data Flow
1. JSON database (data/customer_database.json) contains structured customer data
2. Required fields: company_name, email_addresses, recipient_names, file_generation paths
3. Multi-layer verification system validates:
   - Domain verification for email addresses
   - File path verification for attachments
   - Recipient authorization checks
4. For each customer record:
   - Creates Outlook draft with HTML body
   - Attaches PDF from dynamic file naming (YYMMDD_*.pdf)
   - Sets CC to support@valorem.com.au and jasonn@valorem.com.au
   - Comprehensive audit logging
   - Saves as draft (does not send)

### Key File Paths
- Excel workbook: `C:\Users\MarkAnderson\Valorem\Knowledge Hub - Documents\Pricing\Customer Price Lists\Price Sheet Sending_Python\Python_CustomerPricing.xlsx`
- PDF attachments: Synced from SharePoint via OneDrive to local paths specified in Excel

## Dashboard Features (dashboard.py) - CURRENT MAIN INTERFACE

### Enhanced Customer Management (v2.0)
- **Customer Database Management**: Complete CRUD operations for customer records
- **Multi-layer Verification**: Domain, file path, and recipient verification
- **Audit Logging**: Comprehensive tracking of all system operations
- **Excel-free Operation**: Pure JSON database system with migration tools

### User Interface
- **Two-Column Layout**: 60% left (email content/preview), 40% right (controls)
- **Responsive Design**: Columns stack on narrow screens
- **Minimum Heights**: Draft area (400px), Preview (300px), Debug panel (150px)

### Key Features
- **Email Draft Editor**: Full-featured text editor with syntax highlighting for templates
- **Live Preview**: Real-time preview with sample customer data and variable resolution
- **Monthly Management**: Load/save/edit drafts by month and year
- **Template Variables**: Automatic resolution of {current_month}, {previous_month}, etc.
- **Debug Mode**: Comprehensive debugging with timestamped console output
- **Error Handling**: Detailed error messages with troubleshooting steps
- **Progress Tracking**: Real-time progress bar during email generation

### Bug Fixes (v0.3.0)
- **Fixed Duplicate Signatures**: Automatic signature stripping prevents duplication
- **Fixed Variable Resolution**: {current_month} and other variables now resolve correctly
- **Enhanced Error Handling**: Better error reporting with actionable information

## Enhanced Features (create_drafts_enhanced.py) - CLI Alternative
- **Template Selection**: Choose from multiple pre-defined email templates (default, price_increase, no_change, promotional)
- **Monthly Customization**: Interactive prompt to customize template values each month (pricing notes, dates, percentages, etc.)
- **Template Preview**: See how the email will look before creating all drafts
- **Date Automation**: Automatic calculation of current month, previous month, quarter dates
- **Template Management**: Use manage_templates.py to create, edit, delete, and preview templates
- **Signature Customization**: Centralized signature management in templates file

## Template Structure
Templates are stored in email_templates.json with:
- **templates**: Multiple email templates with placeholders
- **signature**: Company signature information
- **default_values**: Pre-filled values for common placeholders
- **placeholders**: Documentation of available placeholders

## Project Structure

This project follows Python best practices with clean organization:

```
├── src/                         # Core Python modules
│   ├── __init__.py             # Package initialization
│   ├── main.py                 # Entry point for package
│   └── email_generator.py      # Core email generation logic
├── monthly_drafts/             # Monthly draft storage
│   ├── 2025_09.txt            # Monthly draft templates
│   └── dashboard_template.json # Dashboard-generated templates
├── logs/                       # Application logs
├── tests/                      # Test files (proper test structure)
│   ├── __init__.py            # Test package initialization
│   └── test_main.py           # Main functionality tests
├── scripts/                    # Utility scripts
│   ├── bump_version.bat       # Version management (Windows)
│   └── bump_version.sh        # Version management (Unix)
├── Archive/                    # Organized archived files
│   ├── legacy_cli_scripts/    # Original CLI scripts
│   ├── development_tests/     # Development test files
│   ├── unused_web_interface/  # Placeholder web files
│   ├── sandbox_data/          # Test data files
│   ├── generated_files/       # Build artifacts
│   └── old_logs/             # Historical log files
├── dashboard.py               # Main GUI application (CURRENT INTERFACE)
├── create_drafts_enhanced.py  # Enhanced CLI version (backup interface)
├── manage_templates.py        # Template management utility
├── email_templates.json       # Email template configurations
├── Python_CustomerPricing.xlsx # Production data file
├── requirements.txt           # Python dependencies
├── pyproject.toml            # Modern Python project configuration
├── README.md                 # Project documentation
└── CLAUDE.md                # AI guidance (this file)
```

### Tech Stack & Structure
- **GUI Interface**: Python tkinter with modern two-column design
- **Backend**: Python with pandas, pywin32, openpyxl, python-dateutil
- **Data Processing**: Excel file reading with pandas
- **Email Generation**: Microsoft Outlook COM automation
- **Testing**: Python unittest framework (structure ready)

### Development Guidelines
- **Current Structure**: Modern Python package structure with main application in root
- **Core Logic**: Centralized in `src/` directory for reusability
- **Archive Organization**: Legacy files organized by category in `Archive/`
- **Tests**: Proper test structure in `tests/` directory
- **Documentation**: Comprehensive README.md and CONTRIBUTING.md

## Important Notes
- **Excel Requirements**: File must be closed before running scripts
- **Outlook Requirements**: Must be installed, configured, and signed in
- **File Paths**: PDF files must exist at exact paths specified in Excel (FilePath + FileName)
- **Data Structure**: Headers are on row 4 of Excel (row 3 when 0-indexed in pandas)
- **Email Safety**: Scripts create drafts only - manual review and sending required
- **Dependencies**: All required packages listed in requirements.txt and pyproject.toml
- **Backward Compatibility**: Original functionality preserved in Archive/legacy_cli_scripts/ for reference

## Version Management and Release Process

This project implements semantic versioning with automated tooling:

### Versioning System
- **Current Version**: Tracked in pyproject.toml and src/__init__.py
- **Bump2version**: Automated version bumping with git tagging
- **Conventional Commits**: Enforced commit message format
- **Changelog**: Automatically generated from commit history
- **GitHub Actions**: CI/CD pipeline for testing and releases

### Release Workflow
1. **Development**: Follow conventional commit format
2. **Version Bump**: Use scripts/bump_version.bat with patch/minor/major
3. **Automatic**: Git commit, tag creation, and push to remote
4. **CI/CD**: GitHub Actions builds, tests, and creates releases
5. **Artifacts**: Distribution packages and changelog generation

### Code Quality Standards
- **Pre-commit hooks**: Formatting, linting, security scanning
- **Testing**: pytest with coverage reporting
- **Documentation**: Comprehensive README.md and CONTRIBUTING.md
- **Security**: bandit scanning for vulnerabilities

## AI Guidance
This file is used by Claude Code to understand the project structure and provide appropriate development assistance. The project follows modern Python development practices with automated versioning, testing, and release workflows.