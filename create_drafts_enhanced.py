import win32com.client
import pandas as pd
import os
import json
import sys
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

def load_email_templates():
    """Load email templates from JSON file"""
    try:
        templates_file = os.path.join(os.path.dirname(__file__), 'email_templates.json')
        with open(templates_file, 'r', encoding='utf-8') as f:
            templates_data = json.load(f)

        # Check for dashboard template
        dashboard_template_file = os.path.join(os.path.dirname(__file__), 'monthly_drafts', 'dashboard_template.json')
        if os.path.exists(dashboard_template_file):
            try:
                with open(dashboard_template_file, 'r', encoding='utf-8') as f:
                    dashboard_data = json.load(f)
                    # Merge dashboard templates with existing templates
                    templates_data['templates'].update(dashboard_data.get('templates', {}))
                    print("✓ Dashboard template loaded")
            except Exception as e:
                print(f"⚠ Error loading dashboard template: {e}")

        return templates_data
    except FileNotFoundError:
        print("⚠ email_templates.json not found. Using default template.")
        return create_default_template()
    except json.JSONDecodeError as e:
        print(f"⚠ Error reading email_templates.json: {e}. Using default template.")
        return create_default_template()

def create_default_template():
    """Create a default template if JSON file is missing"""
    return {
        "templates": {
            "default": {
                "name": "Standard Monthly Update",
                "subject": "Monthly Pricing Update for {customer_name}",
                "body": {
                    "greeting": "Hi {recipient_name},",
                    "main_message": "Just a quick note to share the updated pricing for your account - attached for reference.",
                    "pricing_note": "No change in pricing for {month}, as FX movement stayed within the 2% band.",
                    "closing": "Thanks,"
                }
            }
        },
        "signature": {
            "name": "Mark Anderson",
            "title": "Managing Director", 
            "company": "Valorem Chemicals Pty Ltd",
            "phone": "+61 417 725 006",
            "email": "marka@valorem.com.au",
            "website": "www.valorem.com.au",
            "company_color": "rgb(74, 144, 226)"
        }
    }

def get_date_placeholders():
    """Generate date-based placeholder values"""
    today = date.today()
    current_month = today.strftime("%B")
    previous_month = (today.replace(day=1) - relativedelta(months=1)).strftime("%B")
    first_of_next_month = (today.replace(day=1) + relativedelta(months=1)).strftime("%B 1, %Y")
    
    # Calculate end of quarter
    quarter = (today.month - 1) // 3 + 1
    end_of_quarter_month = quarter * 3
    end_of_quarter = date(today.year, end_of_quarter_month, 1) + relativedelta(months=1, days=-1)
    
    return {
        "current_month": current_month,
        "previous_month": previous_month,
        "first_of_next_month": first_of_next_month,
        "end_of_quarter": end_of_quarter.strftime("%B %d, %Y"),
        "month": current_month
    }

def display_available_templates(templates_data):
    """Display all available templates for user selection"""
    print("\n" + "="*60)
    print("AVAILABLE EMAIL TEMPLATES")
    print("="*60)
    
    templates = templates_data.get('templates', {})
    for i, (key, template) in enumerate(templates.items(), 1):
        print(f"{i}. {template.get('name', key.title())}")
        print(f"   Subject: {template.get('subject', 'N/A')}")
        print(f"   Key: {key}")
        print()
    
    return list(templates.keys())

def get_template_selection(available_templates, templates_data):
    """Get user's template selection"""
    while True:
        try:
            print("Select a template by number, or press Enter for default (1):")
            choice = input("Choice: ").strip()
            
            if not choice:
                choice = "1"
            
            choice_num = int(choice)
            if 1 <= choice_num <= len(available_templates):
                selected_key = available_templates[choice_num - 1]
                selected_template = templates_data['templates'][selected_key]
                print(f"\n✓ Selected: {selected_template.get('name', selected_key.title())}")
                return selected_key, selected_template
            else:
                print(f"Please enter a number between 1 and {len(available_templates)}")
                
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            sys.exit(0)

def customize_template_values(template, templates_data):
    """Allow user to customize template placeholder values"""
    print("\n" + "="*60)
    print("CUSTOMIZE TEMPLATE VALUES")
    print("="*60)
    
    # Get default date values
    date_values = get_date_placeholders()
    default_values = templates_data.get('default_values', {})
    
    # Merge date values with defaults
    custom_values = {**date_values, **default_values}
    
    # Find placeholders in the template
    template_str = json.dumps(template)
    placeholders = []
    import re
    placeholder_pattern = r'\{([^}]+)\}'
    found_placeholders = set(re.findall(placeholder_pattern, template_str))
    
    # Remove standard placeholders that come from Excel data
    excel_placeholders = {'customer_name', 'recipient_name'}
    customizable_placeholders = found_placeholders - excel_placeholders
    
    print("Current values (press Enter to keep current value):")
    print("-" * 60)
    
    for placeholder in sorted(customizable_placeholders):
        current_value = custom_values.get(placeholder, f"{{placeholder}}")
        print(f"\n{placeholder}: {current_value}")
        new_value = input(f"New value for {placeholder}: ").strip()
        if new_value:
            custom_values[placeholder] = new_value
    
    return custom_values

def build_html_email_body(template, signature, custom_values, customer_name, recipient_name):
    """Build the HTML email body from template"""

    # Prepare all values for substitution
    all_values = custom_values.copy()
    all_values.update({
        'customer_name': customer_name,
        'recipient_name': recipient_name
    })

    # Get template body parts
    body = template.get('body', {})

    # Check if this is a dashboard template (has single 'content' field)
    if 'content' in body:
        # Dashboard template - format the entire content
        content_html = body.get('content', '').format(**all_values)
        # Convert line breaks to HTML
        content_html = content_html.replace('\n', '<br>')
        body_content = f"<p>{content_html}</p>"
    else:
        # Standard template - use structured fields
        greeting = body.get('greeting', 'Hi {recipient_name},').format(**all_values)
        main_message = body.get('main_message', '').format(**all_values)
        pricing_note = body.get('pricing_note', '').format(**all_values)
        closing = body.get('closing', 'Thanks,').format(**all_values)

        body_content = f"""
            <p>{greeting}</p>

            <p>{main_message}</p>

            <p>{pricing_note}</p>

            <p>{closing}</p>
        """

    # Build signature
    sig_html = f"""
    <p>
        <strong>{signature.get('name', 'Mark Anderson')}</strong><br>
        {signature.get('title', 'Managing Director')}<br>
        <strong style="color: {signature.get('company_color', 'rgb(74, 144, 226)')};">{signature.get('company', 'Valorem Chemicals Pty Ltd')}</strong><br>
        Phone: {signature.get('phone', '+61 417 725 006')}<br>
        Email: {signature.get('email', 'marka@valorem.com.au')}<br>
        Web: {signature.get('website', 'www.valorem.com.au')}
    </p>
    """

    # Combine into full HTML
    html_body = f"""
    <html>
        <body style="font-family: Arial, sans-serif;">
            {body_content}

            {sig_html}

            <p style="font-size: 10px;">
                This email and any files transmitted with it are confidential and
                intended solely for the use of the individual or entity to whom they are addressed.
            </p>
        </body>
    </html>
    """

    return html_body

def create_email_drafts():
    """
    Creates draft emails in Outlook with customizable templates.
    This enhanced version allows monthly customization of email content.
    """
    
    print("="*70)
    print("ENHANCED EMAIL DRAFT CREATOR WITH TEMPLATES")
    print("="*70)
    
    # Load templates
    templates_data = load_email_templates()
    
    # Display templates and get selection
    available_templates = display_available_templates(templates_data)
    template_key, selected_template = get_template_selection(available_templates, templates_data)
    
    # Customize template values
    custom_values = customize_template_values(selected_template, templates_data)
    
    # Show preview
    print("\n" + "="*60)
    print("TEMPLATE PREVIEW")
    print("="*60)
    
    preview_subject = selected_template.get('subject', '').format(
        customer_name="[CUSTOMER NAME]", **custom_values
    )
    print(f"Subject: {preview_subject}")
    
    preview_html = build_html_email_body(
        selected_template, 
        templates_data.get('signature', {}),
        custom_values,
        "[CUSTOMER NAME]",
        "[RECIPIENT NAME]"
    )
    
    # Convert HTML to text for preview
    import re
    preview_text = re.sub(r'<[^>]+>', '', preview_html)
    preview_text = re.sub(r'\n\s*\n', '\n\n', preview_text.strip())
    print(f"\nBody Preview:\n{preview_text}")
    
    print("\n" + "="*60)
    confirm = input("Proceed with creating drafts using this template? (y/N): ").strip().lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return
    
    # Step 1: Connect to Outlook
    print("\n" + "="*60)
    print("CREATING EMAIL DRAFTS")
    print("="*60)
    print("Connecting to Outlook...")
    outlook = win32com.client.Dispatch("Outlook.Application")
    
    # Step 2: Read customer data from Excel
    excel_file = r"C:\Users\MarkAnderson\Valorem\Knowledge Hub - Documents\Pricing\Customer Price Lists\Price Sheet Sending_Python\Python_CustomerPricing.xlsx"
    print(f"Reading customer data from {excel_file}")
    
    # Read the Excel file - the headers are on row 3 (0-indexed)
    df = pd.read_excel(excel_file, header=3)

    # Clean column names (remove any trailing spaces)
    df.columns = df.columns.str.strip()

    # Show what columns we found
    print(f"Found columns: {', '.join(df.columns)}")
    print(f"Found {len(df)} customer records\n")

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
            
            # Set the subject using template
            subject_values = custom_values.copy()
            subject_values['customer_name'] = row['CustomerName']
            mail.Subject = selected_template.get('subject', 'Monthly Pricing Update for {customer_name}').format(**subject_values)
            
            # Create the HTML body using template
            mail.HTMLBody = build_html_email_body(
                selected_template,
                templates_data.get('signature', {}),
                custom_values,
                row['CustomerName'],
                row['RecipientName']
            )
            
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
    
    print(f"\nCompleted! Created {drafts_created} draft emails using '{selected_template.get('name', template_key)}' template.")
    print("Check your Outlook Drafts folder to review before sending.")

# Run the script
if __name__ == "__main__":
    try:
        create_email_drafts()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        input("Press Enter to exit...")