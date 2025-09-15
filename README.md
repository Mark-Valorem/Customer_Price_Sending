# Customer Price Sheet Automation

A Python-based automation system for creating Outlook email drafts with customer price sheets. This system reads customer data from Excel files and generates personalized email drafts with PDF attachments for monthly price sheet distribution.

## Features

- **Automated Email Draft Creation**: Creates Outlook drafts with customer-specific content
- **Template Management**: Multiple customizable email templates with placeholders
- **Interactive Configuration**: Monthly customization of template values
- **Excel Integration**: Reads customer data from Excel workbooks
- **PDF Attachment Support**: Automatically attaches customer-specific price sheets
- **Safety Features**: Creates drafts only (no automatic sending)

## Quick Start

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the enhanced version with template selection:
   ```bash
   python create_drafts_enhanced.py
   ```

3. Or use the VBS launcher for easy execution:
   - Double-click `run_enhanced_price_sender.vbs`

## Project Structure

```
├── src/                    # Python source code
│   ├── __init__.py
│   └── main.py            # Main entry point
├── templates/             # HTML templates
│   └── index.html
├── static/               # Static assets (CSS, images)
│   └── styles.css
├── tests/                # Test files
│   ├── __init__.py
│   └── test_main.py
├── Archive/              # Archived/backup files
├── create_drafts.py      # Original automation script
├── create_drafts_enhanced.py  # Enhanced version with templates
├── manage_templates.py   # Template management utility
├── email_templates.json  # Email template configurations
├── check_columns.py      # Excel column verification
├── diagnose_excel.py     # Excel structure analysis
├── requirements.txt      # Python dependencies
├── CLAUDE.md            # AI assistance guidelines
└── README.md           # This file
```

## Key Components

- **Core Scripts**: `create_drafts.py` (original), `create_drafts_enhanced.py` (enhanced)
- **Template System**: `email_templates.json` for customizable email templates
- **Management Tools**: `manage_templates.py` for template editing
- **Diagnostic Tools**: `check_columns.py`, `diagnose_excel.py` for troubleshooting
- **VBS Launchers**: Easy double-click execution scripts

## Technologies Used

- **Python**: Core automation logic
- **pandas**: Excel file processing
- **pywin32**: Outlook integration
- **openpyxl**: Excel file manipulation
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