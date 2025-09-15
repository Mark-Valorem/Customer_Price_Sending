import win32com.client
import pandas as pd
import os
from datetime import datetime

def create_email_drafts():
    """
    Creates draft emails in Outlook with proper HTML formatting and attachments.
    This script reads customer data from Excel and creates a draft for each customer.
    """
    
    # Step 1: Connect to Outlook
    # This creates a connection to your local Outlook application
    print("Connecting to Outlook...")
    outlook = win32com.client.Dispatch("Outlook.Application")
    
    # Step 2: Read customer data from Excel
    # Adjust this path to where your Excel file is located
    excel_file = r"C:\Users\MarkAnderson\Valorem\Knowledge Hub - Documents\Pricing\Customer Price Lists\Price Sheet Sending_Python\Python_CustomerPricing.xlsx"
    print(f"Reading customer data from {excel_file}")
    
    # Read the Excel file - the headers are on row 3 (0-indexed)
    df = pd.read_excel(excel_file, header=3)

    # Clean column names (remove any trailing spaces)
    df.columns = df.columns.str.strip()

    # Show what columns we found
    print(f"Found columns: {', '.join(df.columns)}")
    print(f"Found {len(df)} customer records\n")

    # DEBUG: Show the first few rows to see what we're actually reading
    print("=== DEBUGGING: First customer's data ===")
    first_row = df.iloc[0]
    print(f"Customer Name: {first_row.get('CustomerName', 'NOT FOUND')}")
    print(f"File Path: {first_row.get('FilePath', 'NOT FOUND')}")
    print(f"File Name: {first_row.get('FileName', 'NOT FOUND')}")
    print(f"Email: {first_row.get('EmailAddresses', 'NOT FOUND')}")
    print("=== All columns and their values for first row ===")
    for col in df.columns:
        print(f"{col}: {first_row[col]}")
    print("=====================================\n")
    
    # Step 3: Create a draft for each customer
    drafts_created = 0
    
    for index, row in df.iterrows():
        try:
            # Create a new email draft
            mail = outlook.CreateItem(0)  # 0 = Mail item
            
            # Set the recipients
            mail.To = row['EmailAddresses']
            
            # Set CC and BCC if needed
            mail.CC = "support@valorem.com.au;jasonn@valorem.com.au"
            
            # Set the subject
            mail.Subject = f"Monthly Pricing Update for {row['CustomerName']}"
            
            # Create the HTML body with proper formatting
            mail.HTMLBody = f"""
            <html>
                <body style="font-family: Arial, sans-serif;">
                    <p>Hi {row['RecipientName']},</p>
                    
                    <p>Just a quick note to share the updated pricing for your account - attached for reference.</p>
                    
                    <p>No change in pricing for September, as FX movement stayed within the 2% band.</p>
                    
                    <p>Thanks,</p>
                    
                    <p>
                        <strong>Mark Anderson</strong><br>
                        Managing Director<br>
                        <strong style="color: rgb(74, 144, 226);">Valorem Chemicals Pty Ltd</strong><br>
                        Phone: +61 417 725 006<br>
                        Email: marka@valorem.com.au<br>
                        Web: www.valorem.com.au
                    </p>
                    
                    <p style="font-size: 10px;">
                        This email and any files transmitted with it are confidential and 
                        intended solely for the use of the individual or entity to whom they are addressed.
                    </p>
                </body>
            </html>
            """
            
            # Attach the local file (FilePath = folder, FileName = filename)
            folder   = row.get('FilePath', '').strip()
            filename = row.get('FileName', '').strip()
            if folder and filename:
                fullpath = os.path.join(folder, filename)
                if os.path.exists(fullpath):
                    mail.Attachments.Add(fullpath)
                else:
                    print(f"⚠ File not found for {row['CustomerName']}: {fullpath}")
            
            # Save as draft (not send)
            mail.Save()
            
            # Show what file was attached (or attempted to be attached)
            attached_file = "No file specified"
            if folder and filename:
                attached_file = filename
                if not os.path.exists(os.path.join(folder, filename)):
                    attached_file = f"{filename} (FILE NOT FOUND!)"

            print(f"✓ Created draft for {row['CustomerName']} ({row['EmailAddresses']}) - Attached: {attached_file}")
            drafts_created += 1
            
        except Exception as e:
            print(f"✗ Error creating draft for {row['CustomerName']}: {str(e)}")
    
    print(f"\nCompleted! Created {drafts_created} draft emails.")
    print("Check your Outlook Drafts folder to review before sending.")

# Run the script
if __name__ == "__main__":
    create_email_drafts()
