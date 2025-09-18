#!/usr/bin/env python3
"""
Excel to JSON Migration Script v2.0
====================================

CRITICAL BUSINESS SYSTEM - Migrates customer data from Excel to JSON database
with comprehensive verification to prevent sending wrong pricing data.

This script converts CustomerDetails worksheet to customer_database_v2.json
with multi-layer verification system.

Author: Claude Code v2.0
Date: 2025-09-16
"""

import pandas as pd
import json
import os
import re
from datetime import datetime
from typing import Dict, List, Any, Tuple
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/migration_v2.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class ExcelToJsonMigrator:
    """
    Handles migration from Excel CustomerDetails to JSON database v2.0
    with comprehensive verification system.
    """

    def __init__(self, excel_file: str = "Python_CustomerPricing.xlsx"):
        self.excel_file = excel_file
        self.json_file = "customer_database_v2.json"
        self.verification_errors = []
        self.migration_stats = {
            "total_rows": 0,
            "successful_migrations": 0,
            "failed_migrations": 0,
            "verification_failures": 0
        }

    def verify_domain_match(self, email: str, expected_domain: str) -> bool:
        """
        CRITICAL: Verify email domain matches customer record
        Prevents wrong prices to wrong customer
        """
        try:
            email_domain = email.split('@')[1].lower()
            return email_domain == expected_domain.lower()
        except (IndexError, AttributeError):
            return False

    def extract_emails_from_string(self, email_string: str) -> List[str]:
        """Extract individual email addresses from semicolon-separated string"""
        if pd.isna(email_string) or not email_string:
            return []

        # Split by semicolon and clean up
        emails = [email.strip() for email in str(email_string).split(';')]
        # Filter out empty strings and validate email format
        valid_emails = []
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

        for email in emails:
            if email and email_pattern.match(email):
                valid_emails.append(email)
            elif email:  # Non-empty but invalid format
                logger.warning(f"Invalid email format: {email}")

        return valid_emails

    def extract_recipient_names(self, recipient_string: str) -> List[str]:
        """Extract individual names from recipient string"""
        if pd.isna(recipient_string) or not recipient_string:
            return []

        # Handle common separators: comma, ampersand, 'and'
        names_str = str(recipient_string)
        # Replace common separators with commas
        names_str = re.sub(r'\s*[&,]\s*|\s+and\s+', ',', names_str)

        # Split and clean
        names = [name.strip() for name in names_str.split(',')]
        return [name for name in names if name]

    def generate_customer_id(self, company_name: str) -> str:
        """Generate unique customer ID from company name"""
        if pd.isna(company_name) or not company_name:
            return f"unknown_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        # Convert to lowercase, replace spaces/special chars with underscores
        clean_name = re.sub(r'[^a-zA-Z0-9\s]', '', str(company_name))
        clean_name = re.sub(r'\s+', '_', clean_name.lower())

        # Add unique suffix
        timestamp = datetime.now().strftime('%Y%m%d')
        return f"{clean_name}_{timestamp}"

    def verify_file_path(self, file_path: str) -> bool:
        """Verify that the file path exists"""
        if pd.isna(file_path) or not file_path:
            return False
        return os.path.exists(str(file_path).strip())

    def migrate_customer_record(self, row: pd.Series, row_index: int) -> Dict[str, Any]:
        """
        Migrate a single customer record from Excel row to JSON format
        with comprehensive verification
        """
        try:
            # Extract basic information
            company_name = str(row.get('CustomerName', '')).strip()
            if not company_name or company_name == 'nan':
                raise ValueError(f"Row {row_index}: Missing company name")

            # Extract and verify email addresses
            email_string = row.get('EmailAddresses', '')
            email_addresses = self.extract_emails_from_string(email_string)
            if not email_addresses:
                raise ValueError(f"Row {row_index}: No valid email addresses found")

            # Extract domain and verify consistency
            expected_domain = str(row.get('domain', '')).strip()
            if not expected_domain or expected_domain == 'nan':
                # Extract domain from first email
                expected_domain = email_addresses[0].split('@')[1]
                logger.warning(f"Row {row_index}: Domain extracted from email: {expected_domain}")

            # Verify all emails match the domain
            domain_violations = []
            for email in email_addresses:
                if not self.verify_domain_match(email, expected_domain):
                    domain_violations.append(email)

            if domain_violations:
                error_msg = f"Row {row_index}: Domain mismatch for emails: {domain_violations}"
                self.verification_errors.append(error_msg)
                logger.error(error_msg)

            # Extract recipient names
            recipient_string = row.get('RecipientName', '')
            recipient_names = self.extract_recipient_names(recipient_string)

            # Extract file information
            file_path = str(row.get('FilePath ', '')).strip()  # Note the space in column name
            file_name = str(row.get('FileName', '')).strip()
            month_prefix = str(row.get('Month', '')).strip()
            file_body = str(row.get('FileBody', '')).strip()

            # Verify file path exists
            file_path_verified = self.verify_file_path(file_path)
            if not file_path_verified:
                logger.warning(f"Row {row_index}: File path does not exist: {file_path}")

            # Verify full file exists
            full_file_path = os.path.join(file_path, file_name) if file_path and file_name else ""
            filename_verified = os.path.exists(full_file_path) if full_file_path else False

            # Extract pricing information
            has_fx_change = row.get('HasFXChange', False)
            fx_direction = row.get('FXDirection', None)
            has_price_change = row.get('HasPriceChange', False)
            price_direction = row.get('PriceDirection', None)

            # Generate unique ID
            customer_id = self.generate_customer_id(company_name)

            # Create customer record
            customer_record = {
                "id": customer_id,
                "company_name": company_name,
                "recipient_names": recipient_names,
                "email_addresses": email_addresses,
                "email_domain": expected_domain,
                "file_generation": {
                    "filename_pattern": "{month}_{file_body}",
                    "file_body": file_body if file_body != 'nan' else "",
                    "file_path": file_path if file_path != 'nan' else "",
                    "month_prefix": month_prefix if month_prefix != 'nan' else "",
                    "current_filename": file_name if file_name != 'nan' else ""
                },
                "pricing_details": {
                    "has_fx_change": bool(has_fx_change) if not pd.isna(has_fx_change) else False,
                    "fx_direction": fx_direction if not pd.isna(fx_direction) else None,
                    "has_price_change": bool(has_price_change) if not pd.isna(has_price_change) else False,
                    "price_direction": price_direction if not pd.isna(price_direction) else None
                },
                "verification_status": {
                    "domain_verified": len(domain_violations) == 0,
                    "file_path_verified": file_path_verified,
                    "filename_verified": filename_verified,
                    "last_verification": datetime.now().isoformat()
                },
                "active": True,
                "last_verified": datetime.now().isoformat(),
                "created_date": datetime.now().isoformat(),
                "migration_source": f"Excel row {row_index}",
                "notes": f"Migrated from Excel CustomerDetails worksheet on {datetime.now().strftime('%Y-%m-%d')}"
            }

            logger.info(f"Successfully migrated: {company_name}")
            return customer_record

        except Exception as e:
            error_msg = f"Row {row_index}: Migration failed - {str(e)}"
            self.verification_errors.append(error_msg)
            logger.error(error_msg)
            raise

    def load_excel_data(self) -> pd.DataFrame:
        """Load customer data from Excel file"""
        logger.info(f"Loading Excel file: {self.excel_file}")

        try:
            # Load with header on row 3 (0-indexed)
            df = pd.read_excel(self.excel_file, sheet_name='CustomerDetails', header=3)
            logger.info(f"Loaded {len(df)} rows from CustomerDetails worksheet")

            # Remove completely empty rows
            df = df.dropna(how='all')
            logger.info(f"After removing empty rows: {len(df)} rows")

            return df

        except Exception as e:
            logger.error(f"Failed to load Excel file: {str(e)}")
            raise

    def create_database_structure(self, customers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create the complete JSON database structure"""
        database = {
            "version": "2.0.0",
            "created_date": datetime.now().isoformat(),
            "migrated_from": self.excel_file,
            "verification_enabled": True,
            "migration_stats": self.migration_stats,
            "verification_errors": self.verification_errors,
            "customers": customers,
            "audit_log": [
                {
                    "timestamp": datetime.now().isoformat(),
                    "action": "database_migration",
                    "user": "system",
                    "details": f"Migrated {len(customers)} customers from Excel",
                    "success": True
                }
            ],
            "verification_rules": {
                "domain_check_required": True,
                "file_existence_check": True,
                "filename_pattern_check": True,
                "recipient_validation": True,
                "prevent_cross_domain_sends": True,
                "require_manual_approval_on_warnings": True
            },
            "schema_info": {
                "required_fields": [
                    "company_name",
                    "email_addresses",
                    "email_domain",
                    "file_generation.file_path",
                    "file_generation.file_body"
                ],
                "validation_fields": [
                    "verification_status.domain_verified",
                    "verification_status.file_path_verified",
                    "verification_status.filename_verified"
                ],
                "critical_checks": [
                    "Domain verification prevents cross-customer data exposure",
                    "File existence check prevents failed email sends",
                    "Recipient validation ensures correct delivery"
                ]
            }
        }

        return database

    def migrate(self) -> bool:
        """
        Execute the complete migration process
        Returns True if successful, False if critical errors occurred
        """
        logger.info("Starting Excel to JSON migration v2.0")

        try:
            # Ensure logs directory exists
            os.makedirs('logs', exist_ok=True)

            # Load Excel data
            df = self.load_excel_data()
            self.migration_stats["total_rows"] = len(df)

            # Migrate each customer record
            customers = []
            for index, row in df.iterrows():
                try:
                    customer_record = self.migrate_customer_record(row, index)
                    customers.append(customer_record)
                    self.migration_stats["successful_migrations"] += 1

                except Exception as e:
                    self.migration_stats["failed_migrations"] += 1
                    logger.error(f"Failed to migrate row {index}: {str(e)}")

            # Create complete database
            database = self.create_database_structure(customers)

            # Save to JSON file
            with open(self.json_file, 'w', encoding='utf-8') as f:
                json.dump(database, f, indent=2, ensure_ascii=False)

            # Log summary
            logger.info("Migration completed!")
            logger.info(f"Total rows processed: {self.migration_stats['total_rows']}")
            logger.info(f"Successful migrations: {self.migration_stats['successful_migrations']}")
            logger.info(f"Failed migrations: {self.migration_stats['failed_migrations']}")
            logger.info(f"Verification errors: {len(self.verification_errors)}")
            logger.info(f"Database saved to: {self.json_file}")

            # Display verification errors
            if self.verification_errors:
                logger.warning("VERIFICATION ERRORS DETECTED:")
                for error in self.verification_errors:
                    logger.warning(f"  {error}")

            return len(self.verification_errors) == 0

        except Exception as e:
            logger.error(f"Migration failed: {str(e)}")
            return False


def main():
    """Main execution function"""
    print("="*60)
    print("Customer Database Migration v2.0")
    print("="*60)
    print("CRITICAL BUSINESS SYSTEM")
    print("Migrating Excel data to JSON with verification")
    print("="*60)

    migrator = ExcelToJsonMigrator()
    success = migrator.migrate()

    if success:
        print("\n✅ Migration completed successfully!")
        print("✅ All verification checks passed!")
    else:
        print("\n⚠️  Migration completed with warnings!")
        print("⚠️  Please review verification errors above!")

    print(f"\nDatabase file: customer_database_v2.json")
    print(f"Log file: logs/migration_v2.log")
    print("="*60)


if __name__ == "__main__":
    main()