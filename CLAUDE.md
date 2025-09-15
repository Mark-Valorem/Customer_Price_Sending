# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose
This codebase automates the creation of Outlook email drafts for sending monthly customer price sheets. It reads customer data from an Excel workbook and creates personalized drafts with PDF attachments.

## Key Commands

### Running scripts
```bash
# Original version (hardcoded templates)
python create_drafts.py

# Enhanced version (with customizable templates)
python create_drafts_enhanced.py

# Template management
python manage_templates.py

# Easy launching (double-click VBS files)
run_price_sender.vbs                # Original version
run_enhanced_price_sender.vbs       # Enhanced version
```

### Diagnostic and utility scripts
```bash
python check_columns.py     # Verify Excel column names
python diagnose_excel.py    # Detailed Excel structure analysis
```

### Installing dependencies
```bash
pip install pandas pywin32 openpyxl python-dateutil
```

## Architecture

### Core Components
- **create_drafts.py**: Original script with hardcoded email template
- **create_drafts_enhanced.py**: Enhanced script with customizable templates, interactive selection, and monthly customization
- **email_templates.json**: Template configuration file containing multiple email templates, signature, and default values
- **manage_templates.py**: Interactive template management utility for creating/editing email templates
- **Python_CustomerPricing.xlsx**: Source Excel file containing customer data with headers on row 4 (0-indexed row 3)
- **VBS launchers**: Double-click scripts for easy execution (run_price_sender.vbs, run_enhanced_price_sender.vbs)
- **Backup files**: Original versions preserved (*_backup.py)
- **Check/diagnostic scripts**: Utilities for troubleshooting Excel column mapping issues

### Data Flow
1. Excel file is read using pandas with header on row 3 (0-indexed)
2. Required columns: EmailAddresses, CustomerName, RecipientName, FilePath, FileName
3. For each customer row:
   - Creates Outlook draft with HTML body
   - Attaches PDF from FilePath + FileName
   - Sets CC to support@valorem.com.au and jasonn@valorem.com.au
   - Saves as draft (does not send)

### Key File Paths
- Excel workbook: `C:\Users\MarkAnderson\Valorem\Knowledge Hub - Documents\Pricing\Customer Price Lists\Price Sheet Sending_Python\Python_CustomerPricing.xlsx`
- PDF attachments: Synced from SharePoint via OneDrive to local paths specified in Excel

## Enhanced Features (create_drafts_enhanced.py)
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

This project follows Python best practices with the following organization:

```
├── src/                    # Python source code modules
│   ├── __init__.py        # Package initialization
│   └── main.py           # Main entry point (future refactoring target)
├── templates/             # HTML templates for web interface
│   └── index.html        # Main HTML template
├── static/               # Static assets (CSS, JavaScript, images)
│   └── styles.css        # Main stylesheet
├── tests/                # Test files
│   ├── __init__.py       # Test package initialization
│   └── test_main.py      # Main functionality tests
├── Archive/              # Legacy and backup files
├── create_drafts.py      # Original automation script (legacy)
├── create_drafts_enhanced.py  # Enhanced version (current)
├── manage_templates.py   # Template management utility
├── email_templates.json  # Email template configurations
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── CLAUDE.md           # AI guidance (this file)
```

### Tech Stack & Structure
- **Backend**: Python with pandas, pywin32, openpyxl
- **Frontend**: HTML/CSS templates for future web interface
- **Data**: Excel files for customer information
- **Integration**: Microsoft Outlook automation
- **Testing**: Python unittest framework (structure ready)

### Development Guidelines
- Main scripts are currently in root directory (legacy structure)
- Future development should utilize the `src/` directory for modular code
- HTML templates in `templates/` for any web interface development
- Static assets in `static/` for CSS, JavaScript, images
- Tests in `tests/` directory following Python testing conventions
- Use `requirements.txt` for dependency management

## Important Notes
- Excel file must be closed before running scripts
- Outlook must be installed, configured, and signed in
- PDF files must exist at the exact paths specified in Excel (FilePath + FileName)
- Headers are on row 4 of Excel (row 3 when 0-indexed in pandas)
- Script creates drafts only - manual review and sending required
- Enhanced version requires python-dateutil package
- Original functionality preserved in create_drafts.py for backward compatibility

## AI Guidance
This file is used by Claude Code to understand the project structure and provide appropriate development assistance. The project is transitioning from a script-based approach to a more structured Python package layout for better maintainability and testing.