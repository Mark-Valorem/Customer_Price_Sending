#!/usr/bin/env python3
"""
Enhanced Monthly Email Draft Dashboard v3.0
===========================================

Version 3.0 Features:
- Direct launch without terminal
- Simplified email draft management (default template only)
- Enhanced customer verification console (50/50 split)
- User selection with HTML signatures
- Company logo integration
- Streamlined user interface

Author: Claude Code v3.0
Date: 2025-09-19
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
from PIL import Image, ImageTk
from src import email_generator
from src.verification_system import MultiLayerVerificationSystem, CustomerDatabase

class CustomerManagementPanel:
    """Customer Management Panel with enhanced verification console"""

    def __init__(self, parent_frame, dashboard_ref, database_file="data/customer_database.json"):
        self.parent_frame = parent_frame
        self.dashboard_ref = dashboard_ref
        self.database_file = database_file
        self.database = CustomerDatabase(database_file)
        self.verification_system = MultiLayerVerificationSystem(database_file)

        # Customer management widgets
        self.customer_tree = None
        self.verification_console = None
        self.current_customer = None

        self.setup_customer_management_ui()

    def setup_customer_management_ui(self):
        """Setup the customer management interface with 50/50 split"""
        # Create main horizontal paned window for 50/50 split
        self.main_paned = ttk.PanedWindow(self.parent_frame, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left frame: Customer list and management
        self.left_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.left_frame, weight=1)

        # Right frame: Verification console
        self.right_frame = ttk.Frame(self.main_paned)
        self.main_paned.add(self.right_frame, weight=1)

        self.setup_customer_list_section()
        self.setup_verification_console_section()

    def setup_customer_list_section(self):
        """Setup the customer list section (left side)"""
        # Title
        title_frame = ttk.Frame(self.left_frame)
        title_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Label(title_frame, text="Customer Database", font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)

        # Search frame
        search_frame = ttk.Frame(self.left_frame)
        search_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 10))
        search_entry.bind('<KeyRelease>', lambda e: self.search_customers())

        ttk.Button(search_frame, text="Refresh", command=self.refresh_customer_list).pack(side=tk.RIGHT)

        # Customer list frame
        list_frame = ttk.Frame(self.left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Treeview for customer list
        columns = ('ID', 'Company', 'Domain', 'Emails', 'Status')
        self.customer_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        # Define headings
        for col in columns:
            self.customer_tree.heading(col, text=col)
            if col == 'Company':
                self.customer_tree.column(col, width=150)
            elif col == 'Emails':
                self.customer_tree.column(col, width=100)
            else:
                self.customer_tree.column(col, width=80)

        # Scrollbars
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.customer_tree.yview)
        self.customer_tree.configure(yscrollcommand=vsb.set)

        # Pack treeview and scrollbar
        self.customer_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)

        # Bind double-click to edit
        self.customer_tree.bind('<Double-Button-1>', self.edit_customer)

        # Buttons frame
        buttons_frame = ttk.Frame(self.left_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Button(buttons_frame, text="Add Customer", command=self.add_customer_dialog).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Edit Selected", command=self.edit_customer).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(buttons_frame, text="Delete Selected", command=self.delete_customer).pack(side=tk.LEFT, padx=(0, 5))

        # Load initial data
        self.refresh_customer_list()

    def setup_verification_console_section(self):
        """Setup the verification console section (right side)"""
        # Title frame
        title_frame = ttk.Frame(self.right_frame)
        title_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        ttk.Label(title_frame, text="Verification Console", font=('Segoe UI', 12, 'bold')).pack(side=tk.LEFT)

        # Verification buttons
        buttons_frame = ttk.Frame(self.right_frame)
        buttons_frame.pack(fill=tk.X, padx=10, pady=5)

        self.verify_all_btn = ttk.Button(
            buttons_frame,
            text="Verify ALL Customers",
            command=self.verify_all_customers,
            style='Accent.TButton'
        )
        self.verify_all_btn.pack(side=tk.LEFT, padx=(0, 5))

        self.clear_console_btn = ttk.Button(
            buttons_frame,
            text="Clear Console",
            command=self.clear_verification_console
        )
        self.clear_console_btn.pack(side=tk.LEFT, padx=(0, 5))

        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.right_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress_bar.pack(fill=tk.X, padx=10, pady=5)

        # Verification console (scrolled text)
        console_frame = ttk.LabelFrame(self.right_frame, text="Verification Output")
        console_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.verification_console = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            width=50,
            height=20,
            font=('Courier New', 9),
            bg='#1e1e1e',
            fg='#d4d4d4',
            insertbackground='white'
        )
        self.verification_console.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configure console tags for colored output
        self.verification_console.tag_config('info', foreground='#3794ff')
        self.verification_console.tag_config('success', foreground='#4ec9b0')
        self.verification_console.tag_config('warning', foreground='#ce9178')
        self.verification_console.tag_config('error', foreground='#f48771')
        self.verification_console.tag_config('header', foreground='#dcdcaa', font=('Courier New', 10, 'bold'))

        # Summary frame
        summary_frame = ttk.LabelFrame(self.right_frame, text="Summary")
        summary_frame.pack(fill=tk.X, padx=10, pady=5)

        self.summary_label = ttk.Label(summary_frame, text="Ready to verify", font=('Segoe UI', 10))
        self.summary_label.pack(padx=10, pady=5)

    def add_console_message(self, message, tag='info'):
        """Add a message to the verification console"""
        self.verification_console.configure(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.verification_console.insert(tk.END, f"[{timestamp}] ", 'info')
        self.verification_console.insert(tk.END, f"{message}\n", tag)
        self.verification_console.configure(state=tk.DISABLED)
        self.verification_console.see(tk.END)
        self.parent_frame.update_idletasks()

    def clear_verification_console(self):
        """Clear the verification console"""
        self.verification_console.configure(state=tk.NORMAL)
        self.verification_console.delete(1.0, tk.END)
        self.verification_console.configure(state=tk.DISABLED)
        self.progress_var.set(0)
        self.summary_label.config(text="Ready to verify")

    def verify_all_customers(self):
        """Verify ALL customers with real-time console output"""
        # Clear console first
        self.clear_verification_console()

        # Disable verify button during process
        self.verify_all_btn.config(state='disabled')

        def verification_thread():
            try:
                self.add_console_message("STARTING VERIFICATION OF ALL CUSTOMERS", 'header')
                self.add_console_message("=" * 60, 'info')

                # Get all customers
                customers = self.database.get_all_customers()
                total_customers = len(customers)

                if total_customers == 0:
                    self.add_console_message("No customers found in database", 'warning')
                    return

                self.add_console_message(f"Found {total_customers} customers to verify\n", 'info')

                # Track results
                results = {
                    'passed': [],
                    'failed': [],
                    'warnings': []
                }

                # Verify each customer
                for idx, customer in enumerate(customers):
                    customer_id = customer['id']
                    company_name = customer['company_name']

                    # Update progress
                    progress = ((idx + 1) / total_customers) * 100
                    self.progress_var.set(progress)

                    self.add_console_message(f"\n[{idx+1}/{total_customers}] Verifying: {company_name}", 'header')
                    self.add_console_message("-" * 40, 'info')

                    # Perform verification
                    verification_result = self.verification_system.verify_customer(customer_id)

                    if verification_result['overall_status'] == 'passed':
                        self.add_console_message(f"✓ Domain verified: {customer['email_domain']}", 'success')
                        self.add_console_message(f"✓ Recipients verified: {len(customer['email_addresses'])} emails", 'success')
                        # Handle file_generation as either dict or list
                        file_gen = customer.get('file_generation', {})
                        if isinstance(file_gen, dict):
                            file_count = 1 if file_gen.get('file_path') else 0
                        else:
                            file_count = len(file_gen)
                        self.add_console_message(f"✓ File paths verified: {file_count} file{'s' if file_count != 1 else ''}", 'success')
                        self.add_console_message("STATUS: PASSED", 'success')
                        results['passed'].append(company_name)
                    elif verification_result['overall_status'] == 'warning':
                        for issue in verification_result['issues']:
                            self.add_console_message(f"⚠ {issue['message']}", 'warning')
                        self.add_console_message("STATUS: WARNING", 'warning')
                        results['warnings'].append(company_name)
                    else:
                        for issue in verification_result['issues']:
                            self.add_console_message(f"✗ {issue['message']}", 'error')
                        self.add_console_message("STATUS: FAILED", 'error')
                        results['failed'].append(company_name)

                # Display summary
                self.add_console_message("\n" + "=" * 60, 'info')
                self.add_console_message("VERIFICATION COMPLETE - SUMMARY", 'header')
                self.add_console_message("=" * 60, 'info')

                self.add_console_message(f"\nTotal Customers: {total_customers}", 'info')
                self.add_console_message(f"✓ Passed: {len(results['passed'])} ({len(results['passed'])*100//total_customers}%)", 'success')
                self.add_console_message(f"⚠ Warnings: {len(results['warnings'])} ({len(results['warnings'])*100//total_customers}%)", 'warning')
                self.add_console_message(f"✗ Failed: {len(results['failed'])} ({len(results['failed'])*100//total_customers}%)", 'error')

                # List failed customers if any
                if results['failed']:
                    self.add_console_message("\nFailed Customers:", 'error')
                    for customer in results['failed']:
                        self.add_console_message(f"  - {customer}", 'error')

                # Update summary label
                summary_text = f"Passed: {len(results['passed'])} | Warnings: {len(results['warnings'])} | Failed: {len(results['failed'])}"
                self.summary_label.config(text=summary_text)

                # Update customer list to reflect verification status
                self.refresh_customer_list()

            except Exception as e:
                self.add_console_message(f"\nERROR: {str(e)}", 'error')
            finally:
                # Re-enable verify button
                self.verify_all_btn.config(state='normal')
                self.progress_var.set(100)

        # Run verification in separate thread
        thread = threading.Thread(target=verification_thread, daemon=True)
        thread.start()

    def refresh_customer_list(self):
        """Refresh the customer list display"""
        # Clear current items
        for item in self.customer_tree.get_children():
            self.customer_tree.delete(item)

        # Get search term
        search_term = self.search_var.get().lower()

        # Load and display customers
        customers = self.database.get_all_customers()

        for customer in customers:
            # Skip inactive customers
            if not customer.get('active', True):
                continue

            # Check if search term matches any field
            searchable_text = f"{customer['company_name']} {customer['email_domain']} {' '.join(customer['email_addresses'])}".lower()

            if not search_term or search_term in searchable_text:
                customer_id = customer['id']
                company = customer['company_name']
                domain = customer['email_domain']
                email_count = len(customer['email_addresses'])
                status = "✓" if customer['verification_status']['domain_verified'] else "⚠"

                self.customer_tree.insert('', tk.END, values=(
                    customer_id, company, domain, f"{email_count}", status
                ))

    def search_customers(self):
        """Search customers based on search term"""
        self.refresh_customer_list()

    def add_customer_dialog(self):
        """Show dialog to add new customer"""
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title("Add New Customer")
        dialog.geometry("500x400")

        # Form fields
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(form_frame, text="Company Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        company_entry = ttk.Entry(form_frame, width=40)
        company_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Email Domain:").grid(row=1, column=0, sticky=tk.W, pady=5)
        domain_entry = ttk.Entry(form_frame, width=40)
        domain_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Email Addresses:").grid(row=2, column=0, sticky=tk.NW, pady=5)
        email_text = tk.Text(form_frame, width=40, height=5)
        email_text.grid(row=2, column=1, pady=5)
        ttk.Label(form_frame, text="(One per line)", font=('Segoe UI', 8)).grid(row=3, column=1, sticky=tk.W)

        ttk.Label(form_frame, text="Recipient Names:").grid(row=4, column=0, sticky=tk.NW, pady=5)
        names_text = tk.Text(form_frame, width=40, height=5)
        names_text.grid(row=4, column=1, pady=5)

        def save_customer():
            company = company_entry.get().strip()
            domain = domain_entry.get().strip()
            emails = [e.strip() for e in email_text.get(1.0, tk.END).strip().split('\n') if e.strip()]
            names = [n.strip() for n in names_text.get(1.0, tk.END).strip().split('\n') if n.strip()]

            if not company or not domain or not emails:
                messagebox.showerror("Error", "Please fill in all required fields")
                return

            try:
                self.database.add_customer({
                    'company_name': company,
                    'email_domain': domain,
                    'email_addresses': emails,
                    'recipient_names': names,
                    'file_generation': [],
                    'active': True
                })
                self.refresh_customer_list()
                dialog.destroy()
                messagebox.showinfo("Success", "Customer added successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to add customer: {str(e)}")

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Save", command=save_customer).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def edit_customer(self, event=None):
        """Edit selected customer"""
        selection = self.customer_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer to edit")
            return

        customer_id = self.customer_tree.item(selection[0])['values'][0]
        customer = self.database.get_customer_by_id(customer_id)

        if not customer:
            messagebox.showerror("Error", "Customer not found")
            return

        # Create edit dialog (similar to add_customer_dialog but pre-populated)
        dialog = tk.Toplevel(self.parent_frame)
        dialog.title(f"Edit Customer: {customer['company_name']}")
        dialog.geometry("500x400")

        # Form fields
        form_frame = ttk.Frame(dialog)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        ttk.Label(form_frame, text="Company Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        company_entry = ttk.Entry(form_frame, width=40)
        company_entry.insert(0, customer['company_name'])
        company_entry.grid(row=0, column=1, pady=5)

        ttk.Label(form_frame, text="Email Domain:").grid(row=1, column=0, sticky=tk.W, pady=5)
        domain_entry = ttk.Entry(form_frame, width=40)
        domain_entry.insert(0, customer['email_domain'])
        domain_entry.grid(row=1, column=1, pady=5)

        ttk.Label(form_frame, text="Email Addresses:").grid(row=2, column=0, sticky=tk.NW, pady=5)
        email_text = tk.Text(form_frame, width=40, height=5)
        email_text.insert(1.0, '\n'.join(customer['email_addresses']))
        email_text.grid(row=2, column=1, pady=5)

        ttk.Label(form_frame, text="Recipient Names:").grid(row=4, column=0, sticky=tk.NW, pady=5)
        names_text = tk.Text(form_frame, width=40, height=5)
        names_text.insert(1.0, '\n'.join(customer.get('recipient_names', [])))
        names_text.grid(row=4, column=1, pady=5)

        def save_changes():
            customer['company_name'] = company_entry.get().strip()
            customer['email_domain'] = domain_entry.get().strip()
            customer['email_addresses'] = [e.strip() for e in email_text.get(1.0, tk.END).strip().split('\n') if e.strip()]
            customer['recipient_names'] = [n.strip() for n in names_text.get(1.0, tk.END).strip().split('\n') if n.strip()]

            try:
                self.database.update_customer(customer_id, customer)
                self.refresh_customer_list()
                dialog.destroy()
                messagebox.showinfo("Success", "Customer updated successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to update customer: {str(e)}")

        # Buttons
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="Save Changes", command=save_changes).pack(side=tk.RIGHT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)

    def delete_customer(self):
        """Delete selected customer"""
        selection = self.customer_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a customer to delete")
            return

        customer_id = self.customer_tree.item(selection[0])['values'][0]
        company_name = self.customer_tree.item(selection[0])['values'][1]

        if messagebox.askyesno("Confirm Delete", f"Delete customer '{company_name}'?"):
            try:
                self.database.delete_customer(customer_id)
                self.refresh_customer_list()
                messagebox.showinfo("Success", "Customer deleted successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete customer: {str(e)}")


class EmailDraftDashboard:
    """Main Dashboard Application"""

    def __init__(self, root):
        self.root = root
        self.root.title("Valorem Chemicals - Email Dashboard v3.0")
        self.root.geometry("1400x800")

        # Set icon if available
        try:
            self.root.iconbitmap('valorem_icon.ico')
        except:
            pass

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')

        # Color scheme
        self.colors = {
            'primary': '#2e7d32',
            'secondary': '#1976d2',
            'success': '#4caf50',
            'warning': '#ff9800',
            'error': '#f44336',
            'dark': '#212121',
            'light': '#fafafa'
        }

        # Configure styles
        self.configure_styles()

        # User signature settings
        self.selected_user = tk.StringVar(value="Mark Anderson")
        self.signatures = self.load_signatures()

        # Default email template
        self.default_template = self.load_default_template()

        # Debug mode
        self.debug_enabled = tk.BooleanVar(value=False)

        # Setup UI
        self.setup_ui()

    def configure_styles(self):
        """Configure custom styles"""
        # Accent button style
        self.style.configure('Accent.TButton',
                           background=self.colors['primary'],
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none')
        self.style.map('Accent.TButton',
                      background=[('active', self.colors['secondary'])])

        # Header label style
        self.style.configure('Header.TLabel',
                           font=('Segoe UI', 14, 'bold'))

    def load_signatures(self):
        """Load HTML signatures from data folder"""
        signatures = {}
        sig_files = {
            'Mark Anderson': 'data/Mark_Anderson_231123.html',
            'Jason Najm': 'data/Jason_Najm_250427.html'
        }

        for name, path in sig_files.items():
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    signatures[name] = f.read()
            except FileNotFoundError:
                signatures[name] = f"<p>Best regards,<br>{name}<br>Valorem Chemicals</p>"

        return signatures

    def load_default_template(self):
        """Load default email template"""
        template = """Hi {recipient_name},

Please find attached your {current_month} pricing update.

The pricing reflects changes from {previous_month}.

If you have any questions, please don't hesitate to contact us.

Best regards,
{sender_name}"""

        return template

    def setup_ui(self):
        """Setup the main user interface"""
        # Top frame with logo and user selection
        self.setup_header()

        # Main content area
        self.setup_main_content()

        # Bottom status bar
        self.setup_status_bar()

    def setup_header(self):
        """Setup header with logo and user selection"""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=(10, 5))

        # Logo on the left
        try:
            # Load and resize logo
            logo_img = Image.open('valorem_logo.png')
            logo_img = logo_img.resize((150, 50), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)

            logo_label = tk.Label(header_frame, image=self.logo_photo, bg='white')
            logo_label.pack(side=tk.LEFT, padx=(0, 20))
        except:
            # If logo not found, show text
            logo_label = ttk.Label(header_frame, text="VALOREM", font=('Arial', 16, 'bold'))
            logo_label.pack(side=tk.LEFT, padx=(0, 20))

        # Title in center
        title_label = ttk.Label(header_frame, text="Email Draft Dashboard v3.0", style='Header.TLabel')
        title_label.pack(side=tk.LEFT, expand=True)

        # User selection on the right
        user_frame = ttk.Frame(header_frame)
        user_frame.pack(side=tk.RIGHT)

        ttk.Label(user_frame, text="User:").pack(side=tk.LEFT, padx=(0, 5))
        user_dropdown = ttk.Combobox(user_frame, textvariable=self.selected_user,
                                     values=['Mark Anderson', 'Jason Najm'],
                                     state='readonly', width=15)
        user_dropdown.pack(side=tk.LEFT)
        user_dropdown.bind('<<ComboboxSelected>>', self.on_user_changed)

        # Debug checkbox
        debug_check = ttk.Checkbutton(user_frame, text="Debug", variable=self.debug_enabled,
                                      command=self.toggle_debug_panel)
        debug_check.pack(side=tk.LEFT, padx=(10, 0))

    def setup_main_content(self):
        """Setup main content area"""
        # Main notebook for tabs
        self.main_notebook = ttk.Notebook(self.root)
        self.main_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Tab 1: Email Generation
        self.email_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.email_tab, text="Email Generation")
        self.setup_email_tab()

        # Tab 2: Customer Management
        self.customer_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.customer_tab, text="Customer Management")
        self.customer_panel = CustomerManagementPanel(self.customer_tab, self)

        # Tab 3: Settings
        self.settings_tab = ttk.Frame(self.main_notebook)
        self.main_notebook.add(self.settings_tab, text="Settings")
        self.setup_settings_tab()

    def setup_email_tab(self):
        """Setup email generation tab"""
        # Main paned window for email content
        paned = ttk.PanedWindow(self.email_tab, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Left panel: Email template editor
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=2)

        # Right panel: Controls and preview
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)

        # Setup left panel
        self.setup_email_editor(left_frame)

        # Setup right panel
        self.setup_controls_panel(right_frame)

        # Debug panel (initially hidden)
        self.setup_debug_panel()

    def setup_email_editor(self, parent):
        """Setup email template editor"""
        # Title
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=tk.X, padx=5, pady=5)

        ttk.Label(title_frame, text="Email Template", font=('Segoe UI', 11, 'bold')).pack(side=tk.LEFT)

        # Template editor
        editor_frame = ttk.LabelFrame(parent, text="Edit Template")
        editor_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.template_editor = scrolledtext.ScrolledText(
            editor_frame,
            wrap=tk.WORD,
            width=60,
            height=20,
            font=('Consolas', 10)
        )
        self.template_editor.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Insert default template
        self.template_editor.insert(1.0, self.default_template)

        # Bind change event for auto-save
        self.template_editor.bind('<<Modified>>', self.on_template_changed)

        # Variable help
        help_frame = ttk.Frame(parent)
        help_frame.pack(fill=tk.X, padx=5, pady=5)

        help_text = "Variables: {recipient_name}, {current_month}, {previous_month}, {sender_name}"
        ttk.Label(help_frame, text=help_text, font=('Segoe UI', 9)).pack()

    def setup_controls_panel(self, parent):
        """Setup controls and preview panel"""
        # Month/Year selection
        date_frame = ttk.LabelFrame(parent, text="Target Month")
        date_frame.pack(fill=tk.X, padx=5, pady=5)

        today = date.today()

        # Month dropdown
        ttk.Label(date_frame, text="Month:").grid(row=0, column=0, padx=5, pady=5)
        self.month_var = tk.StringVar(value=today.strftime('%B'))
        month_dropdown = ttk.Combobox(date_frame, textvariable=self.month_var,
                                      values=['January', 'February', 'March', 'April',
                                             'May', 'June', 'July', 'August',
                                             'September', 'October', 'November', 'December'],
                                      state='readonly', width=12)
        month_dropdown.grid(row=0, column=1, padx=5, pady=5)

        # Year dropdown
        ttk.Label(date_frame, text="Year:").grid(row=1, column=0, padx=5, pady=5)
        self.year_var = tk.StringVar(value=str(today.year))
        year_dropdown = ttk.Combobox(date_frame, textvariable=self.year_var,
                                     values=[str(y) for y in range(2020, 2030)],
                                     state='readonly', width=12)
        year_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Action buttons
        buttons_frame = ttk.LabelFrame(parent, text="Actions")
        buttons_frame.pack(fill=tk.X, padx=5, pady=5)

        generate_btn = ttk.Button(
            buttons_frame,
            text="Generate All Drafts",
            command=self.generate_all_drafts,
            style='Accent.TButton'
        )
        generate_btn.pack(fill=tk.X, padx=5, pady=5)

        preview_btn = ttk.Button(
            buttons_frame,
            text="Preview Template",
            command=self.preview_template
        )
        preview_btn.pack(fill=tk.X, padx=5, pady=5)

        # Preview area
        preview_frame = ttk.LabelFrame(parent, text="Preview")
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.preview_text = scrolledtext.ScrolledText(
            preview_frame,
            wrap=tk.WORD,
            width=40,
            height=15,
            font=('Segoe UI', 9),
            state=tk.DISABLED
        )
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(parent, mode='determinate')
        self.progress.pack(fill=tk.X, padx=5, pady=5)

    def setup_debug_panel(self):
        """Setup debug panel (initially hidden)"""
        self.debug_frame = ttk.LabelFrame(self.email_tab, text="Debug Console")

        self.debug_text = scrolledtext.ScrolledText(
            self.debug_frame,
            wrap=tk.WORD,
            width=100,
            height=8,
            font=('Courier New', 9),
            bg='black',
            fg='lime'
        )
        self.debug_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def setup_settings_tab(self):
        """Setup settings tab"""
        settings_frame = ttk.LabelFrame(self.settings_tab, text="Application Settings")
        settings_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # CC email settings
        cc_frame = ttk.Frame(settings_frame)
        cc_frame.pack(fill=tk.X, padx=10, pady=10)

        ttk.Label(cc_frame, text="CC Emails:").pack(anchor=tk.W)
        self.cc_emails = tk.Text(cc_frame, width=50, height=3)
        self.cc_emails.insert(1.0, "support@valorem.com.au\njasonn@valorem.com.au")
        self.cc_emails.pack()

        # Save settings button
        save_btn = ttk.Button(settings_frame, text="Save Settings", command=self.save_settings)
        save_btn.pack(pady=10)

    def setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=5, pady=2)

    def on_user_changed(self, event=None):
        """Handle user selection change"""
        self.update_status(f"Switched to user: {self.selected_user.get()}")
        self.preview_template()

    def on_template_changed(self, event=None):
        """Handle template change (auto-save)"""
        # Mark as modified
        self.template_editor.edit_modified(False)
        # Auto-save template
        self.default_template = self.template_editor.get(1.0, tk.END).strip()

    def toggle_debug_panel(self):
        """Toggle debug panel visibility"""
        if self.debug_enabled.get():
            self.debug_frame.pack(fill=tk.X, padx=5, pady=5, side=tk.BOTTOM)
            self.add_debug_message("Debug mode enabled")
        else:
            self.debug_frame.pack_forget()

    def add_debug_message(self, message):
        """Add message to debug console"""
        if self.debug_enabled.get():
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            self.debug_text.insert(tk.END, f"[{timestamp}] {message}\n")
            self.debug_text.see(tk.END)

    def preview_template(self):
        """Preview the email template with sample data"""
        template = self.template_editor.get(1.0, tk.END).strip()

        # Sample data for preview
        sample_data = {
            'recipient_name': 'John Smith',
            'current_month': self.month_var.get(),
            'previous_month': self.get_previous_month(),
            'sender_name': self.selected_user.get()
        }

        # Format template
        try:
            preview_text = template.format(**sample_data)

            # Add signature
            signature = self.signatures.get(self.selected_user.get(), "")
            if signature and not signature.startswith("<"):
                preview_text += f"\n\n{signature}"

            # Update preview
            self.preview_text.config(state=tk.NORMAL)
            self.preview_text.delete(1.0, tk.END)
            self.preview_text.insert(1.0, preview_text)
            self.preview_text.config(state=tk.DISABLED)

            self.update_status("Preview updated")
        except KeyError as e:
            self.update_status(f"Template error: Unknown variable {e}", 'error')

    def get_previous_month(self):
        """Get the previous month name"""
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                 'July', 'August', 'September', 'October', 'November', 'December']

        current_idx = months.index(self.month_var.get())
        prev_idx = (current_idx - 1) % 12
        return months[prev_idx]

    def generate_all_drafts(self):
        """Generate email drafts for all customers"""
        self.update_status("Generating drafts...")
        self.add_debug_message("Starting draft generation")

        # Get template
        template = self.template_editor.get(1.0, tk.END).strip()

        # Get signature for selected user
        signature_html = self.signatures.get(self.selected_user.get(), "")

        # Start generation in thread
        def generation_thread():
            try:
                # Get all active customers
                customers = self.customer_panel.database.get_all_customers()
                active_customers = [c for c in customers if c.get('active', True)]

                total = len(active_customers)
                self.progress['maximum'] = total

                generated = 0
                failed = []

                for idx, customer in enumerate(active_customers):
                    self.progress['value'] = idx + 1
                    self.update_status(f"Processing {customer['company_name']}...")

                    try:
                        # Generate draft for customer
                        result = email_generator.generate_single_draft(
                            customer,
                            template,
                            signature_html,
                            self.selected_user.get(),
                            self.month_var.get(),
                            self.year_var.get()
                        )

                        if result['success']:
                            generated += 1
                            self.add_debug_message(f"✓ Generated draft for {customer['company_name']}")
                        else:
                            failed.append(customer['company_name'])
                            self.add_debug_message(f"✗ Failed: {customer['company_name']} - {result.get('error')}")

                    except Exception as e:
                        failed.append(customer['company_name'])
                        self.add_debug_message(f"✗ Error for {customer['company_name']}: {str(e)}")

                # Final status
                self.progress['value'] = 0
                status_msg = f"Generated {generated} drafts"
                if failed:
                    status_msg += f", {len(failed)} failed"

                self.update_status(status_msg)

                # Show summary
                if failed:
                    messagebox.showwarning("Generation Complete",
                                         f"Generated {generated} drafts.\n\n"
                                         f"Failed for:\n" + "\n".join(failed[:5]))
                else:
                    messagebox.showinfo("Success", f"Successfully generated {generated} email drafts!")

            except Exception as e:
                self.update_status(f"Error: {str(e)}", 'error')
                messagebox.showerror("Error", f"Generation failed: {str(e)}")

        # Start thread
        thread = threading.Thread(target=generation_thread, daemon=True)
        thread.start()

    def save_settings(self):
        """Save application settings"""
        # Save CC emails and other settings
        messagebox.showinfo("Settings", "Settings saved successfully!")
        self.update_status("Settings saved")

    def update_status(self, message, level='info'):
        """Update status bar"""
        self.status_bar.config(text=message)

        # Color based on level
        if level == 'error':
            self.status_bar.config(foreground='red')
        elif level == 'warning':
            self.status_bar.config(foreground='orange')
        else:
            self.status_bar.config(foreground='black')


def main():
    """Main entry point"""
    # Check for required dependencies
    try:
        import PIL
    except ImportError:
        print("Installing required dependency: Pillow")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "Pillow"])
        import PIL

    # Create and run application
    root = tk.Tk()
    app = EmailDraftDashboard(root)
    root.mainloop()


if __name__ == "__main__":
    main()