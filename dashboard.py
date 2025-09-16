"""
Monthly Email Draft Dashboard for VALOREM CHEMICALS
Redesigned with two-column layout, bug fixes, and debugging features
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import os
import json
import sys
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
import threading
from src import email_generator

class PriceSheetDashboard:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("VALOREM CHEMICALS - Monthly Email Draft Dashboard")
        self.root.geometry("1200x900")
        self.root.configure(bg="#f0f0f0")

        # Color scheme
        self.colors = {
            'primary': '#1e3a5f',      # Dark blue
            'secondary': '#87ceeb',     # Sky blue
            'bg_light': '#f8f9fa',
            'bg_white': '#ffffff',
            'text_dark': '#2c3e50',
            'border': '#d1d5db',
            'debug': '#fff3cd',         # Light yellow for debug
            'error': '#f8d7da'          # Light red for errors
        }

        # Current values
        self.current_month = date.today().month
        self.current_year = date.today().year
        self.monthly_draft = ""

        # Debug mode flag
        self.debug_mode = tk.BooleanVar(value=False)
        self.debug_messages = []

        # Create monthly_drafts directory if it doesn't exist
        self.drafts_dir = os.path.join(os.path.dirname(__file__), 'monthly_drafts')
        os.makedirs(self.drafts_dir, exist_ok=True)

        self.setup_ui()

    def setup_ui(self):
        """Setup the user interface with two-column layout"""
        # Header
        self.create_header()

        # Main container with two columns
        main_container = tk.Frame(self.root, bg=self.colors['bg_light'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Configure grid weights for responsive design
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=6)  # 60% width
        main_container.grid_columnconfigure(1, weight=4)  # 40% width

        # LEFT COLUMN (60%) - Email Draft and Preview
        left_frame = tk.Frame(main_container, bg=self.colors['bg_light'])
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))

        # Email Draft Section
        self.create_draft_section(left_frame)

        # Preview Section
        self.create_preview_section(left_frame)

        # RIGHT COLUMN (40%) - Controls
        right_frame = tk.Frame(main_container, bg=self.colors['bg_light'])
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))

        # Controls Section
        self.create_controls_section(right_frame)

        # Debug Panel (Initially hidden)
        self.create_debug_panel(main_container)

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
        company_label.pack(pady=15)

        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Monthly Email Draft Dashboard - Enhanced Edition",
            font=('Arial', 12),
            fg=self.colors['secondary'],
            bg=self.colors['primary']
        )
        subtitle_label.pack()

    def create_draft_section(self, parent):
        """Create the email draft section in left column"""
        draft_frame = tk.LabelFrame(
            parent,
            text="Email Draft Content",
            font=('Arial', 12, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['bg_white'],
            relief=tk.RAISED,
            bd=2
        )
        draft_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))

        # Draft text area with increased minimum height
        text_frame = tk.Frame(draft_frame, bg=self.colors['bg_white'])
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.draft_text = scrolledtext.ScrolledText(
            text_frame,
            height=20,  # Increased from 15 to ensure 400px minimum
            font=('Consolas', 10),
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            bd=2
        )
        self.draft_text.pack(fill=tk.BOTH, expand=True)

    def create_preview_section(self, parent):
        """Create the preview section in left column"""
        preview_frame = tk.LabelFrame(
            parent,
            text="Email Preview",
            font=('Arial', 12, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['bg_white'],
            relief=tk.RAISED,
            bd=2
        )
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))

        # Preview text area with minimum height
        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            height=12,  # Ensures 300px minimum
            font=('Arial', 9),
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            bd=2,
            bg='#f8f9fa'
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def create_controls_section(self, parent):
        """Create all controls in right column"""
        # Controls Frame
        controls_frame = tk.LabelFrame(
            parent,
            text="Controls",
            font=('Arial', 12, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['bg_white'],
            relief=tk.RAISED,
            bd=2
        )
        controls_frame.pack(fill=tk.BOTH, expand=True)

        # Inner padding frame
        inner_frame = tk.Frame(controls_frame, bg=self.colors['bg_white'])
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        # Date Selection Section
        date_section = tk.LabelFrame(
            inner_frame,
            text="Date Selection",
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg_white']
        )
        date_section.pack(fill=tk.X, pady=(0, 15))

        date_inner = tk.Frame(date_section, bg=self.colors['bg_white'])
        date_inner.pack(padx=10, pady=10)

        # Month selector
        month_frame = tk.Frame(date_inner, bg=self.colors['bg_white'])
        month_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(month_frame, text="Month:", font=('Arial', 10),
                bg=self.colors['bg_white'], width=8, anchor='w').pack(side=tk.LEFT)

        self.month_var = tk.StringVar(value=str(self.current_month))
        month_combo = ttk.Combobox(
            month_frame,
            textvariable=self.month_var,
            values=[str(i) for i in range(1, 13)],
            width=15,
            state="readonly"
        )
        month_combo.pack(side=tk.LEFT, padx=(5, 0))
        month_combo.bind('<<ComboboxSelected>>', self.on_date_changed)

        # Year selector
        year_frame = tk.Frame(date_inner, bg=self.colors['bg_white'])
        year_frame.pack(fill=tk.X)

        tk.Label(year_frame, text="Year:", font=('Arial', 10),
                bg=self.colors['bg_white'], width=8, anchor='w').pack(side=tk.LEFT)

        self.year_var = tk.StringVar(value=str(self.current_year))
        year_combo = ttk.Combobox(
            year_frame,
            textvariable=self.year_var,
            values=[str(self.current_year + i) for i in range(-1, 3)],
            width=15,
            state="readonly"
        )
        year_combo.pack(side=tk.LEFT, padx=(5, 0))
        year_combo.bind('<<ComboboxSelected>>', self.on_date_changed)

        # Draft Operations Section
        draft_section = tk.LabelFrame(
            inner_frame,
            text="Draft Operations",
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg_white']
        )
        draft_section.pack(fill=tk.X, pady=(0, 15))

        draft_inner = tk.Frame(draft_section, bg=self.colors['bg_white'])
        draft_inner.pack(padx=10, pady=10)

        # Load draft button
        load_btn = tk.Button(
            draft_inner,
            text="Load Draft",
            command=self.load_draft,
            bg=self.colors['secondary'],
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.RAISED,
            bd=2,
            pady=5,
            width=20
        )
        load_btn.pack(pady=(0, 10))

        # Load previous month button
        prev_btn = tk.Button(
            draft_inner,
            text="Load Previous Month",
            command=self.load_previous_month,
            bg=self.colors['secondary'],
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.RAISED,
            bd=2,
            pady=5,
            width=20
        )
        prev_btn.pack(pady=(0, 10))

        # Save draft button
        save_btn = tk.Button(
            draft_inner,
            text="Save Draft",
            command=self.save_draft,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 11, 'bold'),
            relief=tk.RAISED,
            bd=3,
            pady=8,
            width=20
        )
        save_btn.pack()

        # Preview Section
        preview_section = tk.LabelFrame(
            inner_frame,
            text="Preview",
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg_white']
        )
        preview_section.pack(fill=tk.X, pady=(0, 15))

        preview_inner = tk.Frame(preview_section, bg=self.colors['bg_white'])
        preview_inner.pack(padx=10, pady=10)

        # Preview button
        preview_btn = tk.Button(
            preview_inner,
            text="Preview with Sample Customer",
            command=self.preview_email,
            bg=self.colors['secondary'],
            fg='white',
            font=('Arial', 10, 'bold'),
            relief=tk.RAISED,
            bd=2,
            pady=5,
            width=24
        )
        preview_btn.pack()

        # Generation Section
        gen_section = tk.LabelFrame(
            inner_frame,
            text="Email Generation",
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg_white']
        )
        gen_section.pack(fill=tk.X, pady=(0, 15))

        gen_inner = tk.Frame(gen_section, bg=self.colors['bg_white'])
        gen_inner.pack(padx=10, pady=10)

        # Generate button
        self.generate_btn = tk.Button(
            gen_inner,
            text="Generate All Email Drafts",
            command=self.generate_all_drafts,
            bg=self.colors['primary'],
            fg='white',
            font=('Arial', 12, 'bold'),
            relief=tk.RAISED,
            bd=3,
            pady=10,
            width=22
        )
        self.generate_btn.pack(pady=(0, 10))

        # Progress bar
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(
            gen_inner,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            length=250
        )
        self.progress_bar.pack(pady=(0, 10))

        # Status display
        self.status_var = tk.StringVar(value="Ready to generate drafts")
        status_label = tk.Label(
            gen_inner,
            textvariable=self.status_var,
            font=('Arial', 9),
            fg=self.colors['text_dark'],
            bg=self.colors['bg_white'],
            wraplength=250
        )
        status_label.pack()

        # Debug Mode Toggle (at bottom)
        debug_section = tk.Frame(inner_frame, bg=self.colors['bg_white'])
        debug_section.pack(fill=tk.X, pady=(10, 0))

        self.debug_check = tk.Checkbutton(
            debug_section,
            text="Debug Mode",
            variable=self.debug_mode,
            command=self.toggle_debug,
            font=('Arial', 10, 'bold'),
            bg=self.colors['bg_white'],
            activebackground=self.colors['debug']
        )
        self.debug_check.pack(anchor='w')

    def create_debug_panel(self, parent):
        """Create the debug panel (initially hidden)"""
        self.debug_frame = tk.LabelFrame(
            parent,
            text="Debug Output",
            font=('Arial', 10, 'bold'),
            fg=self.colors['text_dark'],
            bg=self.colors['debug'],
            relief=tk.RAISED,
            bd=2
        )
        # Initially don't pack it (hidden)

        # Debug text area
        self.debug_text = scrolledtext.ScrolledText(
            self.debug_frame,
            height=8,  # 150px height
            font=('Consolas', 9),
            wrap=tk.WORD,
            relief=tk.SUNKEN,
            bd=2,
            bg='#fffacd'
        )
        self.debug_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    def toggle_debug(self):
        """Toggle debug panel visibility"""
        if self.debug_mode.get():
            # Show debug panel
            self.debug_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=0, pady=(5, 0))
            self.add_debug_message("Debug mode enabled")
        else:
            # Hide debug panel
            self.debug_frame.grid_forget()
            self.debug_messages.clear()

    def add_debug_message(self, message):
        """Add a message to the debug panel"""
        if self.debug_mode.get():
            timestamp = datetime.now().strftime("%H:%M:%S")
            debug_msg = f"[{timestamp}] {message}\n"
            self.debug_messages.append(debug_msg)

            # Update debug text widget if it exists
            if hasattr(self, 'debug_text'):
                self.debug_text.insert(tk.END, debug_msg)
                self.debug_text.see(tk.END)
                self.root.update_idletasks()

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
                self.add_debug_message(f"Loaded draft from: {draft_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load draft: {str(e)}")
                self.add_debug_message(f"ERROR loading draft: {str(e)}")
        else:
            # Load default template
            self.load_default_template()

    def load_default_template(self):
        """Load a default template for new drafts - WITHOUT signature"""
        # Default template without signature (signature will be added by email_generator)
        default_template = """Hi {recipient_name},

Just a quick note to share the updated pricing for your account - attached for reference.

No change in pricing for {current_month}, as FX movement stayed within the 2% band.

Thanks,"""

        self.draft_text.delete(1.0, tk.END)
        self.draft_text.insert(1.0, default_template)
        self.status_var.set(f"Loaded default template for {self.month_var.get()}/{self.year_var.get()}")
        self.add_debug_message("Loaded default template (signature will be added during generation)")

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

                # Strip any existing signature from the loaded content
                content = self.strip_signature_from_content(content)

                self.draft_text.delete(1.0, tk.END)
                self.draft_text.insert(1.0, content)
                self.status_var.set(f"Loaded previous month's draft ({prev_month}/{prev_year}) as template")
                self.add_debug_message(f"Loaded previous draft from: {prev_draft_file}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load previous month's draft: {str(e)}")
                self.add_debug_message(f"ERROR loading previous draft: {str(e)}")
        else:
            messagebox.showwarning("Warning", f"No draft found for previous month ({prev_month}/{prev_year})")

    def strip_signature_from_content(self, content):
        """Remove any existing signature from content to prevent duplication"""
        # Look for common signature markers
        signature_markers = [
            "Mark Anderson",
            "Managing Director",
            "Valorem Chemicals",
            "+61 417 725 006",
            "marka@valorem.com.au"
        ]

        lines = content.split('\n')
        signature_start = -1

        # Find where signature starts
        for i, line in enumerate(lines):
            if any(marker in line for marker in signature_markers):
                signature_start = i
                break

        if signature_start > 0:
            # Remove everything from signature onwards
            lines = lines[:signature_start]
            self.add_debug_message(f"Stripped existing signature starting at line {signature_start}")

        return '\n'.join(lines).rstrip()

    def save_draft(self):
        """Save the current draft"""
        content = self.draft_text.get(1.0, tk.END).strip()

        if not content:
            messagebox.showwarning("Warning", "No content to save")
            return

        # Strip any signature before saving (signature will be added during generation)
        content = self.strip_signature_from_content(content)

        draft_file = self.get_draft_filename()

        try:
            with open(draft_file, 'w', encoding='utf-8') as f:
                f.write(content)

            month_name = datetime(int(self.year_var.get()), int(self.month_var.get()), 1).strftime("%B")
            self.status_var.set(f"Draft saved for {month_name} {self.year_var.get()}")
            self.add_debug_message(f"Draft saved to: {draft_file}")
            messagebox.showinfo("Success", f"Draft saved successfully for {month_name} {self.year_var.get()}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to save draft: {str(e)}")
            self.add_debug_message(f"ERROR saving draft: {str(e)}")

    def preview_email(self):
        """Preview the email with sample customer data"""
        content = self.draft_text.get(1.0, tk.END).strip()

        if not content:
            messagebox.showwarning("Warning", "No draft content to preview")
            return

        # Strip any existing signature
        content = self.strip_signature_from_content(content)

        # Get date values for placeholder replacement
        month_num = int(self.month_var.get())
        year_num = int(self.year_var.get())
        current_date = datetime(year_num, month_num, 1)

        month_name = current_date.strftime("%B")
        previous_month = (current_date - relativedelta(months=1)).strftime("%B")

        # Sample customer data with properly resolved values
        sample_values = {
            'customer_name': 'ABC Company Pty Ltd',
            'recipient_name': 'John Smith',
            'month': month_name,
            'current_month': month_name,  # Resolve {current_month} properly
            'previous_month': previous_month,
            'percentage': '3.5',
            'effective_date': (current_date + relativedelta(months=1)).strftime("%B 1, %Y"),
            'reason': 'increased supplier costs'
        }

        self.add_debug_message("Preview variables:")
        for key, value in sample_values.items():
            self.add_debug_message(f"  {{{key}}} → {value}")

        # Replace placeholders
        preview_content = content
        for key, value in sample_values.items():
            old_content = preview_content
            preview_content = preview_content.replace(f"{{{key}}}", str(value))
            if old_content != preview_content:
                self.add_debug_message(f"Replaced {{{key}}} with '{value}'")

        # Add signature for preview
        signature = """

Mark Anderson
Managing Director
Valorem Chemicals Pty Ltd
+61 417 725 006
marka@valorem.com.au
www.valorem.com.au"""

        preview_content += signature

        # Display preview
        self.preview_text.delete(1.0, tk.END)
        self.preview_text.insert(1.0, f"PREVIEW - Sample Customer: {sample_values['customer_name']}\n")
        self.preview_text.insert(tk.END, "="*60 + "\n\n")
        self.preview_text.insert(tk.END, f"Subject: Monthly Pricing Update for {sample_values['customer_name']}\n\n")
        self.preview_text.insert(tk.END, preview_content)

        self.status_var.set("Preview updated with sample customer data")

    def update_progress(self, current, total, message):
        """Update progress bar and status from background thread"""
        self.progress_var.set(current)
        self.status_var.set(message)
        self.root.update_idletasks()

    def generate_all_drafts(self):
        """Generate all email drafts using the saved monthly template"""
        # First, save the current draft
        self.save_draft()

        # Prepare the monthly draft as a custom template
        content = self.draft_text.get(1.0, tk.END).strip()

        # IMPORTANT: Strip any signature from content before creating template
        content = self.strip_signature_from_content(content)

        if not content:
            messagebox.showwarning("Warning", "No draft content to use for generation")
            return

        self.add_debug_message("="*60)
        self.add_debug_message("Starting email generation process")
        self.add_debug_message(f"Template content length: {len(content)} characters")

        # Disable generate button during processing
        self.generate_btn.config(state='disabled')
        self.progress_var.set(0)

        try:
            self.status_var.set("Preparing dashboard template...")
            self.root.update()

            # Get current month details
            month_num = int(self.month_var.get())
            year_num = int(self.year_var.get())
            current_date = datetime(year_num, month_num, 1)
            month_name = current_date.strftime("%B")

            # Load existing email_templates.json to get signature info
            templates_file = os.path.join(os.path.dirname(__file__), 'email_templates.json')
            signature_info = {}
            default_values = {}

            if os.path.exists(templates_file):
                with open(templates_file, 'r', encoding='utf-8') as f:
                    existing_data = json.load(f)
                    signature_info = existing_data.get('signature', {})
                    default_values = existing_data.get('default_values', {})
                    self.add_debug_message("Loaded signature and default values from email_templates.json")

            # Fix Bug 2: Properly resolve date placeholders BEFORE creating template
            date_placeholders = email_generator.get_date_placeholders()

            # Override default_values with actual resolved dates
            resolved_values = {}
            for key, value in default_values.items():
                if isinstance(value, str) and '{' in value and '}' in value:
                    # This is a placeholder that needs resolution
                    placeholder_key = value.strip('{}')
                    if placeholder_key in date_placeholders:
                        resolved_values[key] = date_placeholders[placeholder_key]
                        self.add_debug_message(f"Resolved {key}: {value} → {resolved_values[key]}")
                    else:
                        resolved_values[key] = value
                else:
                    resolved_values[key] = value

            # Merge with actual date values
            resolved_values.update(date_placeholders)

            self.add_debug_message("Final resolved values:")
            for key, value in resolved_values.items():
                self.add_debug_message(f"  {key}: {value}")

            # Create dashboard template WITHOUT signature in content
            custom_template = {
                "templates": {
                    "dashboard_custom": {
                        "name": f"Dashboard Template - {month_name} {year_num}",
                        "subject": "Monthly Pricing Update for {customer_name}",
                        "body": {
                            "content": content  # Content without signature
                        }
                    }
                },
                "signature": signature_info,  # Signature will be added by email_generator
                "default_values": resolved_values  # Use resolved values, not placeholders
            }

            # Save as dashboard template file
            temp_template_file = os.path.join(self.drafts_dir, 'dashboard_template.json')
            with open(temp_template_file, 'w', encoding='utf-8') as f:
                json.dump(custom_template, f, indent=2)

            self.add_debug_message(f"Dashboard template saved to: {temp_template_file}")
            self.add_debug_message("Signature will be added by email_generator module")

            self.status_var.set("Generating email drafts...")
            self.root.update()

            # Run email generation in a background thread to keep UI responsive
            def generate_in_background():
                try:
                    # Call the email generator with resolved values
                    results = email_generator.create_email_drafts_batch(
                        template_key='dashboard_custom',
                        custom_values=resolved_values,  # Pass resolved values
                        progress_callback=lambda curr, total, msg: self.root.after(0, self.update_progress, curr, total, msg)
                    )

                    # Update UI with results in main thread
                    self.root.after(0, self.display_generation_results, results)

                except Exception as e:
                    error_msg = f"Failed to generate drafts: {str(e)}"
                    self.root.after(0, lambda: self.add_debug_message(f"ERROR: {error_msg}"))
                    self.root.after(0, lambda: messagebox.showerror("Error", error_msg))
                    self.root.after(0, lambda: self.status_var.set("Error occurred during generation"))
                finally:
                    self.root.after(0, lambda: self.generate_btn.config(state='normal'))

            # Start background thread
            thread = threading.Thread(target=generate_in_background, daemon=True)
            thread.start()

        except Exception as e:
            error_msg = f"Failed to prepare template: {str(e)}"
            self.add_debug_message(f"ERROR: {error_msg}")
            messagebox.showerror("Error", error_msg)
            self.status_var.set("Error occurred during preparation")
            self.generate_btn.config(state='normal')

    def display_generation_results(self, results):
        """Display the results of email generation"""
        month_name = datetime(int(self.year_var.get()), int(self.month_var.get()), 1).strftime("%B")

        if results['success']:
            self.add_debug_message(f"Generation complete: {results['drafts_created']} drafts created")

            # Update status
            self.status_var.set(f"Complete! Created {results['drafts_created']} draft(s)")

            # Show success message
            messagebox.showinfo(
                "Success",
                f"Successfully created {results['drafts_created']} email draft(s) for {month_name} {self.year_var.get()}.\n\n"
                "The drafts are now in your Outlook Drafts folder.\n"
                "Please review them before sending."
            )

            # Show details in debug if enabled
            if self.debug_mode.get() and results['details']:
                self.add_debug_message("\nDraft Details:")
                for detail in results['details']:
                    if detail['status'] == 'success':
                        self.add_debug_message(f"  ✓ {detail['customer']}")
                    else:
                        self.add_debug_message(f"  ✗ {detail['customer']}: {detail.get('error', 'Unknown error')}")
        else:
            self.add_debug_message(f"Generation failed with {len(results['errors'])} errors")

            # Display errors
            for error in results['errors']:
                self.add_debug_message(f"ERROR: {error}")

            self.status_var.set("Generation failed - see debug output")

            # Show error dialog
            messagebox.showerror(
                "Error",
                f"Email generation failed.\n\n"
                f"Errors: {len(results['errors'])}\n"
                f"Check debug output for details.\n\n"
                f"Debug log: {results.get('debug_log', 'N/A')}"
            )

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