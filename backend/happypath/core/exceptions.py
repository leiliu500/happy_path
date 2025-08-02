"""
Core exceptions for the Happy Path platform.
Provides hierarchical exception structure for better error handling.
"""

class HappyPathError(Exception):
    """Base exception for all Happy Path platform errors."""
    
    def __init__(self, message: str, error_code: str = None, details: dict = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> dict:
        """Convert exception to dictionary for logging/API responses."""
        return {
            'error_type': self.__class__.__name__,
            'message': self.message,
            'error_code': self.error_code,
            'details': self.details
        }


class DatabaseError(HappyPathError):
    """Database-related errors."""
    pass


class ConnectionError(DatabaseError):
    """Database connection errors."""
    pass


class QueryError(DatabaseError):
    """Database query execution errors."""
    pass


class TransactionError(DatabaseError):
    """Database transaction errors."""
    pass


class ConfigurationError(HappyPathError):
    """Configuration and settings errors."""
    pass


class SecurityError(HappyPathError):
    """Security-related errors."""
    pass


class AuthenticationError(SecurityError):
    """Authentication failures."""
    pass


class AuthorizationError(SecurityError):
    """Authorization/permission errors."""
    pass


class TokenError(SecurityError):
    """JWT token errors."""
    pass


class EncryptionError(SecurityError):
    """Data encryption/decryption errors."""
    pass


class CacheError(HappyPathError):
    """Cache-related errors."""
    pass


class MonitoringError(HappyPathError):
    """Monitoring and metrics errors."""
    pass


class AuditError(HappyPathError):
    """Auditing and compliance errors."""
    pass


class ValidationError(HappyPathError):
    """Data validation errors."""
    pass


class RateLimitError(HappyPathError):
    """Rate limiting errors."""
    pass


class ExternalServiceError(HappyPathError):
    """External service integration errors."""
    pass


class PaymentError(HappyPathError):
    """Payment processing errors."""
    pass


class SubscriptionError(HappyPathError):
    """Subscription management errors."""
    pass
