"""
Auditing and compliance system for the Happy Path platform.
Provides comprehensive audit logging, security monitoring, and compliance tracking.
"""

import json
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid

from .config import get_config
from .database import get_db_manager, execute_query, execute_transaction
from .logging import get_logger
from .exceptions import AuditError

logger = get_logger(__name__)


class AuditEventType(Enum):
    """Types of audit events."""
    # User Management
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_REGISTRATION = "user_registration"
    USER_PASSWORD_CHANGE = "user_password_change"
    USER_PROFILE_UPDATE = "user_profile_update"
    USER_DELETION = "user_deletion"
    
    # Data Access
    DATA_READ = "data_read"
    DATA_WRITE = "data_write"
    DATA_UPDATE = "data_update"
    DATA_DELETE = "data_delete"
    DATA_EXPORT = "data_export"
    DATA_IMPORT = "data_import"
    
    # Security Events
    SECURITY_LOGIN_FAILED = "security_login_failed"
    SECURITY_ACCOUNT_LOCKED = "security_account_locked"
    SECURITY_PASSWORD_RESET = "security_password_reset"
    SECURITY_2FA_ENABLED = "security_2fa_enabled"
    SECURITY_2FA_DISABLED = "security_2fa_disabled"
    SECURITY_SUSPICIOUS_ACTIVITY = "security_suspicious_activity"
    
    # Privacy Events
    PRIVACY_CONSENT_GIVEN = "privacy_consent_given"
    PRIVACY_CONSENT_WITHDRAWN = "privacy_consent_withdrawn"
    PRIVACY_DATA_REQUEST = "privacy_data_request"
    PRIVACY_DATA_DELETION = "privacy_data_deletion"
    PRIVACY_DATA_PORTABILITY = "privacy_data_portability"
    
    # Financial Events
    PAYMENT_PROCESSED = "payment_processed"
    PAYMENT_FAILED = "payment_failed"
    SUBSCRIPTION_CREATED = "subscription_created"
    SUBSCRIPTION_CANCELLED = "subscription_cancelled"
    REFUND_ISSUED = "refund_issued"
    
    # Clinical Events
    MOOD_ENTRY_CREATED = "mood_entry_created"
    JOURNAL_ENTRY_CREATED = "journal_entry_created"
    ASSESSMENT_COMPLETED = "assessment_completed"
    CRISIS_DETECTED = "crisis_detected"
    PROVIDER_MESSAGE_SENT = "provider_message_sent"
    
    # Administrative Events
    ADMIN_LOGIN = "admin_login"
    ADMIN_USER_IMPERSONATION = "admin_user_impersonation"
    ADMIN_SYSTEM_CONFIG_CHANGE = "admin_system_config_change"
    ADMIN_BACKUP_CREATED = "admin_backup_created"
    ADMIN_MAINTENANCE_MODE = "admin_maintenance_mode"


class AuditSeverity(Enum):
    """Audit event severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AuditEvent:
    """Audit event data structure."""
    event_id: str
    event_type: AuditEventType
    user_id: Optional[str]
    session_id: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    timestamp: datetime
    severity: AuditSeverity
    description: str
    details: Dict[str, Any]
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    before_data: Optional[Dict[str, Any]] = None
    after_data: Optional[Dict[str, Any]] = None
    success: bool = True
    error_message: Optional[str] = None


class AuditLogger:
    """Comprehensive audit logging system."""
    
    def __init__(self):
        self.config = get_config()
        self.db_manager = get_db_manager()
        self._event_handlers: Dict[AuditEventType, List[callable]] = {}
    
    def log_event(
        self,
        event_type: AuditEventType,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        severity: AuditSeverity = AuditSeverity.MEDIUM,
        description: str = "",
        details: Optional[Dict[str, Any]] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        before_data: Optional[Dict[str, Any]] = None,
        after_data: Optional[Dict[str, Any]] = None,
        success: bool = True,
        error_message: Optional[str] = None
    ) -> str:
        """Log an audit event."""
        
        event_id = str(uuid.uuid4())
        
        event = AuditEvent(
            event_id=event_id,
            event_type=event_type,
            user_id=user_id,
            session_id=session_id,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.now(timezone.utc),
            severity=severity,
            description=description or self._get_default_description(event_type),
            details=details or {},
            resource_type=resource_type,
            resource_id=resource_id,
            before_data=before_data,
            after_data=after_data,
            success=success,
            error_message=error_message
        )
        
        try:
            # Store in database
            self._store_audit_event(event)
            
            # Log to application logger
            log_level = self._get_log_level(severity)
            logger.log(
                log_level,
                f"Audit Event: {event_type.value} - {description}",
                extra_data={
                    "audit_event_id": event_id,
                    "event_type": event_type.value,
                    "user_id": user_id,
                    "severity": severity.value,
                    "success": success
                }
            )
            
            # Call registered event handlers
            self._call_event_handlers(event)
            
            return event_id
            
        except Exception as e:
            logger.error(f"Failed to log audit event: {e}")
            raise AuditError(f"Audit logging failed: {e}")
    
    def _store_audit_event(self, event: AuditEvent):
        """Store audit event in database."""
        query = """
            INSERT INTO audit_logs (
                audit_id, event_type, user_id, session_id, ip_address, user_agent,
                timestamp, severity, description, details, resource_type, resource_id,
                before_data, after_data, success, error_message
            ) VALUES (
                %(audit_id)s, %(event_type)s, %(user_id)s, %(session_id)s, %(ip_address)s, %(user_agent)s,
                %(timestamp)s, %(severity)s, %(description)s, %(details)s, %(resource_type)s, %(resource_id)s,
                %(before_data)s, %(after_data)s, %(success)s, %(error_message)s
            )
        """
        
        params = {
            "audit_id": event.event_id,
            "event_type": event.event_type.value,
            "user_id": event.user_id,
            "session_id": event.session_id,
            "ip_address": event.ip_address,
            "user_agent": event.user_agent,
            "timestamp": event.timestamp,
            "severity": event.severity.value,
            "description": event.description,
            "details": json.dumps(event.details) if event.details else None,
            "resource_type": event.resource_type,
            "resource_id": event.resource_id,
            "before_data": json.dumps(event.before_data) if event.before_data else None,
            "after_data": json.dumps(event.after_data) if event.after_data else None,
            "success": event.success,
            "error_message": event.error_message
        }
        
        execute_query(query, params, fetch_all=False)
    
    def _get_default_description(self, event_type: AuditEventType) -> str:
        """Get default description for event type."""
        descriptions = {
            AuditEventType.USER_LOGIN: "User logged in",
            AuditEventType.USER_LOGOUT: "User logged out",
            AuditEventType.USER_REGISTRATION: "New user registered",
            AuditEventType.DATA_READ: "Data accessed",
            AuditEventType.DATA_WRITE: "Data created",
            AuditEventType.DATA_UPDATE: "Data updated",
            AuditEventType.DATA_DELETE: "Data deleted",
            AuditEventType.SECURITY_LOGIN_FAILED: "Login attempt failed",
            AuditEventType.PRIVACY_CONSENT_GIVEN: "Privacy consent granted",
            AuditEventType.PAYMENT_PROCESSED: "Payment processed",
            AuditEventType.CRISIS_DETECTED: "Crisis situation detected"
        }
        return descriptions.get(event_type, f"Event: {event_type.value}")
    
    def _get_log_level(self, severity: AuditSeverity) -> int:
        """Convert audit severity to logging level."""
        import logging
        levels = {
            AuditSeverity.LOW: logging.INFO,
            AuditSeverity.MEDIUM: logging.WARNING,
            AuditSeverity.HIGH: logging.ERROR,
            AuditSeverity.CRITICAL: logging.CRITICAL
        }
        return levels.get(severity, logging.INFO)
    
    def register_event_handler(self, event_type: AuditEventType, handler: callable):
        """Register a handler for specific audit events."""
        if event_type not in self._event_handlers:
            self._event_handlers[event_type] = []
        self._event_handlers[event_type].append(handler)
    
    def _call_event_handlers(self, event: AuditEvent):
        """Call registered event handlers."""
        handlers = self._event_handlers.get(event.event_type, [])
        for handler in handlers:
            try:
                handler(event)
            except Exception as e:
                logger.error(f"Event handler failed for {event.event_type.value}: {e}")
    
    def get_audit_trail(
        self,
        user_id: Optional[str] = None,
        resource_type: Optional[str] = None,
        resource_id: Optional[str] = None,
        event_types: Optional[List[AuditEventType]] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get audit trail with filtering options."""
        
        where_conditions = []
        params = {}
        
        if user_id:
            where_conditions.append("user_id = %(user_id)s")
            params["user_id"] = user_id
        
        if resource_type:
            where_conditions.append("resource_type = %(resource_type)s")
            params["resource_type"] = resource_type
        
        if resource_id:
            where_conditions.append("resource_id = %(resource_id)s")
            params["resource_id"] = resource_id
        
        if event_types:
            event_type_values = [et.value for et in event_types]
            where_conditions.append("event_type = ANY(%(event_types)s)")
            params["event_types"] = event_type_values
        
        if start_date:
            where_conditions.append("timestamp >= %(start_date)s")
            params["start_date"] = start_date
        
        if end_date:
            where_conditions.append("timestamp <= %(end_date)s")
            params["end_date"] = end_date
        
        where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
        
        query = f"""
            SELECT 
                audit_id, event_type, user_id, session_id, ip_address,
                timestamp, severity, description, details, resource_type,
                resource_id, success, error_message
            FROM audit_logs
            WHERE {where_clause}
            ORDER BY timestamp DESC
            LIMIT %(limit)s
        """
        
        params["limit"] = limit
        
        return execute_query(query, params)


class SecurityAuditor:
    """Security-focused audit monitoring and analysis."""
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
        self.failed_login_threshold = 5
        self.suspicious_activity_window = 3600  # 1 hour in seconds
    
    def track_login_attempt(self, user_id: str, ip_address: str, user_agent: str, success: bool):
        """Track login attempts for security monitoring."""
        event_type = AuditEventType.USER_LOGIN if success else AuditEventType.SECURITY_LOGIN_FAILED
        severity = AuditSeverity.LOW if success else AuditSeverity.MEDIUM
        
        self.audit_logger.log_event(
            event_type=event_type,
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            severity=severity,
            success=success
        )
        
        # Check for suspicious activity
        if not success:
            self._check_failed_login_pattern(user_id, ip_address)
    
    def _check_failed_login_pattern(self, user_id: str, ip_address: str):
        """Check for suspicious failed login patterns."""
        # Check failed logins in the last hour
        start_time = datetime.now(timezone.utc).timestamp() - self.suspicious_activity_window
        
        query = """
            SELECT COUNT(*) as failed_count
            FROM audit_logs
            WHERE event_type = %(event_type)s
              AND (user_id = %(user_id)s OR ip_address = %(ip_address)s)
              AND timestamp >= %(start_time)s
              AND success = false
        """
        
        result = execute_query(
            query,
            {
                "event_type": AuditEventType.SECURITY_LOGIN_FAILED.value,
                "user_id": user_id,
                "ip_address": ip_address,
                "start_time": datetime.fromtimestamp(start_time, tz=timezone.utc)
            },
            fetch_one=True
        )
        
        if result and result["failed_count"] >= self.failed_login_threshold:
            self.audit_logger.log_event(
                event_type=AuditEventType.SECURITY_SUSPICIOUS_ACTIVITY,
                user_id=user_id,
                ip_address=ip_address,
                severity=AuditSeverity.HIGH,
                description=f"Suspicious activity detected: {result['failed_count']} failed login attempts",
                details={
                    "failed_attempts": result["failed_count"],
                    "threshold": self.failed_login_threshold,
                    "window_hours": self.suspicious_activity_window / 3600
                }
            )
    
    def generate_security_report(self, days: int = 7) -> Dict[str, Any]:
        """Generate security audit report."""
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        # Get security events
        security_events = [
            AuditEventType.SECURITY_LOGIN_FAILED,
            AuditEventType.SECURITY_ACCOUNT_LOCKED,
            AuditEventType.SECURITY_SUSPICIOUS_ACTIVITY,
            AuditEventType.SECURITY_PASSWORD_RESET
        ]
        
        events = self.audit_logger.get_audit_trail(
            event_types=security_events,
            start_date=start_date,
            limit=1000
        )
        
        # Analyze events
        event_counts = {}
        ip_addresses = set()
        failed_logins_by_user = {}
        
        for event in events:
            event_type = event["event_type"]
            event_counts[event_type] = event_counts.get(event_type, 0) + 1
            
            if event["ip_address"]:
                ip_addresses.add(event["ip_address"])
            
            if event_type == AuditEventType.SECURITY_LOGIN_FAILED.value:
                user_id = event["user_id"]
                if user_id:
                    failed_logins_by_user[user_id] = failed_logins_by_user.get(user_id, 0) + 1
        
        return {
            "report_period_days": days,
            "generated_at": datetime.now(timezone.utc),
            "summary": {
                "total_security_events": len(events),
                "unique_ip_addresses": len(ip_addresses),
                "users_with_failed_logins": len(failed_logins_by_user)
            },
            "event_counts": event_counts,
            "top_failed_login_users": sorted(
                failed_logins_by_user.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]
        }


class ComplianceTracker:
    """Compliance monitoring and reporting for regulations like GDPR, HIPAA."""
    
    def __init__(self, audit_logger: AuditLogger):
        self.audit_logger = audit_logger
    
    def track_data_access(
        self,
        user_id: str,
        data_type: str,
        data_id: str,
        action: str,
        purpose: str,
        legal_basis: Optional[str] = None
    ):
        """Track data access for compliance purposes."""
        event_type_map = {
            "read": AuditEventType.DATA_READ,
            "write": AuditEventType.DATA_WRITE,
            "update": AuditEventType.DATA_UPDATE,
            "delete": AuditEventType.DATA_DELETE
        }
        
        event_type = event_type_map.get(action, AuditEventType.DATA_READ)
        
        self.audit_logger.log_event(
            event_type=event_type,
            user_id=user_id,
            resource_type=data_type,
            resource_id=data_id,
            description=f"Data {action}: {data_type}",
            details={
                "action": action,
                "purpose": purpose,
                "legal_basis": legal_basis,
                "data_type": data_type
            }
        )
    
    def track_consent_change(
        self,
        user_id: str,
        consent_type: str,
        granted: bool,
        purpose: str
    ):
        """Track consent changes for GDPR compliance."""
        event_type = AuditEventType.PRIVACY_CONSENT_GIVEN if granted else AuditEventType.PRIVACY_CONSENT_WITHDRAWN
        
        self.audit_logger.log_event(
            event_type=event_type,
            user_id=user_id,
            description=f"Consent {'granted' if granted else 'withdrawn'} for {consent_type}",
            details={
                "consent_type": consent_type,
                "granted": granted,
                "purpose": purpose
            }
        )
    
    def generate_gdpr_report(self, user_id: str) -> Dict[str, Any]:
        """Generate GDPR compliance report for a specific user."""
        # Get all audit events for the user
        events = self.audit_logger.get_audit_trail(user_id=user_id, limit=10000)
        
        # Categorize events
        data_access_events = []
        consent_events = []
        privacy_events = []
        
        for event in events:
            event_type = event["event_type"]
            
            if event_type in [e.value for e in [
                AuditEventType.DATA_READ, AuditEventType.DATA_WRITE,
                AuditEventType.DATA_UPDATE, AuditEventType.DATA_DELETE
            ]]:
                data_access_events.append(event)
            elif event_type in [e.value for e in [
                AuditEventType.PRIVACY_CONSENT_GIVEN, AuditEventType.PRIVACY_CONSENT_WITHDRAWN
            ]]:
                consent_events.append(event)
            elif event_type in [e.value for e in [
                AuditEventType.PRIVACY_DATA_REQUEST, AuditEventType.PRIVACY_DATA_DELETION,
                AuditEventType.PRIVACY_DATA_PORTABILITY
            ]]:
                privacy_events.append(event)
        
        return {
            "user_id": user_id,
            "generated_at": datetime.now(timezone.utc),
            "summary": {
                "total_events": len(events),
                "data_access_events": len(data_access_events),
                "consent_events": len(consent_events),
                "privacy_rights_events": len(privacy_events)
            },
            "data_access_log": data_access_events,
            "consent_history": consent_events,
            "privacy_rights_log": privacy_events
        }


# Global instances
_audit_logger: Optional[AuditLogger] = None
_security_auditor: Optional[SecurityAuditor] = None
_compliance_tracker: Optional[ComplianceTracker] = None


def get_audit_logger() -> AuditLogger:
    """Get the global audit logger instance."""
    global _audit_logger
    if _audit_logger is None:
        _audit_logger = AuditLogger()
    return _audit_logger


def get_security_auditor() -> SecurityAuditor:
    """Get the global security auditor instance."""
    global _security_auditor
    if _security_auditor is None:
        _security_auditor = SecurityAuditor(get_audit_logger())
    return _security_auditor


def get_compliance_tracker() -> ComplianceTracker:
    """Get the global compliance tracker instance."""
    global _compliance_tracker
    if _compliance_tracker is None:
        _compliance_tracker = ComplianceTracker(get_audit_logger())
    return _compliance_tracker


# Convenience functions
def audit_event(event_type: AuditEventType, **kwargs) -> str:
    """Convenience function to log an audit event."""
    return get_audit_logger().log_event(event_type, **kwargs)


def audit_data_access(user_id: str, data_type: str, data_id: str, action: str, purpose: str):
    """Convenience function to track data access."""
    get_compliance_tracker().track_data_access(user_id, data_type, data_id, action, purpose)


def audit_consent_change(user_id: str, consent_type: str, granted: bool, purpose: str):
    """Convenience function to track consent changes."""
    get_compliance_tracker().track_consent_change(user_id, consent_type, granted, purpose)
