"""
Happy Path Core Infrastructure Module

This module provides essential infrastructure components for the Happy Path
mental health wellness platform including database access, logging, monitoring,
auditing, and configuration management.

Components:
- Database: PostgreSQL connection management and query utilities
- Logging: Structured logging with multiple outputs and levels
- Monitoring: Performance metrics and health checks
- Auditing: User action tracking and compliance logging
- Configuration: Environment-based settings management
- Security: Authentication, authorization, and data protection
- Cache: Redis-based caching layer
- Events: Event-driven architecture support
"""

__version__ = "1.0.0"
__author__ = "Happy Path Development Team"

# Core component imports
from .database import DatabaseManager, get_db_connection, execute_query
from .logging import get_logger, setup_logging, LogLevel
from .monitoring import HealthChecker, MetricsCollector, PerformanceMonitor
from .auditing import AuditLogger, SecurityAuditor, ComplianceTracker
from .config import Config, get_config, Environment
from .security import SecurityManager, TokenManager, EncryptionService
from .cache import CacheManager, cache_key, invalidate_cache
from .events import EventManager, event_handler, publish_event

# Core exceptions
from .exceptions import (
    HappyPathError,
    DatabaseError,
    ConfigurationError,
    SecurityError,
    CacheError,
    MonitoringError,
    AuditError
)

__all__ = [
    # Database
    'DatabaseManager', 'get_db_connection', 'execute_query',
    
    # Logging
    'get_logger', 'setup_logging', 'LogLevel',
    
    # Monitoring
    'HealthChecker', 'MetricsCollector', 'PerformanceMonitor',
    
    # Auditing
    'AuditLogger', 'SecurityAuditor', 'ComplianceTracker',
    
    # Configuration
    'Config', 'get_config', 'Environment',
    
    # Security
    'SecurityManager', 'TokenManager', 'EncryptionService',
    
    # Cache
    'CacheManager', 'cache_key', 'invalidate_cache',
    
    # Events
    'EventManager', 'event_handler', 'publish_event',
    
    # Exceptions
    'HappyPathError', 'DatabaseError', 'ConfigurationError',
    'SecurityError', 'CacheError', 'MonitoringError', 'AuditError'
]
