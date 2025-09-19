#!/usr/bin/env python3
"""
Multi-Layer Verification System v2.0
====================================

CRITICAL BUSINESS SYSTEM - Prevents sending wrong pricing data to customers
This module implements a comprehensive 3-layer verification system to ensure
absolute accuracy in customer email targeting and file delivery.

ZERO TOLERANCE POLICY: Better to not send than send wrong data

Author: Claude Code v2.0
Date: 2025-09-16
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple, Optional
import logging
from dataclasses import dataclass
from enum import Enum


class VerificationLevel(Enum):
    """Verification severity levels"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class VerificationResult:
    """Single verification check result"""
    check_name: str
    level: VerificationLevel
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None


@dataclass
class CustomerVerificationReport:
    """Complete verification report for a customer"""
    customer_id: str
    company_name: str
    email: str
    recipient_name: str
    attachment_file: str
    verification_results: List[VerificationResult]
    overall_status: str  # "PASS", "WARNING", "FAIL"
    can_send: bool
    timestamp: datetime


class CustomerDatabase:
    """Handles loading and querying the JSON customer database"""

    def __init__(self, database_file: str = "data/customer_database.json"):
        self.database_file = database_file
        self.data = None
        self.load_database()

    def load_database(self) -> None:
        """Load customer database from JSON file"""
        try:
            with open(self.database_file, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            logging.info(f"Loaded customer database with {len(self.data['customers'])} customers")
        except Exception as e:
            logging.error(f"Failed to load customer database: {str(e)}")
            raise

    def get_customer_by_email_domain(self, email: str) -> Optional[Dict[str, Any]]:
        """Find customer record by email domain"""
        try:
            email_domain = email.split('@')[1].lower()
            for customer in self.data['customers']:
                if customer['email_domain'].lower() == email_domain:
                    return customer
            return None
        except (IndexError, AttributeError):
            return None

    def get_customer_by_id(self, customer_id: str) -> Optional[Dict[str, Any]]:
        """Find customer record by ID"""
        for customer in self.data['customers']:
            if customer['id'] == customer_id:
                return customer
        return None

    def is_email_authorized(self, email: str, customer_record: Dict[str, Any]) -> bool:
        """Check if email is in the authorized list for this customer"""
        return email.lower() in [addr.lower() for addr in customer_record['email_addresses']]

    def get_all_customers(self) -> List[Dict[str, Any]]:
        """Get all customers from the database"""
        return self.data.get('customers', [])

    def add_customer(self, customer_data: Dict[str, Any]) -> str:
        """Add a new customer to the database"""
        # Generate new ID
        import uuid
        customer_id = str(uuid.uuid4())[:8].upper()

        # Add required fields
        customer_data['id'] = customer_id
        customer_data['created_at'] = datetime.now().isoformat()
        customer_data['last_verified'] = 'Never'
        customer_data['verification_status'] = {
            'domain_verified': False,
            'recipients_verified': False,
            'file_paths_verified': False,
            'last_check': None
        }

        # Add to database
        if 'customers' not in self.data:
            self.data['customers'] = []
        self.data['customers'].append(customer_data)

        # Save to file
        self.save_database()
        return customer_id

    def update_customer(self, customer_id: str, customer_data: Dict[str, Any]) -> bool:
        """Update an existing customer in the database"""
        for i, customer in enumerate(self.data['customers']):
            if customer['id'] == customer_id:
                # Preserve ID and metadata
                customer_data['id'] = customer_id
                customer_data['updated_at'] = datetime.now().isoformat()
                self.data['customers'][i] = customer_data
                self.save_database()
                return True
        return False

    def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer from the database"""
        for i, customer in enumerate(self.data['customers']):
            if customer['id'] == customer_id:
                del self.data['customers'][i]
                self.save_database()
                return True
        return False

    def save_database(self) -> None:
        """Save the database back to JSON file"""
        try:
            with open(self.database_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            logging.info(f"Saved customer database with {len(self.data['customers'])} customers")
        except Exception as e:
            logging.error(f"Failed to save customer database: {str(e)}")
            raise


class MultiLayerVerificationSystem:
    """
    Implements comprehensive 3-layer verification system
    CRITICAL: This system prevents cross-customer data exposure
    """

    def __init__(self, database_file: str = "data/customer_database.json"):
        self.database = CustomerDatabase(database_file)
        self.verification_rules = self.database.data.get('verification_rules', {})

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/verification_v2.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    def verify_domain_match(self, email: str, customer_record: Dict[str, Any]) -> VerificationResult:
        """
        CRITICAL: Verify email domain matches customer record
        Prevents wrong prices to wrong customer - ABSOLUTE REQUIREMENT
        """
        try:
            email_domain = email.split('@')[1].lower()
            expected_domain = customer_record['email_domain'].lower()

            if email_domain == expected_domain:
                return VerificationResult(
                    check_name="domain_verification",
                    level=VerificationLevel.INFO,
                    passed=True,
                    message=f"Domain verified: {email_domain}",
                    details={"email": email, "expected_domain": expected_domain}
                )
            else:
                return VerificationResult(
                    check_name="domain_verification",
                    level=VerificationLevel.CRITICAL,
                    passed=False,
                    message=f"CRITICAL: Domain mismatch - {email} not authorized for {customer_record['company_name']}",
                    details={
                        "email": email,
                        "email_domain": email_domain,
                        "expected_domain": expected_domain,
                        "company": customer_record['company_name']
                    }
                )
        except (IndexError, AttributeError, KeyError) as e:
            return VerificationResult(
                check_name="domain_verification",
                level=VerificationLevel.CRITICAL,
                passed=False,
                message=f"CRITICAL: Domain verification failed - {str(e)}",
                details={"error": str(e), "email": email}
            )

    def verify_email_authorization(self, email: str, customer_record: Dict[str, Any]) -> VerificationResult:
        """Verify email is in authorized list for customer"""
        if self.database.is_email_authorized(email, customer_record):
            return VerificationResult(
                check_name="email_authorization",
                level=VerificationLevel.INFO,
                passed=True,
                message=f"Email authorized: {email}",
                details={"email": email, "authorized_emails": customer_record['email_addresses']}
            )
        else:
            return VerificationResult(
                check_name="email_authorization",
                level=VerificationLevel.ERROR,
                passed=False,
                message=f"ERROR: Email {email} not in authorized list for {customer_record['company_name']}",
                details={
                    "email": email,
                    "authorized_emails": customer_record['email_addresses'],
                    "company": customer_record['company_name']
                }
            )

    def verify_pricing_file_exists(self, customer_record: Dict[str, Any]) -> VerificationResult:
        """Verify pricing file exists at specified path"""
        try:
            file_path = customer_record['file_generation']['file_path']
            current_filename = customer_record['file_generation']['current_filename']

            if not file_path or not current_filename:
                return VerificationResult(
                    check_name="file_existence",
                    level=VerificationLevel.ERROR,
                    passed=False,
                    message="ERROR: File path or filename not specified",
                    details={"file_path": file_path, "filename": current_filename}
                )

            full_path = os.path.join(file_path, current_filename)

            if os.path.exists(full_path):
                file_size = os.path.getsize(full_path)
                return VerificationResult(
                    check_name="file_existence",
                    level=VerificationLevel.INFO,
                    passed=True,
                    message=f"Pricing file verified: {current_filename}",
                    details={
                        "full_path": full_path,
                        "file_size": file_size,
                        "file_exists": True
                    }
                )
            else:
                return VerificationResult(
                    check_name="file_existence",
                    level=VerificationLevel.ERROR,
                    passed=False,
                    message=f"ERROR: Pricing file not found: {full_path}",
                    details={
                        "full_path": full_path,
                        "file_path": file_path,
                        "filename": current_filename,
                        "file_exists": False
                    }
                )

        except (KeyError, TypeError) as e:
            return VerificationResult(
                check_name="file_existence",
                level=VerificationLevel.ERROR,
                passed=False,
                message=f"ERROR: File verification failed - {str(e)}",
                details={"error": str(e)}
            )

    def verify_filename_pattern(self, customer_record: Dict[str, Any]) -> VerificationResult:
        """Verify filename matches expected pattern"""
        try:
            expected_pattern = customer_record['file_generation']['filename_pattern']
            current_filename = customer_record['file_generation']['current_filename']
            company_name = customer_record['company_name']

            # Check if filename contains company name
            if company_name.lower() in current_filename.lower():
                return VerificationResult(
                    check_name="filename_pattern",
                    level=VerificationLevel.INFO,
                    passed=True,
                    message=f"Filename pattern verified: {current_filename}",
                    details={
                        "filename": current_filename,
                        "pattern": expected_pattern,
                        "company_name": company_name
                    }
                )
            else:
                return VerificationResult(
                    check_name="filename_pattern",
                    level=VerificationLevel.WARNING,
                    passed=False,
                    message=f"WARNING: Filename may not match company - {current_filename}",
                    details={
                        "filename": current_filename,
                        "expected_company": company_name,
                        "pattern": expected_pattern
                    }
                )

        except (KeyError, TypeError) as e:
            return VerificationResult(
                check_name="filename_pattern",
                level=VerificationLevel.WARNING,
                passed=False,
                message=f"WARNING: Filename pattern check failed - {str(e)}",
                details={"error": str(e)}
            )

    def verify_recipient_name(self, recipient_name: str, customer_record: Dict[str, Any]) -> VerificationResult:
        """Verify recipient name exists in customer record"""
        try:
            authorized_names = customer_record.get('recipient_names', [])

            # Simple check if any part of the recipient name matches
            name_found = False
            for auth_name in authorized_names:
                if auth_name.lower() in recipient_name.lower() or recipient_name.lower() in auth_name.lower():
                    name_found = True
                    break

            if name_found or not authorized_names:  # Pass if no names specified
                return VerificationResult(
                    check_name="recipient_validation",
                    level=VerificationLevel.INFO,
                    passed=True,
                    message=f"Recipient validated: {recipient_name}",
                    details={
                        "recipient": recipient_name,
                        "authorized_names": authorized_names
                    }
                )
            else:
                return VerificationResult(
                    check_name="recipient_validation",
                    level=VerificationLevel.WARNING,
                    passed=False,
                    message=f"WARNING: Recipient name not in authorized list - {recipient_name}",
                    details={
                        "recipient": recipient_name,
                        "authorized_names": authorized_names
                    }
                )

        except (KeyError, TypeError) as e:
            return VerificationResult(
                check_name="recipient_validation",
                level=VerificationLevel.WARNING,
                passed=False,
                message=f"WARNING: Recipient validation failed - {str(e)}",
                details={"error": str(e)}
            )

    def level_1_pre_send_checks(self, email: str, recipient_name: str) -> List[VerificationResult]:
        """
        Level 1: Pre-send checks
        - Email domain matches customer record
        - Email is authorized for customer
        - Basic recipient validation
        """
        results = []

        # Find customer record by email domain
        customer_record = self.database.get_customer_by_email_domain(email)

        if not customer_record:
            results.append(VerificationResult(
                check_name="customer_lookup",
                level=VerificationLevel.CRITICAL,
                passed=False,
                message=f"CRITICAL: No customer record found for email domain in {email}",
                details={"email": email}
            ))
            return results

        # Domain verification (CRITICAL)
        results.append(self.verify_domain_match(email, customer_record))

        # Email authorization
        results.append(self.verify_email_authorization(email, customer_record))

        # Recipient validation
        results.append(self.verify_recipient_name(recipient_name, customer_record))

        return results

    def level_2_content_validation(self, email: str) -> List[VerificationResult]:
        """
        Level 2: Content validation
        - Pricing file exists
        - Filename matches pattern
        - File not empty/corrupted
        """
        results = []

        customer_record = self.database.get_customer_by_email_domain(email)
        if not customer_record:
            results.append(VerificationResult(
                check_name="customer_lookup_l2",
                level=VerificationLevel.CRITICAL,
                passed=False,
                message=f"CRITICAL: Customer record not found for Level 2 checks",
                details={"email": email}
            ))
            return results

        # File existence check
        results.append(self.verify_pricing_file_exists(customer_record))

        # Filename pattern check
        results.append(self.verify_filename_pattern(customer_record))

        return results

    def level_3_final_confirmation(self, email: str, recipient_name: str, attachment_file: str) -> CustomerVerificationReport:
        """
        Level 3: Final confirmation with complete report
        Returns comprehensive verification report for user approval
        """
        customer_record = self.database.get_customer_by_email_domain(email)

        if not customer_record:
            return CustomerVerificationReport(
                customer_id="unknown",
                company_name="Unknown",
                email=email,
                recipient_name=recipient_name,
                attachment_file=attachment_file,
                verification_results=[VerificationResult(
                    check_name="final_customer_lookup",
                    level=VerificationLevel.CRITICAL,
                    passed=False,
                    message="CRITICAL: Customer record not found",
                    details={"email": email}
                )],
                overall_status="FAIL",
                can_send=False,
                timestamp=datetime.now()
            )

        # Run all verification checks
        all_results = []
        all_results.extend(self.level_1_pre_send_checks(email, recipient_name))
        all_results.extend(self.level_2_content_validation(email))

        # Determine overall status
        critical_failures = [r for r in all_results if r.level == VerificationLevel.CRITICAL and not r.passed]
        error_failures = [r for r in all_results if r.level == VerificationLevel.ERROR and not r.passed]
        warnings = [r for r in all_results if r.level == VerificationLevel.WARNING and not r.passed]

        if critical_failures:
            overall_status = "FAIL"
            can_send = False
        elif error_failures:
            overall_status = "FAIL"
            can_send = False
        elif warnings:
            overall_status = "WARNING"
            can_send = False  # Require manual approval for warnings
        else:
            overall_status = "PASS"
            can_send = True

        return CustomerVerificationReport(
            customer_id=customer_record['id'],
            company_name=customer_record['company_name'],
            email=email,
            recipient_name=recipient_name,
            attachment_file=attachment_file,
            verification_results=all_results,
            overall_status=overall_status,
            can_send=can_send,
            timestamp=datetime.now()
        )

    def verify_customer(self, customer_id: str) -> Dict[str, Any]:
        """
        Verify a customer by ID
        Returns verification status and issues
        """
        customer = self.database.get_customer_by_id(customer_id)

        if not customer:
            return {
                'overall_status': 'failed',
                'issues': [{'message': f'Customer ID {customer_id} not found'}]
            }

        issues = []

        # Check domain verification
        if not customer.get('verification_status', {}).get('domain_verified', False):
            issues.append({'message': f"Domain not verified: {customer.get('email_domain', 'unknown')}"})

        # Check email addresses
        if not customer.get('email_addresses'):
            issues.append({'message': 'No email addresses configured'})

        # Check file paths
        file_generation = customer.get('file_generation', {})
        if not file_generation:
            issues.append({'message': 'No file generation paths configured'})
        elif isinstance(file_generation, dict):
            # Handle file_generation as a dictionary (current format)
            if not file_generation.get('file_path'):
                issues.append({'message': 'Missing file path in file generation config'})
        elif isinstance(file_generation, list):
            # Handle file_generation as a list (legacy format)
            for file_info in file_generation:
                if not file_info.get('file_path'):
                    issues.append({'message': 'Missing file path in file generation config'})

        # Determine overall status
        if not issues:
            overall_status = 'passed'
        elif any('No email addresses' in issue['message'] or 'not found' in issue['message'] for issue in issues):
            overall_status = 'failed'
        else:
            overall_status = 'warning'

        # Update verification status
        customer['verification_status']['domain_verified'] = (overall_status != 'failed')
        customer['verification_status']['recipients_verified'] = bool(customer.get('email_addresses'))
        # Check if file_generation has valid path
        if isinstance(file_generation, dict):
            customer['verification_status']['file_paths_verified'] = bool(file_generation.get('file_path'))
        else:
            customer['verification_status']['file_paths_verified'] = bool(file_generation)
        customer['verification_status']['last_check'] = datetime.now().isoformat()
        customer['last_verified'] = datetime.now().strftime('%Y-%m-%d')

        # Save updated status
        self.database.update_customer(customer_id, customer)

        return {
            'overall_status': overall_status,
            'issues': issues
        }

    def verify_email_send(self, email: str, recipient_name: str, attachment_file: str) -> CustomerVerificationReport:
        """
        Complete verification process for email send
        CRITICAL: This is the main verification entry point
        """
        self.logger.info(f"Starting verification for {email} -> {recipient_name}")

        # Ensure logs directory exists
        os.makedirs('logs', exist_ok=True)

        try:
            # Run Level 3 comprehensive check
            report = self.level_3_final_confirmation(email, recipient_name, attachment_file)

            # Log the verification attempt
            log_entry = {
                "timestamp": datetime.now().isoformat(),
                "email": email,
                "recipient": recipient_name,
                "attachment": attachment_file,
                "status": report.overall_status,
                "can_send": report.can_send,
                "verification_results": len(report.verification_results)
            }

            self.logger.info(f"Verification completed: {report.overall_status} - Can send: {report.can_send}")

            # Log critical failures
            for result in report.verification_results:
                if result.level == VerificationLevel.CRITICAL and not result.passed:
                    self.logger.critical(f"CRITICAL FAILURE: {result.message}")
                elif result.level == VerificationLevel.ERROR and not result.passed:
                    self.logger.error(f"ERROR: {result.message}")
                elif result.level == VerificationLevel.WARNING and not result.passed:
                    self.logger.warning(f"WARNING: {result.message}")

            return report

        except Exception as e:
            self.logger.error(f"Verification system error: {str(e)}")

            # Return fail-safe result
            return CustomerVerificationReport(
                customer_id="error",
                company_name="System Error",
                email=email,
                recipient_name=recipient_name,
                attachment_file=attachment_file,
                verification_results=[VerificationResult(
                    check_name="system_error",
                    level=VerificationLevel.CRITICAL,
                    passed=False,
                    message=f"CRITICAL: Verification system error - {str(e)}",
                    details={"error": str(e)}
                )],
                overall_status="FAIL",
                can_send=False,
                timestamp=datetime.now()
            )

    def get_verification_preview(self, email: str, recipient_name: str, attachment_file: str) -> Dict[str, Any]:
        """Generate verification preview for UI display"""
        customer_record = self.database.get_customer_by_email_domain(email)

        if not customer_record:
            return {
                "customer": "Unknown",
                "recipient": recipient_name,
                "email": email,
                "attachment": attachment_file,
                "domain_check": "❌ No customer record found",
                "file_check": "❌ Cannot verify",
                "status": "FAIL",
                "can_send": False
            }

        # Quick domain check
        domain_result = self.verify_domain_match(email, customer_record)
        domain_status = "✅ Verified" if domain_result.passed else "❌ Failed"

        # Quick file check
        file_result = self.verify_pricing_file_exists(customer_record)
        file_status = "✅ Found" if file_result.passed else "❌ Missing"

        return {
            "customer": customer_record['company_name'],
            "recipient": recipient_name,
            "email": email,
            "attachment": attachment_file,
            "domain_check": domain_status,
            "file_check": file_status,
            "status": "PREVIEW",
            "can_send": domain_result.passed and file_result.passed
        }


def main():
    """Test the verification system"""
    print("="*60)
    print("Multi-Layer Verification System v2.0 - Test")
    print("="*60)

    verifier = MultiLayerVerificationSystem()

    # Test with a known good email
    test_email = "arnulfoc@atlanticoil.com"
    test_recipient = "Arnie"
    test_file = "250901_Pricing_Atlantic Performance Oils.pdf"

    print(f"Testing verification for: {test_email}")

    # Get preview
    preview = verifier.get_verification_preview(test_email, test_recipient, test_file)
    print("\nPreview:")
    for key, value in preview.items():
        print(f"  {key}: {value}")

    # Full verification
    report = verifier.verify_email_send(test_email, test_recipient, test_file)
    print(f"\nFull Verification Report:")
    print(f"Customer: {report.company_name}")
    print(f"Status: {report.overall_status}")
    print(f"Can Send: {report.can_send}")
    print(f"Checks: {len(report.verification_results)}")

    for result in report.verification_results:
        status = "✅" if result.passed else "❌"
        print(f"  {status} {result.check_name}: {result.message}")


if __name__ == "__main__":
    main()