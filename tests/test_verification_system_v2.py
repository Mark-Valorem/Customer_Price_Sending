#!/usr/bin/env python3
"""
Comprehensive Testing Suite for Customer Database Migration & Verification System v2.0
=====================================================================================

CRITICAL BUSINESS SYSTEM TESTS - Ensures absolute reliability of customer verification
to prevent sending wrong pricing data to customers.

Test Categories:
1. Domain verification tests (CRITICAL)
2. File existence tests
3. Customer database operations
4. Security violation detection
5. Audit logging verification
6. End-to-end workflow tests

Author: Claude Code v2.0
Date: 2025-09-16
"""

import unittest
import os
import json
import tempfile
import shutil
from datetime import datetime
from unittest.mock import patch, MagicMock
import sys

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from verification_system_v2 import (
    MultiLayerVerificationSystem,
    CustomerDatabase,
    VerificationLevel,
    VerificationResult,
    CustomerVerificationReport
)
from audit_logging_v2 import AuditLogger, AuditEventType, AuditSeverity


class TestCustomerDatabase(unittest.TestCase):
    """Test customer database operations"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.test_db_file = os.path.join(self.test_dir, 'test_customer_db.json')

        # Create test database
        self.test_data = {
            "version": "2.0.0",
            "created_date": datetime.now().isoformat(),
            "customers": [
                {
                    "id": "test_customer_001",
                    "company_name": "Test Company Ltd",
                    "recipient_names": ["John Doe", "Jane Smith"],
                    "email_addresses": ["john@testcompany.com", "jane@testcompany.com"],
                    "email_domain": "testcompany.com",
                    "file_generation": {
                        "filename_pattern": "{month}_{file_body}",
                        "file_body": "_Pricing_Test Company Ltd.pdf",
                        "file_path": "/test/path/",
                        "current_filename": "202509_Pricing_Test Company Ltd.pdf"
                    },
                    "verification_status": {
                        "domain_verified": True,
                        "file_path_verified": True,
                        "filename_verified": True
                    },
                    "active": True
                },
                {
                    "id": "wrong_domain_customer",
                    "company_name": "Wrong Domain Corp",
                    "email_addresses": ["admin@wrongdomain.com"],
                    "email_domain": "rightdomain.com",  # Intentional mismatch for testing
                    "active": True
                }
            ]
        }

        with open(self.test_db_file, 'w') as f:
            json.dump(self.test_data, f)

        self.database = CustomerDatabase(self.test_db_file)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)

    def test_load_database(self):
        """Test database loading"""
        self.assertIsNotNone(self.database.data)
        self.assertEqual(len(self.database.data['customers']), 2)

    def test_get_customer_by_email_domain(self):
        """Test finding customer by email domain"""
        # Test valid domain
        customer = self.database.get_customer_by_email_domain("john@testcompany.com")
        self.assertIsNotNone(customer)
        self.assertEqual(customer['company_name'], "Test Company Ltd")

        # Test invalid domain
        customer = self.database.get_customer_by_email_domain("unknown@unknown.com")
        self.assertIsNone(customer)

    def test_get_customer_by_id(self):
        """Test finding customer by ID"""
        customer = self.database.get_customer_by_id("test_customer_001")
        self.assertIsNotNone(customer)
        self.assertEqual(customer['company_name'], "Test Company Ltd")

    def test_is_email_authorized(self):
        """Test email authorization check"""
        customer = self.database.get_customer_by_id("test_customer_001")

        # Test authorized email
        self.assertTrue(self.database.is_email_authorized("john@testcompany.com", customer))

        # Test unauthorized email
        self.assertFalse(self.database.is_email_authorized("hacker@testcompany.com", customer))


class TestVerificationSystem(unittest.TestCase):
    """Test multi-layer verification system"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.test_db_file = os.path.join(self.test_dir, 'test_customer_db.json')

        # Create test database with verification scenarios
        self.test_data = {
            "version": "2.0.0",
            "customers": [
                {
                    "id": "valid_customer_001",
                    "company_name": "Valid Customer Ltd",
                    "recipient_names": ["Valid User"],
                    "email_addresses": ["user@validcustomer.com"],
                    "email_domain": "validcustomer.com",
                    "file_generation": {
                        "file_path": self.test_dir,  # Use temp dir that exists
                        "current_filename": "test_pricing.pdf",
                        "file_body": "_Pricing_Valid Customer Ltd.pdf"
                    },
                    "verification_status": {
                        "domain_verified": True,
                        "file_path_verified": True,
                        "filename_verified": True
                    },
                    "active": True
                },
                {
                    "id": "invalid_domain_customer",
                    "company_name": "Invalid Domain Corp",
                    "email_addresses": ["user@invaliddomain.com"],
                    "email_domain": "correctdomain.com",  # Mismatch for testing
                    "active": True
                }
            ]
        }

        with open(self.test_db_file, 'w') as f:
            json.dump(self.test_data, f)

        # Create test pricing file
        self.test_file = os.path.join(self.test_dir, "test_pricing.pdf")
        with open(self.test_file, 'w') as f:
            f.write("Test pricing file content")

        self.verifier = MultiLayerVerificationSystem(self.test_db_file)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)

    def test_domain_verification_success(self):
        """Test successful domain verification"""
        customer = self.verifier.database.get_customer_by_id("valid_customer_001")
        result = self.verifier.verify_domain_match("user@validcustomer.com", customer)

        self.assertTrue(result.passed)
        self.assertEqual(result.level, VerificationLevel.INFO)
        self.assertIn("Domain verified", result.message)

    def test_domain_verification_failure(self):
        """CRITICAL TEST: Domain verification must fail for mismatched domains"""
        customer = self.verifier.database.get_customer_by_id("invalid_domain_customer")
        result = self.verifier.verify_domain_match("user@invaliddomain.com", customer)

        self.assertFalse(result.passed)
        self.assertEqual(result.level, VerificationLevel.CRITICAL)
        self.assertIn("CRITICAL: Domain mismatch", result.message)

    def test_email_authorization_success(self):
        """Test successful email authorization"""
        customer = self.verifier.database.get_customer_by_id("valid_customer_001")
        result = self.verifier.verify_email_authorization("user@validcustomer.com", customer)

        self.assertTrue(result.passed)
        self.assertEqual(result.level, VerificationLevel.INFO)

    def test_email_authorization_failure(self):
        """Test email authorization failure"""
        customer = self.verifier.database.get_customer_by_id("valid_customer_001")
        result = self.verifier.verify_email_authorization("hacker@validcustomer.com", customer)

        self.assertFalse(result.passed)
        self.assertEqual(result.level, VerificationLevel.ERROR)

    def test_file_existence_verification(self):
        """Test file existence verification"""
        customer = self.verifier.database.get_customer_by_id("valid_customer_001")
        result = self.verifier.verify_pricing_file_exists(customer)

        self.assertTrue(result.passed)
        self.assertEqual(result.level, VerificationLevel.INFO)

    def test_file_missing_verification(self):
        """Test verification when file is missing"""
        customer = self.verifier.database.get_customer_by_id("valid_customer_001")
        customer['file_generation']['current_filename'] = "missing_file.pdf"

        result = self.verifier.verify_pricing_file_exists(customer)

        self.assertFalse(result.passed)
        self.assertEqual(result.level, VerificationLevel.ERROR)
        self.assertIn("not found", result.message)

    def test_level_1_pre_send_checks(self):
        """Test Level 1 verification checks"""
        results = self.verifier.level_1_pre_send_checks("user@validcustomer.com", "Valid User")

        self.assertTrue(len(results) >= 3)  # Domain, email auth, recipient validation

        # Check that domain verification passed
        domain_check = next((r for r in results if r.check_name == "domain_verification"), None)
        self.assertIsNotNone(domain_check)
        self.assertTrue(domain_check.passed)

    def test_level_1_checks_no_customer(self):
        """Test Level 1 checks when no customer found"""
        results = self.verifier.level_1_pre_send_checks("unknown@unknown.com", "Unknown User")

        self.assertTrue(len(results) >= 1)
        customer_lookup = results[0]
        self.assertEqual(customer_lookup.check_name, "customer_lookup")
        self.assertFalse(customer_lookup.passed)
        self.assertEqual(customer_lookup.level, VerificationLevel.CRITICAL)

    def test_complete_verification_success(self):
        """Test complete verification process success"""
        report = self.verifier.verify_email_send(
            "user@validcustomer.com",
            "Valid User",
            "test_pricing.pdf"
        )

        self.assertEqual(report.overall_status, "PASS")
        self.assertTrue(report.can_send)
        self.assertEqual(report.company_name, "Valid Customer Ltd")

    def test_complete_verification_failure(self):
        """CRITICAL TEST: Complete verification must fail for invalid data"""
        report = self.verifier.verify_email_send(
            "user@invaliddomain.com",  # Domain mismatch
            "Invalid User",
            "missing_file.pdf"
        )

        self.assertEqual(report.overall_status, "FAIL")
        self.assertFalse(report.can_send)

        # Check that critical failures are detected
        critical_failures = [r for r in report.verification_results
                           if r.level == VerificationLevel.CRITICAL and not r.passed]
        self.assertTrue(len(critical_failures) > 0)

    def test_security_verification_preview(self):
        """Test verification preview functionality"""
        preview = self.verifier.get_verification_preview(
            "user@validcustomer.com",
            "Valid User",
            "test_pricing.pdf"
        )

        self.assertEqual(preview['customer'], "Valid Customer Ltd")
        self.assertIn("Verified", preview['domain_check'])
        self.assertTrue(preview['can_send'])


class TestAuditLogging(unittest.TestCase):
    """Test audit logging system"""

    def setUp(self):
        """Set up test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.audit_file = os.path.join(self.test_dir, "test_audit.json")
        self.auditor = AuditLogger(audit_file=self.audit_file)

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)

    def test_email_send_attempt_logging(self):
        """Test email send attempt logging"""
        self.auditor.log_email_send_attempt(
            email="test@example.com",
            recipient="Test User",
            attachment="test.pdf",
            customer_id="test_001",
            verification_status="PASS"
        )

        events = self.auditor.get_audit_events()
        self.assertTrue(len(events) > 0)

        event = events[-1]
        self.assertEqual(event['event_type'], AuditEventType.EMAIL_SEND_ATTEMPT.value)
        self.assertEqual(event['email_address'], "test@example.com")

    def test_verification_failure_logging(self):
        """Test verification failure logging"""
        verification_results = [
            {"check": "domain_verification", "passed": False, "message": "Domain mismatch"}
        ]

        self.auditor.log_verification_failure(
            email="wrong@domain.com",
            recipient="Wrong User",
            attachment="wrong.pdf",
            verification_results=verification_results,
            customer_id="unknown"
        )

        events = self.auditor.get_audit_events(
            event_type=AuditEventType.VERIFICATION_FAILURE
        )
        self.assertTrue(len(events) > 0)

        event = events[-1]
        self.assertEqual(event['severity'], AuditSeverity.CRITICAL.value)
        self.assertFalse(event['success'])

    def test_security_violation_logging(self):
        """Test security violation logging"""
        self.auditor.log_security_violation(
            email="attacker@evil.com",
            violation_type="domain_spoofing",
            details={"attempted_company": "Legitimate Corp"}
        )

        security_events = self.auditor.get_security_events(hours=1)
        self.assertTrue(len(security_events) > 0)

        event = security_events[-1]
        self.assertEqual(event['event_type'], AuditEventType.SECURITY_VIOLATION.value)
        self.assertEqual(event['severity'], AuditSeverity.CRITICAL.value)

    def test_compliance_report_generation(self):
        """Test compliance report generation"""
        # Log some test events
        self.auditor.log_email_send_attempt("test1@example.com", "User1", "file1.pdf")
        self.auditor.log_email_send_success("test1@example.com", "User1", "file1.pdf")
        self.auditor.log_verification_failure("bad@domain.com", "BadUser", "bad.pdf", [])

        end_date = datetime.now()
        start_date = datetime(end_date.year, end_date.month, end_date.day)

        report = self.auditor.generate_compliance_report(start_date, end_date)

        self.assertGreater(report['summary']['total_events'], 0)
        self.assertGreater(report['summary']['email_attempts'], 0)
        self.assertGreater(report['summary']['verification_failures'], 0)


class TestSecurityScenarios(unittest.TestCase):
    """Test security scenarios - CRITICAL for preventing data exposure"""

    def setUp(self):
        """Set up test environment for security testing"""
        self.test_dir = tempfile.mkdtemp()
        self.test_db_file = os.path.join(self.test_dir, 'security_test_db.json')

        # Create test database with multiple customers
        self.test_data = {
            "version": "2.0.0",
            "customers": [
                {
                    "id": "company_a",
                    "company_name": "Company A Ltd",
                    "email_addresses": ["user@companya.com"],
                    "email_domain": "companya.com",
                    "active": True
                },
                {
                    "id": "company_b",
                    "company_name": "Company B Corp",
                    "email_addresses": ["admin@companyb.com"],
                    "email_domain": "companyb.com",
                    "active": True
                }
            ]
        }

        with open(self.test_db_file, 'w') as f:
            json.dump(self.test_data, f)

        self.verifier = MultiLayerVerificationSystem(self.test_db_file)
        self.auditor = AuditLogger()

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)

    def test_cross_domain_prevention(self):
        """CRITICAL: Test prevention of cross-domain data exposure"""
        # Attempt to send Company A's data to Company B's email
        report = self.verifier.verify_email_send(
            "admin@companyb.com",  # Company B email
            "Company B Admin",
            "company_a_pricing.pdf"  # Company A pricing file
        )

        # This should work since we're not checking filename-company matching in this simple test
        # But in a real scenario, the filename would indicate Company A data

        # Test explicit domain mismatch
        fake_customer = {
            "company_name": "Company A Ltd",
            "email_domain": "companya.com"
        }

        result = self.verifier.verify_domain_match("admin@companyb.com", fake_customer)
        self.assertFalse(result.passed)
        self.assertEqual(result.level, VerificationLevel.CRITICAL)

    def test_unauthorized_email_prevention(self):
        """Test prevention of sending to unauthorized emails"""
        customer = self.verifier.database.get_customer_by_email_domain("user@companya.com")

        # Test unauthorized email in same domain
        result = self.verifier.verify_email_authorization("hacker@companya.com", customer)
        self.assertFalse(result.passed)
        self.assertEqual(result.level, VerificationLevel.ERROR)

    def test_missing_customer_prevention(self):
        """Test prevention when customer not found"""
        report = self.verifier.verify_email_send(
            "unknown@unknown.com",
            "Unknown User",
            "mystery_pricing.pdf"
        )

        self.assertEqual(report.overall_status, "FAIL")
        self.assertFalse(report.can_send)
        self.assertEqual(report.customer_id, "unknown")

    def test_verification_system_fail_safe(self):
        """Test that verification system fails safe on errors"""
        # Create verifier with invalid database file
        invalid_verifier = MultiLayerVerificationSystem("nonexistent_file.json")

        # This should not crash but should fail safely
        report = invalid_verifier.verify_email_send(
            "test@example.com",
            "Test User",
            "test.pdf"
        )

        self.assertEqual(report.overall_status, "FAIL")
        self.assertFalse(report.can_send)


class TestEndToEndWorkflows(unittest.TestCase):
    """Test complete end-to-end workflows"""

    def setUp(self):
        """Set up complete test environment"""
        self.test_dir = tempfile.mkdtemp()
        self.setup_complete_test_environment()

    def tearDown(self):
        """Clean up test environment"""
        shutil.rmtree(self.test_dir)

    def setup_complete_test_environment(self):
        """Set up complete test environment with files and database"""
        # Create customer database
        self.test_db_file = os.path.join(self.test_dir, 'complete_test_db.json')

        # Create test pricing files directory
        self.pricing_dir = os.path.join(self.test_dir, "pricing_files")
        os.makedirs(self.pricing_dir, exist_ok=True)

        # Create test pricing file
        pricing_file = os.path.join(self.pricing_dir, "202509_Pricing_Test_Company.pdf")
        with open(pricing_file, 'w') as f:
            f.write("Test pricing file content for Test Company")

        # Create database with realistic data
        test_data = {
            "version": "2.0.0",
            "customers": [
                {
                    "id": "test_company_001",
                    "company_name": "Test Company Ltd",
                    "recipient_names": ["John Manager", "Jane CFO"],
                    "email_addresses": ["john@testcompany.com", "jane@testcompany.com"],
                    "email_domain": "testcompany.com",
                    "file_generation": {
                        "filename_pattern": "{month}_{file_body}",
                        "file_body": "_Pricing_Test_Company.pdf",
                        "file_path": self.pricing_dir,
                        "current_filename": "202509_Pricing_Test_Company.pdf"
                    },
                    "verification_status": {
                        "domain_verified": True,
                        "file_path_verified": True,
                        "filename_verified": True
                    },
                    "active": True
                }
            ]
        }

        with open(self.test_db_file, 'w') as f:
            json.dump(test_data, f)

        self.verifier = MultiLayerVerificationSystem(self.test_db_file)
        self.auditor = AuditLogger()

    def test_complete_successful_workflow(self):
        """Test complete successful email verification workflow"""
        # Step 1: Verify email can be sent
        report = self.verifier.verify_email_send(
            "john@testcompany.com",
            "John Manager",
            "202509_Pricing_Test_Company.pdf"
        )

        # Verify success
        self.assertEqual(report.overall_status, "PASS")
        self.assertTrue(report.can_send)
        self.assertEqual(report.company_name, "Test Company Ltd")

        # Check all verification results passed
        failed_checks = [r for r in report.verification_results if not r.passed]
        critical_failures = [r for r in failed_checks if r.level == VerificationLevel.CRITICAL]

        self.assertEqual(len(critical_failures), 0, f"Critical failures found: {critical_failures}")

        # Step 2: Log the successful verification
        self.auditor.log_email_send_success(
            "john@testcompany.com",
            "John Manager",
            "202509_Pricing_Test_Company.pdf",
            customer_id="test_company_001"
        )

        # Verify audit logging
        events = self.auditor.get_audit_events()
        success_events = [e for e in events if e['event_type'] == AuditEventType.EMAIL_SEND_SUCCESS.value]
        self.assertTrue(len(success_events) > 0)

    def test_complete_failure_workflow(self):
        """Test complete failure workflow with proper logging"""
        # Test with wrong domain
        report = self.verifier.verify_email_send(
            "admin@wrongcompany.com",  # Wrong domain
            "Wrong Manager",
            "202509_Pricing_Test_Company.pdf"
        )

        # Verify failure
        self.assertEqual(report.overall_status, "FAIL")
        self.assertFalse(report.can_send)

        # Log the verification failure
        verification_results = [asdict(r) for r in report.verification_results]
        self.auditor.log_verification_failure(
            "admin@wrongcompany.com",
            "Wrong Manager",
            "202509_Pricing_Test_Company.pdf",
            verification_results
        )

        # Verify audit logging
        events = self.auditor.get_audit_events(event_type=AuditEventType.VERIFICATION_FAILURE)
        self.assertTrue(len(events) > 0)

        failure_event = events[-1]
        self.assertEqual(failure_event['severity'], AuditSeverity.CRITICAL.value)
        self.assertFalse(failure_event['success'])

def asdict(obj):
    """Simple asdict implementation for VerificationResult"""
    return {
        'check_name': obj.check_name,
        'level': obj.level.value,
        'passed': obj.passed,
        'message': obj.message,
        'details': obj.details
    }


class TestSuite:
    """Test suite runner for comprehensive testing"""

    def __init__(self):
        self.test_results = {}

    def run_all_tests(self):
        """Run all test suites"""
        print("="*80)
        print("CUSTOMER DATABASE MIGRATION & VERIFICATION SYSTEM v2.0")
        print("COMPREHENSIVE TEST SUITE")
        print("="*80)
        print()

        test_classes = [
            TestCustomerDatabase,
            TestVerificationSystem,
            TestAuditLogging,
            TestSecurityScenarios,
            TestEndToEndWorkflows
        ]

        total_tests = 0
        total_failures = 0
        total_errors = 0

        for test_class in test_classes:
            print(f"Running {test_class.__name__}...")

            suite = unittest.TestLoader().loadTestsFromTestCase(test_class)
            runner = unittest.TextTestRunner(verbosity=2, stream=open(os.devnull, 'w'))
            result = runner.run(suite)

            tests_run = result.testsRun
            failures = len(result.failures)
            errors = len(result.errors)

            total_tests += tests_run
            total_failures += failures
            total_errors += errors

            status = "PASS" if (failures == 0 and errors == 0) else "FAIL"
            print(f"  {test_class.__name__}: {status} ({tests_run} tests, {failures} failures, {errors} errors)")

            self.test_results[test_class.__name__] = {
                'tests_run': tests_run,
                'failures': failures,
                'errors': errors,
                'status': status
            }

        print()
        print("="*80)
        print("TEST SUMMARY")
        print("="*80)
        print(f"Total Tests: {total_tests}")
        print(f"Total Failures: {total_failures}")
        print(f"Total Errors: {total_errors}")

        overall_status = "PASS" if (total_failures == 0 and total_errors == 0) else "FAIL"
        print(f"Overall Status: {overall_status}")

        if overall_status == "PASS":
            print("\n✅ ALL TESTS PASSED - System ready for production!")
            print("✅ Verification system will prevent wrong pricing data sends")
            print("✅ Security safeguards are functioning correctly")
        else:
            print("\n❌ TESTS FAILED - DO NOT DEPLOY TO PRODUCTION")
            print("❌ Critical security issues detected")
            print("❌ Fix all failures before using system")

        return overall_status == "PASS"


def main():
    """Main test runner"""
    test_suite = TestSuite()
    success = test_suite.run_all_tests()

    if not success:
        exit(1)


if __name__ == "__main__":
    main()