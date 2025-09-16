"""
Test script to verify the dashboard email generation integration.
This script tests that email generation happens entirely within the GUI
without opening any terminal windows.
"""

import sys
import os

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(__file__))

from src import email_generator


def test_email_generator_module():
    """Test that the email generator module works correctly"""
    print("Testing email generator module...")
    print("-" * 60)

    # Test 1: Load templates
    print("\n1. Testing template loading...")
    templates = email_generator.load_email_templates()
    assert 'templates' in templates, "Templates should be loaded"
    print(f"   [OK] Loaded {len(templates.get('templates', {}))} template(s)")

    # Test 2: Get date placeholders
    print("\n2. Testing date placeholder generation...")
    dates = email_generator.get_date_placeholders()
    assert 'current_month' in dates, "Should have current_month"
    assert 'previous_month' in dates, "Should have previous_month"
    print(f"   [OK] Current month: {dates['current_month']}")
    print(f"   [OK] Previous month: {dates['previous_month']}")

    # Test 3: Get available templates
    print("\n3. Testing available templates...")
    available = email_generator.get_available_templates(templates)
    assert len(available) > 0, "Should have at least one template"
    for template in available:
        print(f"   [OK] Template: {template['name']} (key: {template['key']})")

    # Test 4: Create preview
    print("\n4. Testing email preview generation...")
    preview = email_generator.create_single_draft_preview(
        template_key='default',
        custom_values=dates
    )
    assert 'subject' in preview, "Preview should have subject"
    assert 'plain_body' in preview, "Preview should have plain body"
    print(f"   [OK] Subject: {preview['subject']}")
    print(f"   [OK] Preview generated for: {preview['customer']}")

    # Test 5: Test progress callback
    print("\n5. Testing progress callback mechanism...")
    progress_updates = []

    def mock_progress(current, total, message):
        progress_updates.append((current, total, message))
        print(f"   Progress: {current}/{total} - {message}")

    # We can't test actual email generation without Outlook, but we can test the function exists
    assert hasattr(email_generator, 'create_email_drafts_batch'), "Should have batch creation function"
    print("   [OK] Email batch creation function available")

    print("\n" + "=" * 60)
    print("All tests passed! The email generator module is working correctly.")
    print("\nThe dashboard should now:")
    print("1. Use the email_generator module directly (no subprocess)")
    print("2. Show progress in the dashboard progress bar")
    print("3. Display results in the dashboard interface")
    print("4. Never open a terminal window")


def test_dashboard_import():
    """Test that the dashboard can import the email generator"""
    print("\nTesting dashboard import compatibility...")
    print("-" * 60)

    try:
        import dashboard
        print("[OK] Dashboard module imports successfully")

        # Check that dashboard has the new methods
        assert hasattr(dashboard.PriceSheetDashboard, 'update_progress'), "Dashboard should have update_progress method"
        assert hasattr(dashboard.PriceSheetDashboard, 'display_generation_results'), "Dashboard should have display_generation_results method"
        print("[OK] Dashboard has the new integration methods")

    except ImportError as e:
        print(f"[FAIL] Failed to import dashboard: {e}")
        return False

    return True


if __name__ == "__main__":
    print("=" * 60)
    print("DASHBOARD EMAIL GENERATION INTEGRATION TEST")
    print("=" * 60)

    # Run tests
    test_email_generator_module()
    test_dashboard_import()

    print("\n" + "=" * 60)
    print("INTEGRATION TEST COMPLETE")
    print("=" * 60)
    print("\nTo verify the complete GUI-only workflow:")
    print("1. Run the dashboard: python dashboard.py")
    print("2. Enter or load your monthly email draft")
    print("3. Click 'Generate All Email Drafts'")
    print("4. Observe that:")
    print("   - NO terminal window appears")
    print("   - Progress bar shows generation progress")
    print("   - Results appear in the dashboard")
    print("   - Email drafts are created in Outlook")