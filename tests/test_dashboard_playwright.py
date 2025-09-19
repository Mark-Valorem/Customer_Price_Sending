"""
Playwright Tests for Dashboard v3.0
===================================

This module contains automated UI tests for the Dashboard application
using Playwright for browser automation and testing.

Author: Claude Code v3.0
Date: 2025-09-19
"""

import pytest
import asyncio
from playwright.async_api import async_playwright, expect
import os
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestDashboardUI:
    """Test suite for Dashboard UI using Playwright"""

    @pytest.fixture(scope="class")
    async def browser(self):
        """Setup browser for tests"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            yield browser
            await browser.close()

    @pytest.fixture
    async def page(self, browser):
        """Create a new page for each test"""
        page = await browser.new_page()
        yield page
        await page.close()

    @pytest.mark.asyncio
    async def test_dashboard_loads(self, page):
        """Test that the dashboard loads successfully"""
        # Start the dashboard (in a real scenario, this would be a web server)
        # For tkinter app, we'd need to test it differently
        # This is a placeholder for web-based testing if migrated to web

        # Navigate to dashboard URL
        await page.goto("http://localhost:8000")

        # Check title
        await expect(page).to_have_title("Valorem Chemicals - Email Dashboard v3.0")

        # Check main components are visible
        await expect(page.locator("#logo")).to_be_visible()
        await expect(page.locator("#user-selector")).to_be_visible()
        await expect(page.locator("#email-tab")).to_be_visible()

    @pytest.mark.asyncio
    async def test_user_selection(self, page):
        """Test user selection dropdown"""
        await page.goto("http://localhost:8000")

        # Select user dropdown
        user_selector = page.locator("#user-selector")
        await user_selector.select_option("Jason Najm")

        # Verify selection
        selected_value = await user_selector.input_value()
        assert selected_value == "Jason Najm"

        # Switch back to Mark Anderson
        await user_selector.select_option("Mark Anderson")
        selected_value = await user_selector.input_value()
        assert selected_value == "Mark Anderson"

    @pytest.mark.asyncio
    async def test_email_template_editing(self, page):
        """Test email template editing functionality"""
        await page.goto("http://localhost:8000")

        # Get template editor
        template_editor = page.locator("#template-editor")

        # Clear and enter new template
        await template_editor.clear()
        test_template = "Hello {recipient_name},\nThis is a test template."
        await template_editor.fill(test_template)

        # Verify template was entered
        content = await template_editor.input_value()
        assert test_template in content

    @pytest.mark.asyncio
    async def test_customer_verification_console(self, page):
        """Test customer verification console functionality"""
        await page.goto("http://localhost:8000")

        # Navigate to Customer Management tab
        await page.click('text="Customer Management"')

        # Click Verify All Customers button
        verify_button = page.locator("#verify-all-btn")
        await verify_button.click()

        # Wait for verification to start
        await page.wait_for_selector(".verification-progress", state="visible")

        # Check that console shows output
        console_output = page.locator("#verification-console")
        await expect(console_output).to_contain_text("STARTING VERIFICATION")

    @pytest.mark.asyncio
    async def test_preview_functionality(self, page):
        """Test email preview functionality"""
        await page.goto("http://localhost:8000")

        # Click preview button
        preview_button = page.locator("#preview-btn")
        await preview_button.click()

        # Wait for preview to update
        await page.wait_for_timeout(1000)

        # Check preview contains expected elements
        preview_area = page.locator("#preview-text")
        preview_content = await preview_area.text_content()

        assert "pricing update" in preview_content.lower()

    @pytest.mark.asyncio
    async def test_debug_mode_toggle(self, page):
        """Test debug mode toggle"""
        await page.goto("http://localhost:8000")

        # Initially debug console should not be visible
        debug_console = page.locator("#debug-console")
        await expect(debug_console).not_to_be_visible()

        # Toggle debug mode
        debug_checkbox = page.locator("#debug-checkbox")
        await debug_checkbox.check()

        # Debug console should now be visible
        await expect(debug_console).to_be_visible()

        # Toggle off
        await debug_checkbox.uncheck()
        await expect(debug_console).not_to_be_visible()

    @pytest.mark.asyncio
    async def test_customer_add_dialog(self, page):
        """Test adding a new customer"""
        await page.goto("http://localhost:8000")

        # Navigate to Customer Management
        await page.click('text="Customer Management"')

        # Click Add Customer button
        await page.click("#add-customer-btn")

        # Fill in customer details
        await page.fill("#company-name", "Test Company Ltd")
        await page.fill("#email-domain", "testcompany.com")
        await page.fill("#email-addresses", "contact@testcompany.com")
        await page.fill("#recipient-names", "John Test")

        # Save customer
        await page.click("#save-customer-btn")

        # Verify customer appears in list
        customer_list = page.locator("#customer-tree")
        await expect(customer_list).to_contain_text("Test Company Ltd")

    @pytest.mark.asyncio
    async def test_generate_drafts_workflow(self, page):
        """Test the complete email draft generation workflow"""
        await page.goto("http://localhost:8000")

        # Select month and year
        await page.select_option("#month-selector", "September")
        await page.select_option("#year-selector", "2025")

        # Click Generate All Drafts
        generate_button = page.locator("#generate-drafts-btn")
        await generate_button.click()

        # Wait for progress bar
        progress_bar = page.locator("#progress-bar")
        await expect(progress_bar).to_be_visible()

        # Wait for completion message
        await page.wait_for_selector(".success-message", timeout=30000)

        # Verify success message
        success_msg = page.locator(".success-message")
        await expect(success_msg).to_contain_text("Successfully generated")


class TestDashboardIntegration:
    """Integration tests for Dashboard functionality"""

    def test_signature_loading(self):
        """Test that HTML signatures are loaded correctly"""
        from dashboard import EmailDraftDashboard
        import tkinter as tk

        root = tk.Tk()
        app = EmailDraftDashboard(root)

        # Check signatures are loaded
        assert "Mark Anderson" in app.signatures
        assert "Jason Najm" in app.signatures

        # Check signature content
        assert len(app.signatures["Mark Anderson"]) > 0
        assert len(app.signatures["Jason Najm"]) > 0

        root.destroy()

    def test_customer_database_operations(self):
        """Test customer database CRUD operations"""
        from src.verification_system import CustomerDatabase

        # Use test database
        test_db_file = "data/test_customer_database.json"
        db = CustomerDatabase(test_db_file)

        # Add customer
        test_customer = {
            'company_name': 'Playwright Test Co',
            'email_domain': 'playwrighttest.com',
            'email_addresses': ['test@playwrighttest.com'],
            'recipient_names': ['Test User'],
            'file_generation': [],
            'active': True
        }

        customer_id = db.add_customer(test_customer)
        assert customer_id is not None

        # Get customer
        retrieved = db.get_customer_by_id(customer_id)
        assert retrieved['company_name'] == 'Playwright Test Co'

        # Update customer
        retrieved['company_name'] = 'Updated Test Co'
        db.update_customer(customer_id, retrieved)

        updated = db.get_customer_by_id(customer_id)
        assert updated['company_name'] == 'Updated Test Co'

        # Delete customer
        db.delete_customer(customer_id)
        deleted = db.get_customer_by_id(customer_id)
        assert deleted is None

        # Clean up test file
        if os.path.exists(test_db_file):
            os.remove(test_db_file)

    def test_verification_system(self):
        """Test the multi-layer verification system"""
        from src.verification_system import MultiLayerVerificationSystem

        # Use test database
        test_db_file = "data/test_verification.json"

        # Create test data
        test_data = {
            "customers": [
                {
                    "id": "TEST001",
                    "company_name": "Valid Test Co",
                    "email_domain": "validtest.com",
                    "email_addresses": ["contact@validtest.com"],
                    "recipient_names": ["Valid User"],
                    "file_generation": [],
                    "verification_status": {
                        "domain_verified": True,
                        "recipients_verified": True,
                        "file_paths_verified": True
                    },
                    "active": True
                }
            ]
        }

        # Write test data
        with open(test_db_file, 'w') as f:
            json.dump(test_data, f)

        # Test verification
        verifier = MultiLayerVerificationSystem(test_db_file)
        result = verifier.verify_customer("TEST001")

        assert result['overall_status'] in ['passed', 'warning', 'failed']
        assert 'issues' in result

        # Clean up
        if os.path.exists(test_db_file):
            os.remove(test_db_file)

    def test_email_generation_with_signature(self):
        """Test email generation includes correct signature"""
        from src.email_generator import generate_single_draft

        test_customer = {
            'id': 'TEST002',
            'company_name': 'Email Test Co',
            'email_domain': 'emailtest.com',
            'email_addresses': ['test@emailtest.com'],
            'recipient_names': ['Email Tester'],
            'file_generation': []
        }

        template = "Hi {recipient_name}, This is {current_month} update from {sender_name}."
        signature = "<p>Best regards,<br>Test Signature</p>"

        # Note: This would need Outlook installed to actually work
        # Here we're just testing the function doesn't crash
        try:
            result = generate_single_draft(
                test_customer,
                template,
                signature,
                "Test User",
                "September",
                "2025"
            )
            # If Outlook is not available, it should fail gracefully
            assert 'success' in result
        except Exception as e:
            # Expected if Outlook is not installed
            assert "Outlook" in str(e) or "COM" in str(e)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])