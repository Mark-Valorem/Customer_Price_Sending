import json
import os
import sys
from datetime import datetime

def load_templates():
    """Load templates from JSON file"""
    templates_file = os.path.join(os.path.dirname(__file__), 'email_templates.json')
    try:
        with open(templates_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Templates file not found: {templates_file}")
        return create_blank_template_structure()
    except json.JSONDecodeError as e:
        print(f"Error reading templates file: {e}")
        return None

def save_templates(templates_data):
    """Save templates to JSON file"""
    templates_file = os.path.join(os.path.dirname(__file__), 'email_templates.json')
    try:
        # Create backup
        if os.path.exists(templates_file):
            backup_file = f"{templates_file}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.rename(templates_file, backup_file)
            print(f"Backup created: {os.path.basename(backup_file)}")
        
        with open(templates_file, 'w', encoding='utf-8') as f:
            json.dump(templates_data, f, indent=2, ensure_ascii=False)
        print(f"Templates saved successfully to {os.path.basename(templates_file)}")
        return True
    except Exception as e:
        print(f"Error saving templates: {e}")
        return False

def create_blank_template_structure():
    """Create a blank template structure"""
    return {
        "templates": {},
        "signature": {
            "name": "Mark Anderson",
            "title": "Managing Director",
            "company": "Valorem Chemicals Pty Ltd",
            "phone": "+61 417 725 006",
            "email": "marka@valorem.com.au",
            "website": "www.valorem.com.au",
            "company_color": "rgb(74, 144, 226)"
        },
        "default_values": {},
        "placeholders": {}
    }

def display_main_menu():
    """Display the main menu"""
    print("\n" + "="*70)
    print("EMAIL TEMPLATE MANAGER")
    print("="*70)
    print("1. View all templates")
    print("2. Create new template")
    print("3. Edit existing template")
    print("4. Delete template")
    print("5. Edit signature")
    print("6. Manage default values")
    print("7. Export templates to file")
    print("8. Import templates from file")
    print("9. Preview template")
    print("0. Exit")
    print("-" * 70)

def view_all_templates(templates_data):
    """Display all templates"""
    templates = templates_data.get('templates', {})
    if not templates:
        print("\nNo templates found.")
        return
    
    print("\n" + "="*60)
    print("ALL TEMPLATES")
    print("="*60)
    
    for key, template in templates.items():
        print(f"\nTemplate Key: {key}")
        print(f"Name: {template.get('name', 'N/A')}")
        print(f"Subject: {template.get('subject', 'N/A')}")
        
        body = template.get('body', {})
        print(f"Greeting: {body.get('greeting', 'N/A')}")
        print(f"Main Message: {body.get('main_message', 'N/A')[:80]}{'...' if len(body.get('main_message', '')) > 80 else ''}")
        print(f"Pricing Note: {body.get('pricing_note', 'N/A')[:80]}{'...' if len(body.get('pricing_note', '')) > 80 else ''}")
        print(f"Closing: {body.get('closing', 'N/A')}")
        print("-" * 60)

def create_new_template(templates_data):
    """Create a new template interactively"""
    print("\n" + "="*60)
    print("CREATE NEW TEMPLATE")
    print("="*60)
    
    # Get template key
    while True:
        key = input("Template key (lowercase, no spaces): ").strip().lower().replace(' ', '_')
        if not key:
            print("Template key cannot be empty.")
            continue
        if key in templates_data.get('templates', {}):
            overwrite = input(f"Template '{key}' already exists. Overwrite? (y/N): ").strip().lower()
            if overwrite != 'y':
                continue
        break
    
    # Get template details
    name = input("Template name (display name): ").strip() or key.title()
    subject = input("Subject line (use {customer_name} for customer): ").strip()
    
    print("\nEmail body components:")
    greeting = input("Greeting (use {recipient_name} for recipient): ").strip()
    main_message = input("Main message: ").strip()
    pricing_note = input("Pricing/update note: ").strip()
    closing = input("Closing: ").strip()
    
    # Create template structure
    new_template = {
        "name": name,
        "subject": subject,
        "body": {
            "greeting": greeting,
            "main_message": main_message,
            "pricing_note": pricing_note,
            "closing": closing
        }
    }
    
    # Add to templates
    if 'templates' not in templates_data:
        templates_data['templates'] = {}
    
    templates_data['templates'][key] = new_template
    
    print(f"\n✓ Template '{name}' created successfully with key '{key}'")
    return templates_data

def edit_template(templates_data):
    """Edit an existing template"""
    templates = templates_data.get('templates', {})
    if not templates:
        print("\nNo templates available to edit.")
        return templates_data
    
    print("\n" + "="*60)
    print("EDIT TEMPLATE")
    print("="*60)
    
    # Show available templates
    print("Available templates:")
    for i, (key, template) in enumerate(templates.items(), 1):
        print(f"{i}. {template.get('name', key)} (key: {key})")
    
    # Get selection
    try:
        choice = input(f"\nSelect template to edit (1-{len(templates)}): ").strip()
        if not choice:
            return templates_data
        
        choice_num = int(choice)
        if not (1 <= choice_num <= len(templates)):
            print("Invalid selection.")
            return templates_data
        
        selected_key = list(templates.keys())[choice_num - 1]
        selected_template = templates[selected_key]
        
    except ValueError:
        print("Please enter a valid number.")
        return templates_data
    
    print(f"\nEditing template: {selected_template.get('name', selected_key)}")
    print("(Press Enter to keep current value)")
    
    # Edit fields
    current_name = selected_template.get('name', '')
    new_name = input(f"Name [{current_name}]: ").strip()
    if new_name:
        selected_template['name'] = new_name
    
    current_subject = selected_template.get('subject', '')
    new_subject = input(f"Subject [{current_subject}]: ").strip()
    if new_subject:
        selected_template['subject'] = new_subject
    
    # Edit body components
    body = selected_template.get('body', {})
    
    for field in ['greeting', 'main_message', 'pricing_note', 'closing']:
        current_value = body.get(field, '')
        new_value = input(f"{field.replace('_', ' ').title()} [{current_value}]: ").strip()
        if new_value:
            body[field] = new_value
    
    selected_template['body'] = body
    print(f"\n✓ Template '{selected_template.get('name', selected_key)}' updated successfully")
    return templates_data

def delete_template(templates_data):
    """Delete a template"""
    templates = templates_data.get('templates', {})
    if not templates:
        print("\nNo templates available to delete.")
        return templates_data
    
    print("\n" + "="*60)
    print("DELETE TEMPLATE")
    print("="*60)
    
    # Show available templates
    print("Available templates:")
    for i, (key, template) in enumerate(templates.items(), 1):
        print(f"{i}. {template.get('name', key)} (key: {key})")
    
    # Get selection
    try:
        choice = input(f"\nSelect template to delete (1-{len(templates)}): ").strip()
        if not choice:
            return templates_data
        
        choice_num = int(choice)
        if not (1 <= choice_num <= len(templates)):
            print("Invalid selection.")
            return templates_data
        
        selected_key = list(templates.keys())[choice_num - 1]
        selected_template = templates[selected_key]
        
        # Confirm deletion
        confirm = input(f"Are you sure you want to delete '{selected_template.get('name', selected_key)}'? (y/N): ").strip().lower()
        if confirm == 'y':
            del templates_data['templates'][selected_key]
            print(f"✓ Template '{selected_template.get('name', selected_key)}' deleted successfully")
        else:
            print("Deletion cancelled.")
            
    except ValueError:
        print("Please enter a valid number.")
    
    return templates_data

def edit_signature(templates_data):
    """Edit the email signature"""
    print("\n" + "="*60)
    print("EDIT SIGNATURE")
    print("="*60)
    
    signature = templates_data.get('signature', {})
    
    print("Current signature settings (press Enter to keep current value):")
    
    fields = [
        ('name', 'Full Name'),
        ('title', 'Job Title'),
        ('company', 'Company Name'),
        ('phone', 'Phone Number'),
        ('email', 'Email Address'),
        ('website', 'Website'),
        ('company_color', 'Company Color (CSS format)')
    ]
    
    for field, display_name in fields:
        current_value = signature.get(field, '')
        new_value = input(f"{display_name} [{current_value}]: ").strip()
        if new_value:
            signature[field] = new_value
    
    templates_data['signature'] = signature
    print("✓ Signature updated successfully")
    return templates_data

def preview_template(templates_data):
    """Preview a template with sample data"""
    templates = templates_data.get('templates', {})
    if not templates:
        print("\nNo templates available to preview.")
        return
    
    print("\n" + "="*60)
    print("PREVIEW TEMPLATE")
    print("="*60)
    
    # Show available templates
    print("Available templates:")
    for i, (key, template) in enumerate(templates.items(), 1):
        print(f"{i}. {template.get('name', key)} (key: {key})")
    
    # Get selection
    try:
        choice = input(f"\nSelect template to preview (1-{len(templates)}): ").strip()
        if not choice:
            return
        
        choice_num = int(choice)
        if not (1 <= choice_num <= len(templates)):
            print("Invalid selection.")
            return
        
        selected_key = list(templates.keys())[choice_num - 1]
        selected_template = templates[selected_key]
        
    except ValueError:
        print("Please enter a valid number.")
        return
    
    # Sample data
    sample_data = {
        'customer_name': 'ABC Corporation',
        'recipient_name': 'John Smith',
        'current_month': 'October',
        'previous_month': 'September',
        'month': 'October'
    }
    
    print("\n" + "="*60)
    print(f"PREVIEW: {selected_template.get('name', selected_key)}")
    print("="*60)
    
    # Preview subject
    subject = selected_template.get('subject', '').format(**sample_data)
    print(f"Subject: {subject}")
    
    # Preview body
    body = selected_template.get('body', {})
    print(f"\nBody:")
    print("-" * 40)
    
    for field in ['greeting', 'main_message', 'pricing_note', 'closing']:
        content = body.get(field, '').format(**sample_data)
        if content:
            print(content)
            print()
    
    # Preview signature
    signature = templates_data.get('signature', {})
    print(f"{signature.get('name', 'Mark Anderson')}")
    print(f"{signature.get('title', 'Managing Director')}")
    print(f"{signature.get('company', 'Valorem Chemicals Pty Ltd')}")
    print(f"Phone: {signature.get('phone', '+61 417 725 006')}")
    print(f"Email: {signature.get('email', 'marka@valorem.com.au')}")
    print(f"Web: {signature.get('website', 'www.valorem.com.au')}")

def main():
    """Main program loop"""
    print("Loading templates...")
    templates_data = load_templates()
    
    if templates_data is None:
        print("Failed to load templates. Exiting.")
        return
    
    while True:
        display_main_menu()
        
        try:
            choice = input("Select an option (0-9): ").strip()
            
            if choice == '0':
                print("Goodbye!")
                break
            elif choice == '1':
                view_all_templates(templates_data)
            elif choice == '2':
                templates_data = create_new_template(templates_data)
            elif choice == '3':
                templates_data = edit_template(templates_data)
            elif choice == '4':
                templates_data = delete_template(templates_data)
            elif choice == '5':
                templates_data = edit_signature(templates_data)
            elif choice == '6':
                print("Default values management - Coming soon!")
            elif choice == '7':
                print("Export functionality - Coming soon!")
            elif choice == '8':
                print("Import functionality - Coming soon!")
            elif choice == '9':
                preview_template(templates_data)
            else:
                print("Invalid option. Please try again.")
                continue
            
            # Offer to save after each modification
            if choice in ['2', '3', '4', '5']:
                save_choice = input("\nSave changes now? (Y/n): ").strip().lower()
                if save_choice != 'n':
                    save_templates(templates_data)
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            save_choice = input("Save changes before exiting? (y/N): ").strip().lower()
            if save_choice == 'y':
                save_templates(templates_data)
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()