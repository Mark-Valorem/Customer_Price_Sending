import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import json
import subprocess
import sys
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd

class PriceSheetDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VALOREM CHEMICALS - Monthly Email Draft Dashboard")
        self.root.geometry("1000x800")
        self.root.configure(bg="#f0f0f0")

        # Color scheme
        self.colors = {
            'primary': '#1e3a5f',      # Dark blue
            'secondary': '#87ceeb',     # Sky blue
            'bg_light': '#f8f9fa',
            'bg_white': '#ffffff',
            'text_dark': '#2c3e50',
            'border': '#d1d5db'
        }

        # Current values
        self.current_month = date.today().month
        self.current_year = date.today().year
        self.monthly_draft = ""

        # Create monthly_drafts directory if it doesn't exist
        self.drafts_dir = os.path.join(os.path.dirname(__file__), 'monthly_drafts')
        os.makedirs(self.drafts_dir, exist_ok=True)

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface"""
        # Header
        self.create_header()

        # Main container
        main_frame = tk.Frame(self.root, bg=self.colors['bg_light'])
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Monthly Email Draft Section
        self.create_monthly_draft_section(main_frame)

        # Preview Section
        self.create_preview_section(main_frame)

        # Generate Section
        self.create_generate_section(main_frame)

    def create_header(self):
        """Create the header with Valorem branding"""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)

        # Company name
        company_label = tk.Label(
            header_frame,
            text="VALOREM CHEMICALS",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg=self.colors['primary']
        )
        company_label.pack(pady=20)

        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Monthly Email Draft Dashboard",
            font=('Arial', 12),
            fg=self.colors['secondary'],
            bg=self.colors['primary']
        )
        subtitle_label.pack()

    def create_monthly_draft_section(self, parent):
        """Create the monthly email draft section"""
        # Frame with raised border
        draft_frame = tk.LabelFrame(
            parent,
            text="Monthly Email Draft",
            font=('Arial', 14, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['bg_white'],
            relief=tk.RAISED,
            bd=2
        )
        draft_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Month/Year selector
        selector_frame = tk.Frame(draft_frame, bg=self.colors['bg_white'])
        selector_frame.pack(fill=tk.X, padx=10, pady=5)

        tk.Label(selector_frame, text="Month:", font=('Arial', 10),
                bg=self.colors['bg_white']).pack(side=tk.LEFT, padx=(0, 5))

        self.month_var = tk.StringVar(value=str(self.current_month))
        month_combo = ttk.Combobox(
            selector_frame,
            textvariable=self.month_var,
            values=[str(i) for i in range(1, 13)],
            width=5,
            state="readonly"
        )
        month_combo.pack(side=tk.LEFT, padx=(0, 10))

        tk.Label(selector_frame, text="Year:", font=('Arial', 10),
                bg=self.colors['bg_white']).pack(side=tk.LEFT, padx=(0, 5))

        self.year_var = tk.StringVar(value=str(self.current_year))
        year_combo = ttk.Combobox(
            selector_frame,
            textvariable=self.year_var,
            values=[str(self.current_year + i) for i in range(-1, 3)],
            width=8,
            state="readonly"
        )
        year_combo.pack(side=tk.LEFT, padx=(0, 20))

        # Bind change events
        month_combo.bind('<<ComboboxSelected>>', self.on_date_changed)
        year_combo.bind('<<ComboboxSelected>>', self.on_date_changed)

        # Load draft button
        load_btn = tk.Button(
            selector_frame,
            text="Load Draft",
            command=self.load_draft,
            bg=self.colors['secondary'],
            fg='white',
            font=('Arial', 10),
            relief=tk.RAISED,
            bd=2
        )
        load_btn.pack(side=tk.LEFT, padx=(0, 10))

        # Load previous month button
        prev_btn = tk.Button(
            selector_frame,
            text="Load Previous Month",
            command=self.load_previous_month,
            bg=self.colors['secondary'],
            fg='white',
            font=('Arial', 10),
            relief=tk.RAISED,
            bd=2
        )
        prev_btn.pack(side=tk.LEFT)

        # Large text area for email draft
        text_frame = tk.Frame(draft_frame, bg=self.colors['bg_white'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(text_frame, text="Email Draft Content:",
                font=('Arial', 10, 'bold'),
                bg=self.colors['bg_white']).pack(anchor=tk.W)

        self.draft_text = scrolledtext.ScrolledText(
            text_frame,
            height=15,
            font=('Consolas', 10),
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            bd=2
        )
        self.draft_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # Save draft button
        save_frame = tk.Frame(draft_frame, bg=self.colors['bg_white'])
        save_frame.pack(fill=tk.X, padx=10, pady=5)

        save_btn = tk.Button(
            save_frame,
            text="Save Draft",
            command=self.save_draft,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.RAISED,
            bd=3,
            pady=5
        )
        save_btn.pack(side=tk.RIGHT)

    def create_preview_section(self, parent):
        """Create the preview section"""
        preview_frame = tk.LabelFrame(
            parent,
            text="Preview",
            font=('Arial', 14, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['bg_white'],
            relief=tk.RAISED,
            bd=2
        )
        preview_frame.pack(fill=tk.X, padx=5, pady=5)

        # Preview button
        btn_frame = tk.Frame(preview_frame, bg=self.colors['bg_white'])
        btn_frame.pack(fill=tk.X, padx=10, pady=5)

        preview_btn = tk.Button(
            btn_frame,
            text="Preview with Sample Customer",
            command=self.preview_email,
            bg=self.colors['secondary'],
            fg='white',
            font=('Arial', 11, 'bold'),
            relief=tk.RAISED,
            bd=2,
            pady=3
        )
        preview_btn.pack(side=tk.LEFT)

        # Preview text area
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            height=6,
            font=('Arial', 9),
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            bd=2,
            bg='#f8f9fa'
        )
        self.preview_text.pack(fill=tk.X, padx=10, pady=(0, 10))

    def create_generate_section(self, parent):
        """Create the generate section"""
        generate_frame = tk.LabelFrame(
            parent,
            text="Generate Email Drafts",
            font=('Arial', 14, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['bg_white'],
            relief=tk.RAISED,
            bd=2
        )
        generate_frame.pack(fill=tk.X, padx=5, pady=5)

        # Generate button and status
        control_frame = tk.Frame(generate_frame, bg=self.colors['bg_white'])
        control_frame.pack(fill=tk.X, padx=10, pady=10)

        generate_btn = tk.Button(
            control_frame,
            text="Generate All Email Drafts",
            command=self.generate_all_drafts,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.RAISED,
            bd=3,
            pady=8,
            padx=20
        )
        generate_btn.pack(side=tk.LEFT)

        # Status display
        self.status_var = tk.StringVar(value="Ready to generate drafts")
        status_label = tk.Label(
            control_frame,
            textvariable=self.status_var,
            font=('Arial', 10),
            fg=self.colors['text_dark'],
            bg=self.colors['bg_white']
        )
        status_label.pack(side=tk.LEFT, padx=(20, 0))

    def on_date_changed(self, event=None):
        """Handle month/year selection change"""
        self.load_draft()

    def get_draft_filename(self, month=None, year=None):
        """Get the filename for the monthly draft"""
        if month is None:
            month = int(self.month_var.get())
        if year is None:
            year = int(self.year_var.get())
        return os.path.join(self.drafts_dir, f"{year}_{month:02d}.txt")

    def load_draft(self):
        """Load the draft for the selected month/year"""
        draft_file = self.get_draft_filename()

        if os.path.exists(draft_file):
            try:
                with open(draft_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.draft_text.delete(1.0, tk.END)
                self.draft_text.insert(1.0, content)
                self.status_var.set(f"Loaded draft for {self.month_var.get()}/{self.year_var.get()}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load draft: {str(e)}")
        else:
            # Load default template
            self.load_default_template()

    def load_default_template(self):
        """Load a default template for new drafts"""
        default_template = """Hi {recipient_name},

Just a quick note to share the updated pricing for your account - attached for reference.

No change in pricing for {month}, as FX movement stayed within the 2% band.

Thanks,

Mark Anderson
Managing Director
Valorem Chemicals Pty Ltd
+61 417 725 006
marka@valorem.com.au
www.valorem.com.au"""

        self.draft_text.delete(1.0, tk.END)
        self.draft_text.insert(1.0, default_template)
        self.status_var.set(f"Loaded default template for {self.month_var.get()}/{self.year_var.get()}")

    def load_previous_month(self):
        """Load the previous month's draft as a starting point"""
        current_month = int(self.month_var.get())
        current_year = int(self.year_var.get())

        # Calculate previous month
        if current_month == 1:
            prev_month = 12
            prev_year = current_year - 1
        else:
            prev_month = current_month - 1
            prev_year = current_year

        prev_draft_file = self.get_draft_filename(prev_month, prev_year)

        if os.path.exists(prev_draft_file):
            try:
                with open(prev_draft_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.draft_text.delete(1.0, tk.END)
                self.draft_text.insert(1.0, content)
                self.status_var.set(f"Loaded previous month's draft ({prev_month}/{prev_year}) as template")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load previous month's draft: {str(e)}")
        else:
            messagebox.showwarning("Warning", f"No draft found for previous month ({prev_month}/{prev_year})")

    def save_draft(self):
        """Save the current draft"""
        content = self.draft_text.get(1.0, tk.END).strip()

        if not content:
            messagebox.showwarning("Warning", "No content to save")
            return

        draft_file = self.get_draft_filename()

        try:
            with open(draft_file, 'w', encoding='utf-8') as f:
                f.write(content)

            month_name = datetime(int(self.year_var.get()), int(self.month_var.get()), 1).strftime("%B")
            self.status_var.set(f"Draft saved for {month_name} {self.year_var.get()}")
            messagebox.showinfo("Success", f"Draft saved successfully for {month_name} {self.year_var.get()}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save draft: {str(e)}")

    def preview_email(self):
        """Preview the email with sample customer data"""
        content = self.draft_text.get(1.0, tk.END).strip()

        if not content:
            messagebox.showwarning("Warning", "No draft content to preview")
            return

        # Get date values for placeholder replacement
        month_name = datetime(int(self.year_var.get()), int(self.month_var.get()), 1).strftime("%B")

        # Sample customer data
        sample_values = {
            'customer_name': 'ABC Company Pty Ltd',
            'recipient_name': 'John Smith',
            'month': month_name,
            'previous_month': (datetime(int(self.year_var.get()), int(self.month_var.get()), 1) - relativedelta(months=1)).strftime("%B"),
            'current_month': month_name,
            'percentage': '3.5',
            'effective_date': 'October 1, 2024',
            'reason': 'increased supplier costs'
        }

        # Replace placeholders
        preview_content = content
        for key, value in sample_values.items():
            preview_content = preview_content.replace(f"{{{key}}}", str(value))

        # Display preview
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, f"PREVIEW - Sample Customer: {sample_values['customer_name']}\n")
        self.preview_text.insert(tk.END, "="*60 + "\n\n")
        self.preview_text.insert(tk.END, preview_content)

        self.status_var.set("Preview updated with sample customer data")

    def generate_all_drafts(self):
        """Generate all email drafts using the saved monthly template"""
        # First, save the current draft
        self.save_draft()

        # Check if create_drafts_enhanced.py exists
        enhanced_script = os.path.join(os.path.dirname(__file__), 'create_drafts_enhanced.py')

        if not os.path.exists(enhanced_script):
            messagebox.showerror("Error", "create_drafts_enhanced.py not found")
            return

        # Prepare the monthly draft as a custom template
        content = self.draft_text.get(1.0, tk.END).strip()

        if not content:
            messagebox.showwarning("Warning", "No draft content to use for generation")
            return

        try:
            self.status_var.set("Preparing dashboard template...")
            self.root.update()

            # Load existing email_templates.json to get signature info
            templates_file = os.path.join(os.path.dirname(__file__), 'email_templates.json')
            signature_info = {}
            default_values = {}

            if os.path.exists(templates_file):
                with open(templates_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    signature_info = existing_data.get('signature', {})
                    default_values = existing_data.get('default_values', {})

            # Create dashboard template with signature and default values
            month_name = datetime(int(self.year_var.get()), int(self.month_var.get()), 1).strftime("%B")

            custom_template = {
                "templates": {
                    "dashboard_custom": {
                        "name": f"Dashboard Template - {month_name} {self.year_var.get()}",
                        "subject": "Monthly Pricing Update for {customer_name}",
                        "body": {
                            "content": content
                        }
                    }
                },
                "signature": signature_info,
                "default_values": default_values
            }

            # Save as dashboard template file
            temp_template_file = os.path.join(self.drafts_dir, 'dashboard_template.json')
            with open(temp_template_file, 'w', encoding='utf-8') as f:
                json.dump(custom_template, f, indent=2)

            self.status_var.set("Launching create_drafts_enhanced.py...")
            self.root.update()

            # Run the enhanced script directly
            try:
                if sys.platform.startswith('win'):
                    # Run in a new command window
                    subprocess.Popen(
                        ['cmd', '/k', 'python', 'create_drafts_enhanced.py'],
                        cwd=os.path.dirname(__file__),
                        creationflags=subprocess.CREATE_NEW_CONSOLE
                    )
                else:
                    # For non-Windows systems
                    subprocess.Popen(['python', 'create_drafts_enhanced.py'], cwd=os.path.dirname(__file__))

                result = messagebox.showinfo(
                    "Dashboard Template Ready",
                    f"Dashboard template has been created for {month_name} {self.year_var.get()}.\n\n"
                    "The enhanced script has been launched. When prompted:\n"
                    f"1. Look for 'Dashboard Template - {month_name} {self.year_var.get()}'\n"
                    "2. Select that template to use your custom monthly draft\n"
                    "3. Review and customize any placeholders as needed\n\n"
                    "Your monthly draft will be used for all customer emails."
                )

                self.status_var.set(f"Dashboard template ready - {month_name} {self.year_var.get()}")

            except Exception as e:
                # Fallback - just show instructions
                messagebox.showinfo(
                    "Template Created",
                    f"Dashboard template created for {month_name} {self.year_var.get()}.\n\n"
                    "To use it:\n"
                    "1. Run create_drafts_enhanced.py manually\n"
                    f"2. Select 'Dashboard Template - {month_name} {self.year_var.get()}'\n"
                    "3. Follow the prompts to generate all customer emails\n\n"
                    f"Template saved to: {temp_template_file}"
                )
                self.status_var.set("Template created - run enhanced script manually")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate drafts: {str(e)}")
            self.status_var.set("Error occurred during generation")

    def run(self):
        """Run the dashboard"""
        # Load the current month's draft on startup
        self.load_draft()

        # Start the GUI
        self.root.mainloop()

def main():
    """Main function to run the dashboard"""
    try:
        app = PriceSheetDashboard()
        app.run()
    except Exception as e:
        print(f"Error starting dashboard: {str(e)}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()