"""
Test script to verify the COM initialization fix for Outlook.
This tests that email generation works correctly in a background thread.
"""

import sys
import os
import threading
import time

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from src import email_generator


def test_direct_call():
    """Test email generation with direct call (main thread)"""
    print("=" * 60)
    print("TEST 1: Direct Call (Main Thread)")
    print("=" * 60)

    try:
        # Test with minimal parameters
        results = email_generator.create_email_drafts_batch(
            template_key='default',
            custom_values={'month': 'Test'},
            progress_callback=lambda c, t, m: print(f"Progress: {c}/{t} - {m}")
        )

        print("\nResults:")
        print(f"Success: {results['success']}")
        print(f"Drafts created: {results['drafts_created']}")
        print(f"Errors: {len(results['errors'])}")
        if results['errors']:
            for error in results['errors']:
                print(f"  - {error}")
        print(f"Debug log: {results.get('debug_log', 'N/A')}")

        return results['success']

    except Exception as e:
        print(f"[FAIL] Direct call failed: {str(e)}")
        return False


def test_background_thread():
    """Test email generation in background thread (simulates dashboard)"""
    print("\n" + "=" * 60)
    print("TEST 2: Background Thread (Dashboard Simulation)")
    print("=" * 60)

    results_container = {'result': None, 'completed': False}

    def run_in_background():
        """Function to run in background thread"""
        try:
            print("Starting generation in background thread...")
            results = email_generator.create_email_drafts_batch(
                template_key='dashboard_custom',
                custom_values={'month': 'Test'},
                progress_callback=lambda c, t, m: print(f"  Thread Progress: {c}/{t} - {m}")
            )
            results_container['result'] = results
            results_container['completed'] = True
            print("Background thread completed.")

        except Exception as e:
            print(f"[FAIL] Background thread error: {str(e)}")
            results_container['result'] = {
                'success': False,
                'errors': [str(e)],
                'drafts_created': 0
            }
            results_container['completed'] = True

    # Start the background thread
    thread = threading.Thread(target=run_in_background, daemon=True)
    thread.start()

    # Wait for completion (max 30 seconds)
    timeout = 30
    start_time = time.time()
    while not results_container['completed'] and (time.time() - start_time) < timeout:
        time.sleep(0.5)

    if not results_container['completed']:
        print("[FAIL] Background thread timed out")
        return False

    # Check results
    results = results_container['result']
    if results:
        print("\nBackground Thread Results:")
        print(f"Success: {results['success']}")
        print(f"Drafts created: {results['drafts_created']}")
        print(f"Errors: {len(results['errors'])}")
        if results['errors']:
            for error in results['errors']:
                print(f"  - {error[:200]}...")  # Truncate long errors
        print(f"Debug log: {results.get('debug_log', 'N/A')}")

        return results['success']

    return False


def main():
    """Main test function"""
    print("COM INITIALIZATION FIX TEST")
    print("=" * 60)
    print("This test verifies that Outlook COM objects work correctly")
    print("in background threads (fixing the CoInitialize error).")
    print()

    # Run tests
    test1_passed = test_direct_call()
    test2_passed = test_background_thread()

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Test 1 (Direct Call):      {'[PASS]' if test1_passed else '[FAIL]'}")
    print(f"Test 2 (Background Thread): {'[PASS]' if test2_passed else '[FAIL]'}")

    if test1_passed and test2_passed:
        print("\n[OK] All tests passed! The COM initialization fix is working.")
        print("\nThe dashboard should now work without opening terminal windows:")
        print("- Email generation runs in background thread")
        print("- COM is properly initialized with pythoncom.CoInitialize()")
        print("- Progress updates appear in the dashboard")
        print("- Results display in the dashboard interface")
    else:
        print("\n[FAIL] Some tests failed. Check the debug logs for details.")
        print("\nTroubleshooting:")
        print("1. Check that Outlook is installed and configured")
        print("2. Verify Excel file exists and has correct format")
        print("3. Review debug logs in the 'logs' directory")


if __name__ == "__main__":
    main()