"""
Security management for the Happy Path platform.
Provides authentication, authorization, encryption, and token management.
"""

import jwt
import bcrypt
import secrets
import hashlib
import base64
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import re

from .config import get_config
from .database import execute_query
from .logging import get_logger
from .exceptions import SecurityError, AuthenticationError, AuthorizationError, TokenError, EncryptionError

logger = get_logger(__name__)


@dataclass
class TokenPayload:
    """JWT token payload structure."""
    user_id: str
    email: str
    role: str
    subscription_type: str
    session_id: str
    issued_at: datetime
    expires_at: datetime


@dataclass
class AuthContext:
    """Authentication context information."""
    user_id: str
    email: str
    role: str
    subscription_type: str
    session_id: str
    permissions: List[str]
    is_authenticated: bool
    token: Optional[str] = None


class SecurityManager:
    """Main security management class."""
    
    def __init__(self):
        self.config = get_config()
        self._validate_security_config()
    
    def _validate_security_config(self):
        """Validate security configuration."""
        if not self.config.security.secret_key:
            raise SecurityError("SECRET_KEY not configured")
        if not self.config.security.jwt_secret:
            raise SecurityError("JWT_SECRET not configured")
        if len(self.config.security.secret_key) < 32:
            raise SecurityError("SECRET_KEY must be at least 32 characters")
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        if not self._validate_password_strength(password):
            raise SecurityError("Password does not meet security requirements")
        
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification failed: {e}")
            return False
    
    def _validate_password_strength(self, password: str) -> bool:
        """Validate password strength requirements."""
        min_length = self.config.security.password_min_length
        require_special = self.config.security.password_require_special
        
        if len(password) < min_length:
            return False
        
        # Check for uppercase, lowercase, digit
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        
        # Check for special characters if required
        if require_special and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False
        
        return True
    
    def generate_secure_token(self, length: int = 32) -> str:
        """Generate a cryptographically secure random token."""
        return secrets.token_urlsafe(length)
    
    def generate_session_id(self) -> str:
        """Generate a unique session ID."""
        return self.generate_secure_token(16)
    
    def hash_data(self, data: str, algorithm: str = "sha256") -> str:
        """Hash data using specified algorithm."""
        if algorithm == "sha256":
            return hashlib.sha256(data.encode('utf-8')).hexdigest()
        elif algorithm == "sha512":
            return hashlib.sha512(data.encode('utf-8')).hexdigest()
        else:
            raise SecurityError(f"Unsupported hash algorithm: {algorithm}")


class TokenManager:
    """JWT token management."""
    
    def __init__(self):
        self.config = get_config()
        self.algorithm = "HS256"
    
    def create_access_token(
        self,
        user_id: str,
        email: str,
        role: str,
        subscription_type: str,
        session_id: str,
        expires_in_hours: Optional[int] = None
    ) -> str:
        """Create a JWT access token."""
        
        expires_in = expires_in_hours or self.config.security.jwt_expiry_hours
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(hours=expires_in)
        
        payload = {
            "user_id": user_id,
            "email": email,
            "role": role,
            "subscription_type": subscription_type,
            "session_id": session_id,
            "iat": now.timestamp(),
            "exp": expires_at.timestamp(),
            "type": "access"
        }
        
        try:
            token = jwt.encode(payload, self.config.security.jwt_secret, algorithm=self.algorithm)
            return token
        except Exception as e:
            logger.error(f"Token creation failed: {e}")
            raise TokenError(f"Failed to create access token: {e}")
    
    def create_refresh_token(self, user_id: str, session_id: str) -> str:
        """Create a refresh token."""
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(days=30)  # Refresh tokens last 30 days
        
        payload = {
            "user_id": user_id,
            "session_id": session_id,
            "iat": now.timestamp(),
            "exp": expires_at.timestamp(),
            "type": "refresh"
        }
        
        try:
            token = jwt.encode(payload, self.config.security.jwt_secret, algorithm=self.algorithm)
            return token
        except Exception as e:
            logger.error(f"Refresh token creation failed: {e}")
            raise TokenError(f"Failed to create refresh token: {e}")
    
    def verify_token(self, token: str) -> TokenPayload:
        """Verify and decode a JWT token."""
        try:
            payload = jwt.decode(
                token,
                self.config.security.jwt_secret,
                algorithms=[self.algorithm]
            )
            
            return TokenPayload(
                user_id=payload["user_id"],
                email=payload["email"],
                role=payload["role"],
                subscription_type=payload["subscription_type"],
                session_id=payload["session_id"],
                issued_at=datetime.fromtimestamp(payload["iat"], tz=timezone.utc),
                expires_at=datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
            )
            
        except jwt.ExpiredSignatureError:
            raise TokenError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise TokenError(f"Invalid token: {e}")
        except KeyError as e:
            raise TokenError(f"Missing required token field: {e}")
    
    def refresh_access_token(self, refresh_token: str) -> str:
        """Create a new access token using a refresh token."""
        try:
            payload = jwt.decode(
                refresh_token,
                self.config.security.jwt_secret,
                algorithms=[self.algorithm]
            )
            
            if payload.get("type") != "refresh":
                raise TokenError("Invalid token type for refresh")
            
            user_id = payload["user_id"]
            session_id = payload["session_id"]
            
            # Get user information from database
            user_data = execute_query(
                "SELECT email, role, subscription_type FROM user_view WHERE user_id = %s",
                (user_id,),
                fetch_one=True
            )
            
            if not user_data:
                raise TokenError("User not found")
            
            # Create new access token
            return self.create_access_token(
                user_id=user_id,
                email=user_data["email"],
                role=user_data["role"],
                subscription_type=user_data["subscription_type"],
                session_id=session_id
            )
            
        except jwt.ExpiredSignatureError:
            raise TokenError("Refresh token has expired")
        except jwt.InvalidTokenError as e:
            raise TokenError(f"Invalid refresh token: {e}")


class EncryptionService:
    """Data encryption and decryption service."""
    
    def __init__(self):
        self.config = get_config()
        self._fernet = self._create_fernet_instance()
    
    def _create_fernet_instance(self) -> Fernet:
        """Create Fernet instance from encryption key."""
        if not self.config.security.encryption_key:
            raise EncryptionError("Encryption key not configured")
        
        try:
            # If the key is base64 encoded, use it directly
            key = self.config.security.encryption_key.encode()
            if len(key) == 44:  # Base64 encoded 32-byte key
                return Fernet(key)
            
            # Otherwise, derive key from password
            kdf = PBKDF2HMAC(
                algorithm=hashes.SHA256(),
                length=32,
                salt=b'happy_path_salt',  # In production, use random salt per encryption
                iterations=100000,
            )
            key = base64.urlsafe_b64encode(kdf.derive(self.config.security.encryption_key.encode()))
            return Fernet(key)
            
        except Exception as e:
            raise EncryptionError(f"Failed to create encryption instance: {e}")
    
    @classmethod
    def generate_key(cls) -> str:
        """Generate a new encryption key."""
        return Fernet.generate_key().decode()
    
    def encrypt(self, data: str) -> str:
        """Encrypt string data."""
        try:
            encrypted_data = self._fernet.encrypt(data.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            raise EncryptionError(f"Encryption failed: {e}")
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt string data."""
        try:
            encrypted_bytes = base64.urlsafe_b64decode(encrypted_data.encode('utf-8'))
            decrypted_data = self._fernet.decrypt(encrypted_bytes)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            raise EncryptionError(f"Decryption failed: {e}")
    
    def encrypt_dict(self, data: Dict[str, Any]) -> str:
        """Encrypt dictionary data as JSON."""
        import json
        json_data = json.dumps(data, default=str)
        return self.encrypt(json_data)
    
    def decrypt_dict(self, encrypted_data: str) -> Dict[str, Any]:
        """Decrypt data and parse as JSON dictionary."""
        import json
        decrypted_json = self.decrypt(encrypted_data)
        return json.loads(decrypted_json)


class PermissionManager:
    """Role-based access control and permissions."""
    
    # Define role hierarchy
    ROLE_HIERARCHY = {
        "user": 0,
        "premium_user": 1,
        "provider": 2,
        "admin": 3,
        "superadmin": 4
    }
    
    # Define permissions for each role
    ROLE_PERMISSIONS = {
        "user": [
            "mood:read", "mood:write",
            "journal:read", "journal:write",
            "profile:read", "profile:write",
            "subscription:read"
        ],
        "premium_user": [
            "mood:read", "mood:write",
            "journal:read", "journal:write",
            "profile:read", "profile:write",
            "subscription:read", "subscription:write",
            "analytics:read",
            "provider:message"
        ],
        "provider": [
            "patient:read", "patient:message",
            "appointment:read", "appointment:write",
            "clinical:read", "clinical:write",
            "profile:read", "profile:write"
        ],
        "admin": [
            "users:read", "users:write",
            "system:read", "system:write",
            "analytics:read", "analytics:write",
            "audit:read"
        ],
        "superadmin": ["*"]  # All permissions
    }
    
    def get_user_permissions(self, role: str) -> List[str]:
        """Get permissions for a user role."""
        return self.ROLE_PERMISSIONS.get(role, [])
    
    def has_permission(self, user_role: str, required_permission: str) -> bool:
        """Check if a user role has a specific permission."""
        user_permissions = self.get_user_permissions(user_role)
        
        # Superadmin has all permissions
        if "*" in user_permissions:
            return True
        
        # Check exact permission match
        if required_permission in user_permissions:
            return True
        
        # Check wildcard permissions
        for permission in user_permissions:
            if permission.endswith(":*"):
                permission_prefix = permission[:-1]  # Remove the *
                if required_permission.startswith(permission_prefix):
                    return True
        
        return False
    
    def can_access_user_data(self, accessor_role: str, accessor_id: str, target_user_id: str) -> bool:
        """Check if a user can access another user's data."""
        # Users can access their own data
        if accessor_id == target_user_id:
            return True
        
        # Providers can access their patients' data
        if accessor_role == "provider":
            # Check if there's an active therapeutic relationship
            result = execute_query(
                """
                SELECT 1 FROM therapeutic_relationships 
                WHERE therapist_id = %s AND patient_id = %s AND status = 'active'
                """,
                (accessor_id, target_user_id),
                fetch_one=True
            )
            return bool(result)
        
        # Admins can access user data
        if accessor_role in ["admin", "superadmin"]:
            return True
        
        return False


class AuthenticationService:
    """User authentication service."""
    
    def __init__(self):
        self.security_manager = SecurityManager()
        self.token_manager = TokenManager()
        self.config = get_config()
    
    def authenticate_user(self, email: str, password: str, ip_address: str, user_agent: str) -> AuthContext:
        """Authenticate a user with email and password."""
        from .auditing import get_security_auditor
        
        try:
            # Get user from database
            user_data = execute_query(
                """
                SELECT user_id, email, password_hash, role, is_active, failed_login_attempts, 
                       locked_until, subscription_type
                FROM user_view 
                WHERE email = %s
                """,
                (email,),
                fetch_one=True
            )
            
            if not user_data:
                # Log failed attempt for non-existent user
                get_security_auditor().track_login_attempt("unknown", ip_address, user_agent, False)
                raise AuthenticationError("Invalid email or password")
            
            user_id = user_data["user_id"]
            
            # Check if account is locked
            if user_data["locked_until"] and user_data["locked_until"] > datetime.now(timezone.utc):
                get_security_auditor().track_login_attempt(user_id, ip_address, user_agent, False)
                raise AuthenticationError("Account is temporarily locked")
            
            # Check if account is active
            if not user_data["is_active"]:
                get_security_auditor().track_login_attempt(user_id, ip_address, user_agent, False)
                raise AuthenticationError("Account is disabled")
            
            # Verify password
            if not self.security_manager.verify_password(password, user_data["password_hash"]):
                # Increment failed attempts
                self._handle_failed_login(user_id)
                get_security_auditor().track_login_attempt(user_id, ip_address, user_agent, False)
                raise AuthenticationError("Invalid email or password")
            
            # Reset failed attempts on successful login
            self._reset_failed_attempts(user_id)
            
            # Create session
            session_id = self.security_manager.generate_session_id()
            
            # Create auth context
            permission_manager = PermissionManager()
            auth_context = AuthContext(
                user_id=user_id,
                email=user_data["email"],
                role=user_data["role"],
                subscription_type=user_data["subscription_type"],
                session_id=session_id,
                permissions=permission_manager.get_user_permissions(user_data["role"]),
                is_authenticated=True
            )
            
            # Create access token
            auth_context.token = self.token_manager.create_access_token(
                user_id=user_id,
                email=user_data["email"],
                role=user_data["role"],
                subscription_type=user_data["subscription_type"],
                session_id=session_id
            )
            
            # Log successful login
            get_security_auditor().track_login_attempt(user_id, ip_address, user_agent, True)
            
            return auth_context
            
        except AuthenticationError:
            raise
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            raise AuthenticationError("Authentication failed")
    
    def _handle_failed_login(self, user_id: str):
        """Handle failed login attempt."""
        max_attempts = self.config.security.max_login_attempts
        lockout_duration = self.config.security.lockout_duration_minutes
        
        # Increment failed attempts
        execute_query(
            """
            UPDATE users 
            SET failed_login_attempts = failed_login_attempts + 1,
                last_failed_login = CURRENT_TIMESTAMP
            WHERE user_id = %s
            """,
            (user_id,),
            fetch_all=False
        )
        
        # Check if account should be locked
        user_data = execute_query(
            "SELECT failed_login_attempts FROM users WHERE user_id = %s",
            (user_id,),
            fetch_one=True
        )
        
        if user_data and user_data["failed_login_attempts"] >= max_attempts:
            locked_until = datetime.now(timezone.utc) + timedelta(minutes=lockout_duration)
            execute_query(
                "UPDATE users SET locked_until = %s WHERE user_id = %s",
                (locked_until, user_id),
                fetch_all=False
            )
    
    def _reset_failed_attempts(self, user_id: str):
        """Reset failed login attempts after successful login."""
        execute_query(
            """
            UPDATE users 
            SET failed_login_attempts = 0, 
                locked_until = NULL,
                last_login = CURRENT_TIMESTAMP
            WHERE user_id = %s
            """,
            (user_id,),
            fetch_all=False
        )


# Global instances
_security_manager: Optional[SecurityManager] = None
_token_manager: Optional[TokenManager] = None
_encryption_service: Optional[EncryptionService] = None
_permission_manager: Optional[PermissionManager] = None
_authentication_service: Optional[AuthenticationService] = None


def get_security_manager() -> SecurityManager:
    """Get the global security manager instance."""
    global _security_manager
    if _security_manager is None:
        _security_manager = SecurityManager()
    return _security_manager


def get_token_manager() -> TokenManager:
    """Get the global token manager instance."""
    global _token_manager
    if _token_manager is None:
        _token_manager = TokenManager()
    return _token_manager


def get_encryption_service() -> EncryptionService:
    """Get the global encryption service instance."""
    global _encryption_service
    if _encryption_service is None:
        _encryption_service = EncryptionService()
    return _encryption_service


def get_permission_manager() -> PermissionManager:
    """Get the global permission manager instance."""
    global _permission_manager
    if _permission_manager is None:
        _permission_manager = PermissionManager()
    return _permission_manager


def get_authentication_service() -> AuthenticationService:
    """Get the global authentication service instance."""
    global _authentication_service
    if _authentication_service is None:
        _authentication_service = AuthenticationService()
    return _authentication_service


# Convenience functions
def hash_password(password: str) -> str:
    """Hash a password."""
    return get_security_manager().hash_password(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password."""
    return get_security_manager().verify_password(password, hashed_password)


def create_access_token(user_id: str, email: str, role: str, subscription_type: str, session_id: str) -> str:
    """Create an access token."""
    return get_token_manager().create_access_token(user_id, email, role, subscription_type, session_id)


def verify_token(token: str) -> TokenPayload:
    """Verify and decode a token."""
    return get_token_manager().verify_token(token)


def encrypt_data(data: str) -> str:
    """Encrypt data."""
    return get_encryption_service().encrypt(data)


def decrypt_data(encrypted_data: str) -> str:
    """Decrypt data."""
    return get_encryption_service().decrypt(encrypted_data)
