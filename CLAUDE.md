# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose
This codebase automates the creation of Outlook email drafts for sending monthly customer price sheets. It reads customer data from an Excel workbook and creates personalized drafts with PDF attachments.

## Key Commands

### Running the main script
```bash
python create_drafts.py
```

### Diagnostic and utility scripts
```bash
python check_columns.py     # Verify Excel column names
python diagnose_excel.py    # Detailed Excel structure analysis
```

### Installing dependencies
```bash
pip install pandas pywin32 openpyxl
```

## Architecture

### Core Components
- **create_drafts.py**: Main script that connects to Outlook via win32com, reads customer data from Excel (header on row 3), and creates draft emails with HTML formatting and PDF attachments
- **Python_CustomerPricing.xlsx**: Source Excel file containing customer data with headers on row 4 (0-indexed row 3)
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

## Important Notes
- Excel file must be closed before running scripts
- Outlook must be installed, configured, and signed in
- PDF files must exist at the exact paths specified in Excel (FilePath + FileName)
- Headers are on row 4 of Excel (row 3 when 0-indexed in pandas)
- Script creates drafts only - manual review and sending required