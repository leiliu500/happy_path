"""
System Administration Repository

Repository implementation for system administration, user management,
audit trails, and platform configuration.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, date, timedelta
from dataclasses import dataclass
from enum import Enum
from decimal import Decimal
import logging
import json

from .base_repository import BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult
from .base_repository import ValidationError, NotFoundError


class UserRole(Enum):
    """User role enumeration."""
    PATIENT = "patient"
    THERAPIST = "therapist"
    ADMIN = "admin"
    SUPERVISOR = "supervisor"
    MODERATOR = "moderator"
    SUPPORT = "support"
    RESEARCHER = "researcher"
    BILLING = "billing"


class UserStatus(Enum):
    """User status enumeration."""
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING = "pending"
    ARCHIVED = "archived"


class ActionType(Enum):
    """Audit action type enumeration."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    ACCESS = "access"
    EXPORT = "export"
    IMPORT = "import"
    BACKUP = "backup"
    RESTORE = "restore"


class AuditSeverity(Enum):
    """Audit severity enumeration."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class SystemConfigType(Enum):
    """System configuration type enumeration."""
    SECURITY = "security"
    NOTIFICATION = "notification"
    INTEGRATION = "integration"
    FEATURE_FLAG = "feature_flag"
    PERFORMANCE = "performance"
    COMPLIANCE = "compliance"
    UI_SETTINGS = "ui_settings"
    API_SETTINGS = "api_settings"


@dataclass
class UserAccount:
    """User account entity."""
    user_id: Optional[str] = None
    
    # Basic information
    username: str = ""
    email: str = ""
    password_hash: Optional[str] = None
    
    # Profile information
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    profile_picture: Optional[str] = None
    phone_number: Optional[str] = None
    
    # Role and permissions
    role: UserRole = UserRole.PATIENT
    status: UserStatus = UserStatus.PENDING
    permissions: Optional[List[str]] = None
    
    # Security
    two_factor_enabled: bool = False
    two_factor_secret: Optional[str] = None
    last_password_change: Optional[datetime] = None
    failed_login_attempts: int = 0
    locked_until: Optional[datetime] = None
    
    # Session management
    last_login: Optional[datetime] = None
    last_active: Optional[datetime] = None
    session_token: Optional[str] = None
    session_expires: Optional[datetime] = None
    
    # Professional information (for therapists)
    license_number: Optional[str] = None
    license_state: Optional[str] = None
    license_expiry: Optional[date] = None
    specialty: Optional[str] = None
    credentials: Optional[List[str]] = None
    
    # Emergency contacts
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relationship: Optional[str] = None
    
    # Preferences
    timezone: Optional[str] = None
    language: str = "en"
    notification_preferences: Optional[Dict[str, bool]] = None
    
    # Terms and privacy
    terms_accepted: bool = False
    terms_accepted_at: Optional[datetime] = None
    privacy_policy_accepted: bool = False
    privacy_policy_accepted_at: Optional[datetime] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class AuditLog:
    """Audit log entity."""
    audit_id: Optional[str] = None
    
    # Who performed the action
    user_id: Optional[str] = None
    username: Optional[str] = None
    user_role: Optional[UserRole] = None
    
    # What action was performed
    action_type: ActionType = ActionType.READ
    resource_type: Optional[str] = None  # table name, API endpoint, etc.
    resource_id: Optional[str] = None
    
    # Action details
    description: str = ""
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    changes: Optional[Dict[str, Any]] = None
    
    # Context
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    session_id: Optional[str] = None
    request_id: Optional[str] = None
    
    # Classification
    severity: AuditSeverity = AuditSeverity.LOW
    tags: Optional[List[str]] = None
    
    # Success/failure
    success: bool = True
    error_message: Optional[str] = None
    
    # Compliance
    hipaa_relevant: bool = False
    pii_accessed: bool = False
    
    created_at: Optional[datetime] = None


@dataclass
class SystemConfiguration:
    """System configuration entity."""
    config_id: Optional[str] = None
    
    # Configuration identification
    key: str = ""
    category: SystemConfigType = SystemConfigType.FEATURE_FLAG
    name: Optional[str] = None
    description: Optional[str] = None
    
    # Configuration value
    value: Optional[Any] = None
    value_type: str = "string"  # string, number, boolean, json, array
    default_value: Optional[Any] = None
    
    # Constraints
    allowed_values: Optional[List[Any]] = None
    validation_pattern: Optional[str] = None
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    
    # Environment and deployment
    environment: str = "production"  # development, staging, production
    feature_flag: bool = False
    requires_restart: bool = False
    
    # Security and access
    is_sensitive: bool = False
    encrypted: bool = False
    access_level: str = "admin"  # public, user, admin, system
    
    # Management
    is_active: bool = True
    last_modified_by: Optional[str] = None
    change_reason: Optional[str] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass
class SystemAlert:
    """System alert entity."""
    alert_id: Optional[str] = None
    
    # Alert information
    title: str = ""
    message: str = ""
    alert_type: str = "info"  # info, warning, error, critical
    category: Optional[str] = None
    
    # Targeting
    target_users: Optional[List[str]] = None  # specific user IDs
    target_roles: Optional[List[UserRole]] = None
    target_all: bool = False
    
    # Scheduling
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
    display_until_dismissed: bool = False
    
    # Display options
    priority: int = 0  # higher numbers = higher priority
    show_on_dashboard: bool = True
    show_on_login: bool = False
    require_acknowledgment: bool = False
    
    # Styling
    color: Optional[str] = None
    icon: Optional[str] = None
    
    # Status
    is_active: bool = True
    created_by: Optional[str] = None
    
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserAccountRepository(BaseRepository[UserAccount, str]):
    """Repository for user account management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "user_accounts", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> UserAccount:
        """Convert database row to UserAccount entity."""
        return UserAccount(
            user_id=row.get('user_id'),
            username=row.get('username', ''),
            email=row.get('email', ''),
            password_hash=row.get('password_hash'),
            first_name=row.get('first_name'),
            last_name=row.get('last_name'),
            display_name=row.get('display_name'),
            profile_picture=row.get('profile_picture'),
            phone_number=row.get('phone_number'),
            role=UserRole(row['role']) if row.get('role') else UserRole.PATIENT,
            status=UserStatus(row['status']) if row.get('status') else UserStatus.PENDING,
            permissions=row.get('permissions', []),
            two_factor_enabled=row.get('two_factor_enabled', False),
            two_factor_secret=row.get('two_factor_secret'),
            last_password_change=row.get('last_password_change'),
            failed_login_attempts=row.get('failed_login_attempts', 0),
            locked_until=row.get('locked_until'),
            last_login=row.get('last_login'),
            last_active=row.get('last_active'),
            session_token=row.get('session_token'),
            session_expires=row.get('session_expires'),
            license_number=row.get('license_number'),
            license_state=row.get('license_state'),
            license_expiry=row.get('license_expiry'),
            specialty=row.get('specialty'),
            credentials=row.get('credentials', []),
            emergency_contact_name=row.get('emergency_contact_name'),
            emergency_contact_phone=row.get('emergency_contact_phone'),
            emergency_contact_relationship=row.get('emergency_contact_relationship'),
            timezone=row.get('timezone'),
            language=row.get('language', 'en'),
            notification_preferences=row.get('notification_preferences'),
            terms_accepted=row.get('terms_accepted', False),
            terms_accepted_at=row.get('terms_accepted_at'),
            privacy_policy_accepted=row.get('privacy_policy_accepted', False),
            privacy_policy_accepted_at=row.get('privacy_policy_accepted_at'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: UserAccount) -> Dict[str, Any]:
        """Convert UserAccount entity to dictionary."""
        return {
            'user_id': entity.user_id,
            'username': entity.username,
            'email': entity.email,
            'password_hash': entity.password_hash,
            'first_name': entity.first_name,
            'last_name': entity.last_name,
            'display_name': entity.display_name,
            'profile_picture': entity.profile_picture,
            'phone_number': entity.phone_number,
            'role': entity.role.value,
            'status': entity.status.value,
            'permissions': entity.permissions,
            'two_factor_enabled': entity.two_factor_enabled,
            'two_factor_secret': entity.two_factor_secret,
            'last_password_change': entity.last_password_change,
            'failed_login_attempts': entity.failed_login_attempts,
            'locked_until': entity.locked_until,
            'last_login': entity.last_login,
            'last_active': entity.last_active,
            'session_token': entity.session_token,
            'session_expires': entity.session_expires,
            'license_number': entity.license_number,
            'license_state': entity.license_state,
            'license_expiry': entity.license_expiry,
            'specialty': entity.specialty,
            'credentials': entity.credentials,
            'emergency_contact_name': entity.emergency_contact_name,
            'emergency_contact_phone': entity.emergency_contact_phone,
            'emergency_contact_relationship': entity.emergency_contact_relationship,
            'timezone': entity.timezone,
            'language': entity.language,
            'notification_preferences': entity.notification_preferences,
            'terms_accepted': entity.terms_accepted,
            'terms_accepted_at': entity.terms_accepted_at,
            'privacy_policy_accepted': entity.privacy_policy_accepted,
            'privacy_policy_accepted_at': entity.privacy_policy_accepted_at,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: UserAccount, is_update: bool = False) -> None:
        """Validate UserAccount entity."""
        if not entity.username:
            raise ValidationError("Username is required")
        
        if not entity.email:
            raise ValidationError("Email is required")
        
        # Email format validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, entity.email):
            raise ValidationError("Invalid email format")
        
        if entity.failed_login_attempts < 0:
            raise ValidationError("Failed login attempts cannot be negative")
        
        if entity.license_expiry and entity.license_expiry < date.today():
            self.logger.warning(f"License expired for user {entity.user_id}")
        
        if not entity.user_id and not is_update:
            import uuid
            entity.user_id = str(uuid.uuid4())
    
    def create_user(self, username: str, email: str, password_hash: str, 
                   role: UserRole = UserRole.PATIENT) -> UserAccount:
        """Create a new user account."""
        user = UserAccount(
            username=username,
            email=email,
            password_hash=password_hash,
            role=role,
            status=UserStatus.PENDING
        )
        
        created_user = self.create(user)
        
        self.logger.info(f"Created user account {created_user.user_id} with role {role.value}")
        return created_user
    
    def get_by_username(self, username: str) -> Optional[UserAccount]:
        """Get user by username."""
        return self.find_one_by(username=username)
    
    def get_by_email(self, email: str) -> Optional[UserAccount]:
        """Get user by email."""
        return self.find_one_by(email=email)
    
    def update_last_login(self, user_id: str) -> bool:
        """Update last login timestamp."""
        try:
            user = self.get_by_id(user_id)
            if not user:
                return False
            
            user.last_login = datetime.now()
            user.last_active = user.last_login
            user.failed_login_attempts = 0  # Reset on successful login
            
            self.update(user)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update last login: {e}")
            return False
    
    def increment_failed_login(self, user_id: str, max_attempts: int = 5,
                             lockout_duration_minutes: int = 30) -> bool:
        """Increment failed login attempts and lock if necessary."""
        try:
            user = self.get_by_id(user_id)
            if not user:
                return False
            
            user.failed_login_attempts += 1
            
            if user.failed_login_attempts >= max_attempts:
                user.locked_until = datetime.now() + timedelta(minutes=lockout_duration_minutes)
                user.status = UserStatus.SUSPENDED
                
                self.logger.warning(f"User {user_id} locked due to {max_attempts} failed login attempts")
            
            self.update(user)
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to increment failed login: {e}")
            return False
    
    def is_account_locked(self, user_id: str) -> bool:
        """Check if account is currently locked."""
        user = self.get_by_id(user_id)
        if not user:
            return True  # Treat non-existent users as locked
        
        if user.locked_until and user.locked_until > datetime.now():
            return True
        
        if user.status == UserStatus.SUSPENDED:
            return True
        
        return False
    
    def unlock_account(self, user_id: str) -> bool:
        """Unlock a user account."""
        try:
            user = self.get_by_id(user_id)
            if not user:
                return False
            
            user.failed_login_attempts = 0
            user.locked_until = None
            user.status = UserStatus.ACTIVE
            
            self.update(user)
            
            self.logger.info(f"Unlocked user account {user_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to unlock account: {e}")
            return False
    
    def get_users_by_role(self, role: UserRole, active_only: bool = True) -> List[UserAccount]:
        """Get users by role."""
        filters = {'role': role.value}
        if active_only:
            filters['status'] = UserStatus.ACTIVE.value
        
        options = QueryOptions(
            filters=filters,
            order_by=['last_name', 'first_name']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_expired_licenses(self, days_ahead: int = 30) -> List[UserAccount]:
        """Get users with licenses expiring soon."""
        cutoff_date = date.today() + timedelta(days=days_ahead)
        
        query = f"""
            SELECT * FROM {self.table_name}
            WHERE license_expiry IS NOT NULL
            AND license_expiry <= %(cutoff_date)s
            AND role IN ('therapist', 'supervisor')
            AND status = 'active'
            ORDER BY license_expiry
        """
        
        try:
            result = self.db.execute_query(query, {'cutoff_date': cutoff_date})
            return [self._to_entity(row) for row in result] if result else []
            
        except Exception as e:
            self.logger.error(f"Failed to get expired licenses: {e}")
            return []


class AuditLogRepository(BaseRepository[AuditLog, str]):
    """Repository for audit log management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "audit_logs", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> AuditLog:
        """Convert database row to AuditLog entity."""
        return AuditLog(
            audit_id=row.get('audit_id'),
            user_id=row.get('user_id'),
            username=row.get('username'),
            user_role=UserRole(row['user_role']) if row.get('user_role') else None,
            action_type=ActionType(row['action_type']) if row.get('action_type') else ActionType.READ,
            resource_type=row.get('resource_type'),
            resource_id=row.get('resource_id'),
            description=row.get('description', ''),
            old_values=row.get('old_values'),
            new_values=row.get('new_values'),
            changes=row.get('changes'),
            ip_address=row.get('ip_address'),
            user_agent=row.get('user_agent'),
            session_id=row.get('session_id'),
            request_id=row.get('request_id'),
            severity=AuditSeverity(row['severity']) if row.get('severity') else AuditSeverity.LOW,
            tags=row.get('tags', []),
            success=row.get('success', True),
            error_message=row.get('error_message'),
            hipaa_relevant=row.get('hipaa_relevant', False),
            pii_accessed=row.get('pii_accessed', False),
            created_at=row.get('created_at')
        )
    
    def _to_dict(self, entity: AuditLog) -> Dict[str, Any]:
        """Convert AuditLog entity to dictionary."""
        return {
            'audit_id': entity.audit_id,
            'user_id': entity.user_id,
            'username': entity.username,
            'user_role': entity.user_role.value if entity.user_role else None,
            'action_type': entity.action_type.value,
            'resource_type': entity.resource_type,
            'resource_id': entity.resource_id,
            'description': entity.description,
            'old_values': entity.old_values,
            'new_values': entity.new_values,
            'changes': entity.changes,
            'ip_address': entity.ip_address,
            'user_agent': entity.user_agent,
            'session_id': entity.session_id,
            'request_id': entity.request_id,
            'severity': entity.severity.value,
            'tags': entity.tags,
            'success': entity.success,
            'error_message': entity.error_message,
            'hipaa_relevant': entity.hipaa_relevant,
            'pii_accessed': entity.pii_accessed,
            'created_at': entity.created_at
        }
    
    def _validate_entity(self, entity: AuditLog, is_update: bool = False) -> None:
        """Validate AuditLog entity."""
        if not entity.description:
            raise ValidationError("Description is required")
        
        if not entity.audit_id and not is_update:
            import uuid
            entity.audit_id = str(uuid.uuid4())
        
        if not entity.created_at:
            entity.created_at = datetime.now()
    
    def log_action(self, user_id: str, action_type: ActionType, description: str,
                   resource_type: str = None, resource_id: str = None,
                   severity: AuditSeverity = AuditSeverity.LOW,
                   ip_address: str = None, user_agent: str = None,
                   old_values: Dict[str, Any] = None, new_values: Dict[str, Any] = None,
                   hipaa_relevant: bool = False, pii_accessed: bool = False,
                   success: bool = True, error_message: str = None) -> AuditLog:
        """Log an audit action."""
        
        # Get user information
        user_repo = UserAccountRepository(self.db, self.logger)
        user = user_repo.get_by_id(user_id) if user_id else None
        
        # Calculate changes
        changes = None
        if old_values and new_values:
            changes = {}
            for key in set(old_values.keys()) | set(new_values.keys()):
                old_val = old_values.get(key)
                new_val = new_values.get(key)
                if old_val != new_val:
                    changes[key] = {'old': old_val, 'new': new_val}
        
        audit_log = AuditLog(
            user_id=user_id,
            username=user.username if user else None,
            user_role=user.role if user else None,
            action_type=action_type,
            resource_type=resource_type,
            resource_id=resource_id,
            description=description,
            old_values=old_values,
            new_values=new_values,
            changes=changes,
            ip_address=ip_address,
            user_agent=user_agent,
            severity=severity,
            success=success,
            error_message=error_message,
            hipaa_relevant=hipaa_relevant,
            pii_accessed=pii_accessed
        )
        
        return self.create(audit_log)
    
    def get_user_activity(self, user_id: str, days_back: int = 30) -> List[AuditLog]:
        """Get recent activity for a user."""
        start_date = datetime.now() - timedelta(days=days_back)
        
        options = QueryOptions(
            filters={
                'user_id': user_id,
                'created_at__gte': start_date
            },
            order_by=['-created_at'],
            limit=1000
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_security_events(self, days_back: int = 7) -> List[AuditLog]:
        """Get security-related events."""
        start_date = datetime.now() - timedelta(days=days_back)
        
        security_actions = [ActionType.LOGIN.value, ActionType.LOGOUT.value]
        
        options = QueryOptions(
            filters={
                'created_at__gte': start_date,
                'action_type__in': security_actions
            },
            order_by=['-created_at'],
            limit=1000
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_failed_attempts(self, hours_back: int = 24) -> List[AuditLog]:
        """Get failed login attempts."""
        start_date = datetime.now() - timedelta(hours=hours_back)
        
        options = QueryOptions(
            filters={
                'created_at__gte': start_date,
                'action_type': ActionType.LOGIN.value,
                'success': False
            },
            order_by=['-created_at']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_hipaa_relevant_logs(self, start_date: datetime, end_date: datetime) -> List[AuditLog]:
        """Get HIPAA-relevant audit logs for compliance reporting."""
        options = QueryOptions(
            filters={
                'created_at__gte': start_date,
                'created_at__lte': end_date,
                'hipaa_relevant': True
            },
            order_by=['created_at']
        )
        
        result = self.list_all(options)
        return result.data


class SystemConfigurationRepository(BaseRepository[SystemConfiguration, str]):
    """Repository for system configuration management."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "system_configurations", logger)
    
    def _to_entity(self, row: Dict[str, Any]) -> SystemConfiguration:
        """Convert database row to SystemConfiguration entity."""
        return SystemConfiguration(
            config_id=row.get('config_id'),
            key=row.get('key', ''),
            category=SystemConfigType(row['category']) if row.get('category') else SystemConfigType.FEATURE_FLAG,
            name=row.get('name'),
            description=row.get('description'),
            value=row.get('value'),
            value_type=row.get('value_type', 'string'),
            default_value=row.get('default_value'),
            allowed_values=row.get('allowed_values'),
            validation_pattern=row.get('validation_pattern'),
            min_value=row.get('min_value'),
            max_value=row.get('max_value'),
            environment=row.get('environment', 'production'),
            feature_flag=row.get('feature_flag', False),
            requires_restart=row.get('requires_restart', False),
            is_sensitive=row.get('is_sensitive', False),
            encrypted=row.get('encrypted', False),
            access_level=row.get('access_level', 'admin'),
            is_active=row.get('is_active', True),
            last_modified_by=row.get('last_modified_by'),
            change_reason=row.get('change_reason'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    def _to_dict(self, entity: SystemConfiguration) -> Dict[str, Any]:
        """Convert SystemConfiguration entity to dictionary."""
        return {
            'config_id': entity.config_id,
            'key': entity.key,
            'category': entity.category.value,
            'name': entity.name,
            'description': entity.description,
            'value': entity.value,
            'value_type': entity.value_type,
            'default_value': entity.default_value,
            'allowed_values': entity.allowed_values,
            'validation_pattern': entity.validation_pattern,
            'min_value': entity.min_value,
            'max_value': entity.max_value,
            'environment': entity.environment,
            'feature_flag': entity.feature_flag,
            'requires_restart': entity.requires_restart,
            'is_sensitive': entity.is_sensitive,
            'encrypted': entity.encrypted,
            'access_level': entity.access_level,
            'is_active': entity.is_active,
            'last_modified_by': entity.last_modified_by,
            'change_reason': entity.change_reason,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at
        }
    
    def _validate_entity(self, entity: SystemConfiguration, is_update: bool = False) -> None:
        """Validate SystemConfiguration entity."""
        if not entity.key:
            raise ValidationError("Configuration key is required")
        
        # Validate value type
        if entity.value is not None:
            try:
                if entity.value_type == 'number':
                    float(entity.value)
                elif entity.value_type == 'boolean':
                    if entity.value not in [True, False, 'true', 'false', '1', '0']:
                        raise ValueError("Invalid boolean value")
                elif entity.value_type == 'json':
                    if isinstance(entity.value, str):
                        json.loads(entity.value)
            except (ValueError, json.JSONDecodeError):
                raise ValidationError(f"Invalid value for type {entity.value_type}")
        
        # Validate allowed values
        if entity.allowed_values and entity.value not in entity.allowed_values:
            raise ValidationError(f"Value must be one of: {entity.allowed_values}")
        
        # Validate range
        if entity.value_type == 'number' and entity.value is not None:
            val = float(entity.value)
            if entity.min_value is not None and val < float(entity.min_value):
                raise ValidationError(f"Value must be >= {entity.min_value}")
            if entity.max_value is not None and val > float(entity.max_value):
                raise ValidationError(f"Value must be <= {entity.max_value}")
        
        if not entity.config_id and not is_update:
            import uuid
            entity.config_id = str(uuid.uuid4())
    
    def get_by_key(self, key: str, environment: str = "production") -> Optional[SystemConfiguration]:
        """Get configuration by key."""
        return self.find_one_by(key=key, environment=environment, is_active=True)
    
    def get_by_category(self, category: SystemConfigType, 
                       environment: str = "production") -> List[SystemConfiguration]:
        """Get configurations by category."""
        options = QueryOptions(
            filters={
                'category': category.value,
                'environment': environment,
                'is_active': True
            },
            order_by=['key']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_feature_flags(self, environment: str = "production") -> List[SystemConfiguration]:
        """Get feature flag configurations."""
        options = QueryOptions(
            filters={
                'feature_flag': True,
                'environment': environment,
                'is_active': True
            },
            order_by=['key']
        )
        
        result = self.list_all(options)
        return result.data
    
    def update_config_value(self, key: str, value: Any, changed_by: str,
                           reason: str = None, environment: str = "production") -> bool:
        """Update configuration value."""
        try:
            config = self.get_by_key(key, environment)
            if not config:
                return False
            
            config.value = value
            config.last_modified_by = changed_by
            config.change_reason = reason
            
            self.update(config)
            
            self.logger.info(f"Updated config {key} = {value} by {changed_by}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update config value: {e}")
            return False
    
    def is_feature_enabled(self, feature_key: str, environment: str = "production") -> bool:
        """Check if a feature flag is enabled."""
        config = self.get_by_key(feature_key, environment)
        if not config or not config.feature_flag:
            return False
        
        if config.value_type == 'boolean':
            if isinstance(config.value, bool):
                return config.value
            if isinstance(config.value, str):
                return config.value.lower() in ['true', '1', 'yes', 'on']
        
        return bool(config.value)
