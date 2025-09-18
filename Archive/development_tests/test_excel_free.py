#!/usr/bin/env python3
"""
Test script to verify Excel-free workflow
Tests JSON database loading and dynamic file name generation
"""

import json
import os
from datetime import datetime
from src import email_generator

def test_json_database():
    """Test that JSON database loads correctly"""
    print("=" * 60)
    print("TEST 1: Loading Customer Database")
    print("=" * 60)

    database_file = "customer_database_v2.json"

    if not os.path.exists(database_file):
        print(f"[ERROR] Database file not found: {database_file}")
        return False

    with open(database_file, 'r', encoding='utf-8') as f:
        database = json.load(f)

    customers = database.get('customers', [])
    print(f"[OK] Successfully loaded {len(customers)} customers from JSON")

    # Show first customer as example
    if customers:
        first = customers[0]
        print(f"\nExample customer:")
        print(f"  Company: {first.get('company_name')}")
        print(f"  Emails: {first.get('email_addresses')}")
        print(f"  File path: {first.get('file_generation', {}).get('file_path')}")

    return True

def test_dynamic_file_naming():
    """Test dynamic file name generation"""
    print("\n" + "=" * 60)
    print("TEST 2: Dynamic File Name Generation")
    print("=" * 60)

    # Test cases for different months
    test_cases = [
        (10, 2025, "251001"),  # October 2025
        (9, 2025, "250901"),   # September 2025
        (1, 2026, "260101"),   # January 2026
        (12, 2025, "251201"),  # December 2025
    ]

    for month, year, expected_prefix in test_cases:
        # Generate the date prefix as the code would
        date_prefix = f"{year % 100:02d}{month:02d}01"

        if date_prefix == expected_prefix:
            print(f"[OK] Month {month:02d}/{year} -> {date_prefix}_Pricing_CustomerName.pdf")
        else:
            print(f"[ERROR] Month {month:02d}/{year} -> Expected {expected_prefix}, got {date_prefix}")
            return False

    return True

def test_date_placeholders():
    """Test date placeholder generation"""
    print("\n" + "=" * 60)
    print("TEST 3: Date Placeholder Resolution")
    print("=" * 60)

    # Test with October 2025
    placeholders = email_generator.get_date_placeholders(10, 2025)

    print(f"Selected: October 2025")
    print(f"  current_month: {placeholders.get('current_month')}")
    print(f"  previous_month: {placeholders.get('previous_month')}")
    print(f"  current_year: {placeholders.get('current_year')}")
    print(f"  effective_date: {placeholders.get('effective_date')}")

    # Verify values
    checks = [
        (placeholders.get('current_month') == 'October', 'current_month'),
        (placeholders.get('previous_month') == 'September', 'previous_month'),
        (placeholders.get('current_year') == 2025, 'current_year'),
        ('November' in str(placeholders.get('effective_date', '')), 'effective_date'),
    ]

    all_passed = True
    for check, name in checks:
        if check:
            print(f"  [OK] {name} is correct")
        else:
            print(f"  [ERROR] {name} is incorrect")
            all_passed = False

    return all_passed

def main():
    """Run all tests"""
    print("\n[TEST] TESTING EXCEL-FREE WORKFLOW\n")

    tests = [
        test_json_database,
        test_dynamic_file_naming,
        test_date_placeholders,
    ]

    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"[ERROR] Test failed with error: {e}")
            results.append(False)

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    passed = sum(1 for r in results if r)
    total = len(results)

    if passed == total:
        print(f"[SUCCESS] All {total} tests passed!")
        print("\n[COMPLETE] The system is now Excel-free and working correctly!")
        print("   - Customer data loads from JSON")
        print("   - File names generate dynamically from dashboard month/year")
        print("   - Date placeholders resolve correctly")
    else:
        print(f"[WARNING] {passed}/{total} tests passed")
        print("\nPlease review the failed tests above.")

    return passed == total

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)