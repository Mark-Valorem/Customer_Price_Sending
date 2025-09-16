"""
Email generation module for creating Outlook drafts without terminal I/O.
All functions return data instead of printing to console.
"""

import win32com.client
import pythoncom
import pandas as pd
import os
import json
import logging
import traceback
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

# Set up logging
log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, f'email_generation_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log')

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(funcName)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()  # Also log to console for debugging
    ]
)

logger = logging.getLogger(__name__)


def load_email_templates():
    """Load email templates from JSON file"""
    templates_data = {}

    try:
        # Load main templates
        templates_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'email_templates.json')
        with open(templates_file, 'r', encoding='utf-8') as f:
            templates_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        templates_data = create_default_template()

    # Check for dashboard template
    dashboard_template_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'monthly_drafts',
        'dashboard_template.json'
    )

    if os.path.exists(dashboard_template_file):
        try:
            with open(dashboard_template_file, 'r', encoding='utf-8') as f:
                dashboard_data = json.load(f)
                # Merge dashboard templates with existing templates
                if 'templates' not in templates_data:
                    templates_data['templates'] = {}
                templates_data['templates'].update(dashboard_data.get('templates', {}))
        except (json.JSONDecodeError, Exception):
            pass  # Silently ignore errors loading dashboard template

    return templates_data


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


def get_available_templates(templates_data):
    """Get list of available templates"""
    templates = templates_data.get('templates', {})
    return [
        {
            'key': key,
            'name': template.get('name', key.title()),
            'subject': template.get('subject', 'N/A')
        }
        for key, template in templates.items()
    ]


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


def create_email_drafts_batch(template_key=None, custom_values=None, progress_callback=None):
    """
    Creates draft emails in Outlook for all customers.

    Args:
        template_key: Key of the template to use (default: 'dashboard_custom' or 'default')
        custom_values: Dictionary of placeholder values
        progress_callback: Function to call with progress updates (current, total, message)

    Returns:
        Dictionary with results:
        - success: True if successful
        - drafts_created: Number of drafts created
        - errors: List of error messages
        - details: List of draft details
        - debug_log: Path to debug log file
    """

    results = {
        'success': False,
        'drafts_created': 0,
        'errors': [],
        'details': [],
        'debug_log': log_file
    }

    logger.info("="*60)
    logger.info("Starting email draft generation")
    logger.info(f"Template key: {template_key}")
    logger.info(f"Custom values provided: {bool(custom_values)}")

    # Initialize COM for this thread
    com_initialized = False

    try:
        logger.debug("Initializing COM for thread...")
        pythoncom.CoInitialize()
        com_initialized = True
        logger.info("COM initialized successfully")
        # Load templates
        templates_data = load_email_templates()

        # Select template
        if template_key and template_key in templates_data.get('templates', {}):
            selected_template = templates_data['templates'][template_key]
        elif 'dashboard_custom' in templates_data.get('templates', {}):
            selected_template = templates_data['templates']['dashboard_custom']
            template_key = 'dashboard_custom'
        else:
            selected_template = templates_data['templates'].get('default', create_default_template()['templates']['default'])
            template_key = 'default'

        # Get signature
        signature = templates_data.get('signature', create_default_template()['signature'])

        # Prepare custom values
        if custom_values is None:
            custom_values = get_date_placeholders()
        else:
            # Merge with date placeholders
            date_values = get_date_placeholders()
            custom_values = {**date_values, **custom_values}

        # Connect to Outlook
        if progress_callback:
            progress_callback(0, 100, "Connecting to Outlook...")

        logger.debug("Attempting to connect to Outlook...")
        try:
            outlook = win32com.client.Dispatch("Outlook.Application")
            logger.info("Successfully connected to Outlook")
        except Exception as outlook_error:
            logger.error(f"Failed to connect to Outlook: {str(outlook_error)}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            error_msg = (
                f"Failed to connect to Outlook: {str(outlook_error)}\n\n"
                "Please ensure:\n"
                "1. Microsoft Outlook is installed\n"
                "2. Outlook is configured with an email account\n"
                "3. Outlook is not running in Administrator mode\n"
                f"\n\nDebug log: {log_file}"
            )
            results['errors'].append(error_msg)
            raise Exception(error_msg)

        # Read customer data from Excel
        excel_file = r"C:\Users\MarkAnderson\Valorem\Knowledge Hub - Documents\Pricing\Customer Price Lists\Price Sheet Sending_Python\Python_CustomerPricing.xlsx"

        if progress_callback:
            progress_callback(10, 100, "Reading customer data...")

        # Read the Excel file - headers are on row 3 (0-indexed)
        logger.debug(f"Reading Excel file: {excel_file}")
        if not os.path.exists(excel_file):
            error_msg = f"Excel file not found: {excel_file}"
            logger.error(error_msg)
            results['errors'].append(error_msg)
            raise FileNotFoundError(error_msg)

        df = pd.read_excel(excel_file, header=3)
        logger.info(f"Successfully read Excel file with {len(df)} rows")

        # Clean column names
        df.columns = df.columns.str.strip()
        logger.debug(f"Column names: {list(df.columns)}")

        total_customers = len(df)
        logger.info(f"Processing {total_customers} customers")

        # Create a draft for each customer
        for index, row in df.iterrows():
            try:
                # Update progress
                if progress_callback:
                    progress = 10 + int((index / total_customers) * 85)
                    progress_callback(progress, 100, f"Creating draft for {row['CustomerName']}...")

                # Create a new email draft
                mail = outlook.CreateItem(0)  # 0 = Mail item

                # Set the recipients
                mail.To = row['EmailAddresses']

                # Set CC
                mail.CC = "support@valorem.com.au;jasonn@valorem.com.au"

                # Set the subject using template
                subject_values = custom_values.copy()
                subject_values['customer_name'] = row['CustomerName']
                mail.Subject = selected_template.get('subject', 'Monthly Pricing Update for {customer_name}').format(**subject_values)

                # Create the HTML body using template
                mail.HTMLBody = build_html_email_body(
                    selected_template,
                    signature,
                    custom_values,
                    row['CustomerName'],
                    row['RecipientName']
                )

                # Attach the local file
                folder = row.get('FilePath', '').strip()
                filename = row.get('FileName', '').strip()
                attached_file = "No file specified"

                if folder and filename:
                    fullpath = os.path.join(folder, filename)
                    if os.path.exists(fullpath):
                        mail.Attachments.Add(fullpath)
                        attached_file = filename
                    else:
                        attached_file = f"{filename} (NOT FOUND)"
                        results['errors'].append(f"File not found for {row['CustomerName']}: {fullpath}")

                # Save as draft
                mail.Save()

                # Record success
                results['details'].append({
                    'customer': row['CustomerName'],
                    'email': row['EmailAddresses'],
                    'attachment': attached_file,
                    'status': 'success'
                })
                results['drafts_created'] += 1
                logger.debug(f"Successfully created draft for {row['CustomerName']}")

            except Exception as e:
                # Record error
                customer_name = row.get('CustomerName', 'Unknown')
                error_msg = f"Error creating draft for {customer_name}: {str(e)}"
                logger.error(error_msg)
                logger.error(f"Row data: {row.to_dict()}")
                logger.error(f"Traceback: {traceback.format_exc()}")

                results['errors'].append(error_msg)
                results['details'].append({
                    'customer': customer_name,
                    'email': row.get('EmailAddresses', 'N/A'),
                    'attachment': 'N/A',
                    'status': 'error',
                    'error': str(e)
                })

        # Final progress update
        if progress_callback:
            progress_callback(100, 100, "Complete!")

        results['success'] = True

    except Exception as e:
        logger.error(f"Critical error during email generation: {str(e)}")
        logger.error(f"Full traceback:\n{traceback.format_exc()}")

        # Add user-friendly error message
        if "CoInitialize" in str(e):
            error_msg = (
                "COM initialization error. This is a threading issue.\n"
                "The error has been logged for debugging.\n"
                f"Debug log: {log_file}"
            )
        elif "Outlook" in str(e):
            error_msg = (
                f"Outlook connection error: {str(e)}\n\n"
                "Please check that Outlook is properly installed and configured.\n"
                f"Debug log: {log_file}"
            )
        else:
            error_msg = f"Critical error: {str(e)}\n\nDebug log: {log_file}"

        results['errors'].append(error_msg)
        results['success'] = False

    finally:
        # Clean up COM
        if com_initialized:
            try:
                logger.debug("Uninitializing COM...")
                pythoncom.CoUninitialize()
                logger.info("COM uninitialized successfully")
            except Exception as cleanup_error:
                logger.error(f"Error during COM cleanup: {str(cleanup_error)}")

    logger.info(f"Email generation completed. Success: {results['success']}, Drafts created: {results['drafts_created']}")
    logger.info("="*60)

    return results


def create_single_draft_preview(template_key, custom_values=None):
    """
    Create a preview of an email for a sample customer.

    Args:
        template_key: Key of the template to use
        custom_values: Dictionary of placeholder values

    Returns:
        Dictionary with preview details
    """

    # Load templates
    templates_data = load_email_templates()

    # Get template
    if template_key in templates_data.get('templates', {}):
        template = templates_data['templates'][template_key]
    else:
        template = create_default_template()['templates']['default']

    # Get signature
    signature = templates_data.get('signature', create_default_template()['signature'])

    # Prepare custom values
    if custom_values is None:
        custom_values = get_date_placeholders()

    # Sample customer data
    sample_customer = "ABC Company Pty Ltd"
    sample_recipient = "John Smith"

    # Generate subject
    subject_values = custom_values.copy()
    subject_values['customer_name'] = sample_customer
    subject = template.get('subject', 'Monthly Pricing Update for {customer_name}').format(**subject_values)

    # Generate HTML body
    html_body = build_html_email_body(
        template,
        signature,
        custom_values,
        sample_customer,
        sample_recipient
    )

    # Convert HTML to plain text for preview
    import re
    plain_body = re.sub(r'<[^>]+>', '', html_body)
    plain_body = re.sub(r'\n\s*\n', '\n\n', plain_body.strip())

    return {
        'subject': subject,
        'html_body': html_body,
        'plain_body': plain_body,
        'customer': sample_customer,
        'recipient': sample_recipient
    }