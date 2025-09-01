create_drafts.py

Overview
create_drafts.py reads your customer-pricing Excel workbook and builds an Outlook draft for each account, complete with your HTML signature and the correct PDF attachment. Drafts are saved for review before sending.

Features
- Connects to your local Outlook application
- Reads customer data (To, CC, BCC, subject, recipient name, file path and file name) from an Excel workbook
- Builds and saves each message as a draft
- Attaches the correct PDF from your local drive, verifying that the file exists
- Logs progress and any missing-file warnings to the console

Prerequisites
- Windows PC with Outlook installed and configured
- Python 3.7 or later
- A local (OneDrive-synced) copy of your SharePoint files

Installation
Run on the command line:
pip install pandas pywin32

Configuration
1. Place your Excel workbook at:
   C:\Users\MarkAnderson\Valorem\Knowledge Hub - Documents\Pricing\Customer Price Lists\Price Sheet Sending_Python\Python_CustomerPricing.xlsx
2. In row 4 of that sheet, ensure you have columns named exactly:
   EmailAddresses, CustomerName, RecipientName, FilePath, FileName

Usage
1. Close the Excel file so Python can open it
2. Open a command prompt in the script folder
3. Run:
   python create_drafts.py
4. Watch the console for ‘draft created’ messages and ‘file not found’ warnings
5. Open Outlook’s Drafts folder, review your messages and send when ready

Troubleshooting
- Permission denied: close the workbook in Excel or check folder permissions
- Missing-file warnings: check that FilePath plus FileName resolves to an existing file
- Outlook issues: ensure Outlook has been opened and signed in before running the script

Support
Contact your internal IT team or email support@valorem.com.au
