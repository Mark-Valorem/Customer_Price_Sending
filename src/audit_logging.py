#!/usr/bin/env python3
"""
Audit Logging System v2.0
=========================

CRITICAL BUSINESS SYSTEM - Comprehensive audit logging for customer email operations
This module provides detailed audit trails for all customer interactions, verification
attempts, and system activities to ensure complete traceability.

Features:
- Detailed email send attempt logging
- Customer database modification tracking
- Verification failure tracking
- Security event logging
- Compliance reporting

Author: Claude Code v2.0
Date: 2025-09-16
"""

import json
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import hashlib
import getpass


class AuditEventType(Enum):
    """Types of audit events"""
    EMAIL_SEND_ATTEMPT = "email_send_attempt"
    EMAIL_SEND_SUCCESS = "email_send_success"
    EMAIL_SEND_FAILURE = "email_send_failure"
    VERIFICATION_FAILURE = "verification_failure"
    CUSTOMER_CREATED = "customer_created"
    CUSTOMER_UPDATED = "customer_updated"
    CUSTOMER_DELETED = "customer_deleted"
    DATABASE_MIGRATION = "database_migration"
    SYSTEM_ERROR = "system_error"
    SECURITY_VIOLATION = "security_violation"
    LOGIN_ATTEMPT = "login_attempt"
    CONFIG_CHANGE = "config_change"


class AuditSeverity(Enum):
    """Severity levels for audit events"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """Individual audit event record"""
    timestamp: str
    event_type: AuditEventType
    severity: AuditSeverity
    user: str
    action: str
    details: Dict[str, Any]
    customer_id: Optional[str] = None
    email_address: Optional[str] = None
    recipient_name: Optional[str] = None
    attachment_file: Optional[str] = None
    verification_status: Optional[str] = None
    ip_address: Optional[str] = None
    session_id: Optional[str] = None
    success: bool = True
    error_message: Optional[str] = None
    event_id: Optional[str] = None

    def __post_init__(self):
        """Generate unique event ID"""
        if not self.event_id:
            event_data = f"{self.timestamp}{self.user}{self.action}"
            self.event_id = hashlib.md5(event_data.encode()).hexdigest()[:12]


class AuditLogger:
    """
    Comprehensive audit logging system for customer email operations
    CRITICAL: Maintains complete audit trail for compliance and security
    """

    def __init__(self, audit_file: str = "logs/audit_log_v2.json",
                 customer_database_file: str = "customer_database_v2.json"):
        self.audit_file = audit_file
        self.customer_database_file = customer_database_file
        self.current_user = getpass.getuser()
        self.session_id = self._generate_session_id()

        # Ensure directories exist
        os.makedirs(os.path.dirname(audit_file), exist_ok=True)

        # Configure file logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/audit_system.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        # Load or create audit log
        self.audit_log = self._load_audit_log()

    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        session_data = f"{datetime.now().isoformat()}{self.current_user}"
        return hashlib.md5(session_data.encode()).hexdigest()[:16]

    def _load_audit_log(self) -> List[Dict[str, Any]]:
        """Load existing audit log or create new one"""
        try:
            if os.path.exists(self.audit_file):
                with open(self.audit_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('audit_events', [])
            return []
        except Exception as e:
            self.logger.error(f"Failed to load audit log: {str(e)}")
            return []

    def _save_audit_log(self) -> None:
        """Save audit log to file"""
        try:
            audit_data = {
                "version": "2.0.0",
                "created_date": datetime.now().isoformat(),
                "total_events": len(self.audit_log),
                "audit_events": self.audit_log
            }

            with open(self.audit_file, 'w', encoding='utf-8') as f:
                json.dump(audit_data, f, indent=2, ensure_ascii=False)

            # Also update customer database audit log
            self._update_customer_database_audit()

        except Exception as e:
            self.logger.error(f"Failed to save audit log: {str(e)}")

    def _update_customer_database_audit(self) -> None:
        """Update audit log in customer database"""
        try:
            if os.path.exists(self.customer_database_file):
                with open(self.customer_database_file, 'r', encoding='utf-8') as f:
                    customer_data = json.load(f)

                # Update audit log in customer database
                customer_data['audit_log'] = self.audit_log[-100:]  # Keep last 100 events

                with open(self.customer_database_file, 'w', encoding='utf-8') as f:
                    json.dump(customer_data, f, indent=2, ensure_ascii=False)

        except Exception as e:
            self.logger.warning(f"Failed to update customer database audit log: {str(e)}")

    def log_event(self, event: AuditEvent) -> None:
        """Log an audit event"""
        try:
            # Convert event to dictionary
            event_dict = asdict(event)

            # Convert enums to strings
            event_dict['event_type'] = event.event_type.value
            event_dict['severity'] = event.severity.value

            # Add session information
            event_dict['session_id'] = self.session_id

            # Add to audit log
            self.audit_log.append(event_dict)

            # Log to file logger as well
            log_level = {
                AuditSeverity.INFO: logging.INFO,
                AuditSeverity.WARNING: logging.WARNING,
                AuditSeverity.ERROR: logging.ERROR,
                AuditSeverity.CRITICAL: logging.CRITICAL
            }[event.severity]

            self.logger.log(log_level, f"AUDIT: {event.action} - {event.details}")

            # Save immediately for critical events
            if event.severity in [AuditSeverity.ERROR, AuditSeverity.CRITICAL]:
                self._save_audit_log()

        except Exception as e:
            self.logger.error(f"Failed to log audit event: {str(e)}")

    def log_email_send_attempt(self, email: str, recipient: str, attachment: str,
                              customer_id: str = None, verification_status: str = "unknown") -> None:
        """Log email send attempt"""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=AuditEventType.EMAIL_SEND_ATTEMPT,
            severity=AuditSeverity.INFO,
            user=self.current_user,
            action="email_send_attempt",
            details={
                "email": email,
                "recipient": recipient,
                "attachment": attachment,
                "verification_status": verification_status
            },
            customer_id=customer_id,
            email_address=email,
            recipient_name=recipient,
            attachment_file=attachment,
            verification_status=verification_status
        )
        self.log_event(event)

    def log_email_send_success(self, email: str, recipient: str, attachment: str,
                              customer_id: str = None) -> None:
        """Log successful email send"""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=AuditEventType.EMAIL_SEND_SUCCESS,
            severity=AuditSeverity.INFO,
            user=self.current_user,
            action="email_sent_successfully",
            details={
                "email": email,
                "recipient": recipient,
                "attachment": attachment,
                "message": "Email draft created successfully"
            },
            customer_id=customer_id,
            email_address=email,
            recipient_name=recipient,
            attachment_file=attachment,
            success=True
        )
        self.log_event(event)

    def log_email_send_failure(self, email: str, recipient: str, attachment: str,
                              error_message: str, customer_id: str = None) -> None:
        """Log failed email send"""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=AuditEventType.EMAIL_SEND_FAILURE,
            severity=AuditSeverity.ERROR,
            user=self.current_user,
            action="email_send_failed",
            details={
                "email": email,
                "recipient": recipient,
                "attachment": attachment,
                "error": error_message
            },
            customer_id=customer_id,
            email_address=email,
            recipient_name=recipient,
            attachment_file=attachment,
            success=False,
            error_message=error_message
        )
        self.log_event(event)

    def log_verification_failure(self, email: str, recipient: str, attachment: str,
                                verification_results: List[Dict[str, Any]],
                                customer_id: str = None) -> None:
        """Log verification failure - CRITICAL for security"""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=AuditEventType.VERIFICATION_FAILURE,
            severity=AuditSeverity.CRITICAL,
            user=self.current_user,
            action="verification_failed",
            details={
                "email": email,
                "recipient": recipient,
                "attachment": attachment,
                "verification_results": verification_results,
                "message": "CRITICAL: Verification failed - email send blocked"
            },
            customer_id=customer_id,
            email_address=email,
            recipient_name=recipient,
            attachment_file=attachment,
            verification_status="FAILED",
            success=False,
            error_message="Verification checks failed"
        )
        self.log_event(event)

    def log_security_violation(self, email: str, violation_type: str, details: Dict[str, Any]) -> None:
        """Log security violation - CRITICAL"""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=AuditEventType.SECURITY_VIOLATION,
            severity=AuditSeverity.CRITICAL,
            user=self.current_user,
            action=f"security_violation_{violation_type}",
            details={
                "violation_type": violation_type,
                "email": email,
                "details": details,
                "message": f"SECURITY VIOLATION: {violation_type}"
            },
            email_address=email,
            success=False,
            error_message=f"Security violation: {violation_type}"
        )
        self.log_event(event)

    def log_customer_operation(self, operation: str, customer_id: str,
                              customer_name: str, details: Dict[str, Any]) -> None:
        """Log customer database operations"""
        event_types = {
            "create": AuditEventType.CUSTOMER_CREATED,
            "update": AuditEventType.CUSTOMER_UPDATED,
            "delete": AuditEventType.CUSTOMER_DELETED
        }

        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=event_types.get(operation, AuditEventType.CUSTOMER_UPDATED),
            severity=AuditSeverity.INFO,
            user=self.current_user,
            action=f"customer_{operation}",
            details={
                "customer_name": customer_name,
                "operation_details": details
            },
            customer_id=customer_id
        )
        self.log_event(event)

    def log_system_error(self, error_type: str, error_message: str, details: Dict[str, Any] = None) -> None:
        """Log system errors"""
        event = AuditEvent(
            timestamp=datetime.now().isoformat(),
            event_type=AuditEventType.SYSTEM_ERROR,
            severity=AuditSeverity.ERROR,
            user=self.current_user,
            action=f"system_error_{error_type}",
            details=details or {},
            success=False,
            error_message=error_message
        )
        self.log_event(event)

    def get_audit_events(self, start_date: datetime = None, end_date: datetime = None,
                        event_type: AuditEventType = None, customer_id: str = None,
                        email: str = None, severity: AuditSeverity = None) -> List[Dict[str, Any]]:
        """Retrieve audit events with filtering"""
        filtered_events = []

        for event in self.audit_log:
            # Date filtering
            if start_date or end_date:
                event_time = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                if start_date and event_time < start_date:
                    continue
                if end_date and event_time > end_date:
                    continue

            # Event type filtering
            if event_type and event['event_type'] != event_type.value:
                continue

            # Customer ID filtering
            if customer_id and event.get('customer_id') != customer_id:
                continue

            # Email filtering
            if email and event.get('email_address') != email:
                continue

            # Severity filtering
            if severity and event.get('severity') != severity.value:
                continue

            filtered_events.append(event)

        return filtered_events

    def get_security_events(self, hours: int = 24) -> List[Dict[str, Any]]:
        """Get security-related events from the last N hours"""
        start_time = datetime.now() - timedelta(hours=hours)

        security_events = []
        for event in self.audit_log:
            if event.get('severity') in ['error', 'critical']:
                event_time = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                if event_time >= start_time:
                    security_events.append(event)

        return security_events

    def get_customer_activity(self, customer_id: str, days: int = 30) -> List[Dict[str, Any]]:
        """Get all activity for a specific customer"""
        start_time = datetime.now() - timedelta(days=days)

        customer_events = []
        for event in self.audit_log:
            if event.get('customer_id') == customer_id:
                event_time = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                if event_time >= start_time:
                    customer_events.append(event)

        return customer_events

    def generate_compliance_report(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Generate compliance report for a date range"""
        events = self.get_audit_events(start_date, end_date)

        report = {
            "report_period": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat()
            },
            "summary": {
                "total_events": len(events),
                "email_attempts": 0,
                "successful_sends": 0,
                "failed_sends": 0,
                "verification_failures": 0,
                "security_violations": 0,
                "customer_operations": 0
            },
            "event_breakdown": {},
            "security_summary": [],
            "failed_verifications": [],
            "customer_activity": {}
        }

        # Analyze events
        for event in events:
            event_type = event['event_type']

            # Count by type
            if event_type not in report["event_breakdown"]:
                report["event_breakdown"][event_type] = 0
            report["event_breakdown"][event_type] += 1

            # Summary counts
            if event_type == AuditEventType.EMAIL_SEND_ATTEMPT.value:
                report["summary"]["email_attempts"] += 1
            elif event_type == AuditEventType.EMAIL_SEND_SUCCESS.value:
                report["summary"]["successful_sends"] += 1
            elif event_type == AuditEventType.EMAIL_SEND_FAILURE.value:
                report["summary"]["failed_sends"] += 1
            elif event_type == AuditEventType.VERIFICATION_FAILURE.value:
                report["summary"]["verification_failures"] += 1
                report["failed_verifications"].append(event)
            elif event_type == AuditEventType.SECURITY_VIOLATION.value:
                report["summary"]["security_violations"] += 1
                report["security_summary"].append(event)
            elif event_type in [AuditEventType.CUSTOMER_CREATED.value,
                              AuditEventType.CUSTOMER_UPDATED.value,
                              AuditEventType.CUSTOMER_DELETED.value]:
                report["summary"]["customer_operations"] += 1

            # Customer activity
            customer_id = event.get('customer_id')
            if customer_id:
                if customer_id not in report["customer_activity"]:
                    report["customer_activity"][customer_id] = []
                report["customer_activity"][customer_id].append({
                    "timestamp": event['timestamp'],
                    "action": event['action'],
                    "success": event.get('success', True)
                })

        return report

    def save_audit_log(self) -> None:
        """Manually save audit log"""
        self._save_audit_log()

    def cleanup_old_logs(self, days: int = 365) -> None:
        """Clean up audit logs older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)

        original_count = len(self.audit_log)

        # Filter out old events
        self.audit_log = [
            event for event in self.audit_log
            if datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00')) >= cutoff_date
        ]

        removed_count = original_count - len(self.audit_log)

        if removed_count > 0:
            self.logger.info(f"Cleaned up {removed_count} old audit events (older than {days} days)")
            self._save_audit_log()


def main():
    """Test the audit logging system"""
    print("="*60)
    print("Audit Logging System v2.0 - Test")
    print("="*60)

    # Create audit logger
    auditor = AuditLogger()

    # Test various log entries
    auditor.log_email_send_attempt(
        email="test@example.com",
        recipient="Test User",
        attachment="test_pricing.pdf",
        customer_id="test_customer_001",
        verification_status="PASS"
    )

    auditor.log_verification_failure(
        email="wrong@domain.com",
        recipient="Wrong User",
        attachment="wrong_file.pdf",
        verification_results=[
            {"check": "domain_verification", "passed": False, "message": "Domain mismatch"}
        ],
        customer_id="unknown"
    )

    auditor.log_customer_operation(
        operation="create",
        customer_id="new_customer_001",
        customer_name="New Test Customer",
        details={"created_by": "dashboard", "email_count": 2}
    )

    # Save logs
    auditor.save_audit_log()

    # Generate sample report
    end_date = datetime.now()
    start_date = end_date - timedelta(days=7)
    report = auditor.generate_compliance_report(start_date, end_date)

    print(f"Generated compliance report for last 7 days:")
    print(f"Total events: {report['summary']['total_events']}")
    print(f"Email attempts: {report['summary']['email_attempts']}")
    print(f"Verification failures: {report['summary']['verification_failures']}")
    print(f"Security violations: {report['summary']['security_violations']}")

    print("\nAudit logging system test completed!")


if __name__ == "__main__":
    main()