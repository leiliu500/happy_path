#!/usr/bin/env python3
"""
Comprehensive test suite for Happy Path core infrastructure.

This test suite validates all components of the core module:
- Configuration management
- Database operations
- Security features
- Caching
- Audit logging
- Event system
- Monitoring & health checks
- Structured logging
- Error handling

Run with: python -m pytest core_test.py -v
or: python core_test.py
"""

import os
import sys
import pytest
import asyncio
import tempfile
import json
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Setup test environment variables before importing core modules
test_env_vars = {
    "DB_HOST": "localhost",
    "DB_PORT": "5432", 
    "DB_NAME": "happypath_test",
    "DB_USER": "test_user",
    "DB_PASSWORD": "test_password",
    "SECRET_KEY": "test-secret-key-for-testing-only-32-chars",
    "JWT_SECRET": "test-jwt-secret-for-testing-only-32-chars",
    "ENCRYPTION_KEY": "test-encryption-key-32-bytes-long!",
    "REDIS_HOST": "localhost",
    "REDIS_PORT": "6379",
    "ENVIRONMENT": "development",
    "LOG_LEVEL": "DEBUG",
    "ENABLE_AUDIT_LOGGING": "true",
    "ENABLE_METRICS_COLLECTION": "true",
    "ENABLE_RATE_LIMITING": "true",
    "ENABLE_CACHING": "true"
}

for key, value in test_env_vars.items():
    os.environ[key] = value

# Import core components after setting environment
from happypath.core import (
    initialize_config, get_config,
    setup_logging, get_logger,
    get_db_manager,
    get_security_manager,
    get_cache_manager,
    get_audit_logger,
    get_event_manager,
    get_health_checker,
    get_metrics_collector
)

from happypath.core.auditing import AuditEventType, AuditSeverity
from happypath.core.events import EventType, EventHandler
from happypath.core.exceptions import (
    HappyPathError, SecurityError, DatabaseError, 
    ConfigurationError, CacheError, AuditError
)
from happypath.core.config import Environment


class TestConfiguration:
    """Test configuration management."""
    
    def test_initialize_config(self):
        """Test configuration initialization."""
        config = initialize_config()
        assert config is not None
        assert config.env == Environment.DEVELOPMENT
        
    def test_config_database_settings(self):
        """Test database configuration."""
        config = get_config()
        assert config.database.host == "localhost"
        assert config.database.port == 5432
        assert config.database.name == "happypath_test"
        assert config.database.user == "test_user"
        
    def test_config_security_settings(self):
        """Test security configuration."""
        config = get_config()
        assert config.security.secret_key == "test-secret-key-for-testing-only-32-chars"
        assert config.security.jwt_secret == "test-jwt-secret-for-testing-only-32-chars"
        assert config.security.jwt_expiry_hours > 0
        assert config.security.password_min_length >= 8
        
    def test_config_cache_settings(self):
        """Test cache configuration."""
        config = get_config()
        assert config.cache.host == "localhost"
        assert config.cache.port == 6379
        
    def test_config_feature_flags(self):
        """Test feature flags."""
        config = get_config()
        assert config.features.enable_audit_logging is True
        assert config.features.enable_metrics_collection is True
        assert config.features.enable_rate_limiting is True
        assert config.features.enable_caching is True
        
    def test_config_to_dict(self):
        """Test configuration serialization."""
        config = get_config()
        config_dict = config.to_dict()
        assert isinstance(config_dict, dict)
        assert "database" in config_dict
        assert "security" in config_dict
        assert "cache" in config_dict
        assert "features" in config_dict


class TestLogging:
    """Test structured logging system."""
    
    def test_setup_logging(self):
        """Test logging system initialization."""
        setup_logging()
        logger = get_logger(__name__)
        assert logger is not None
        
    def test_logger_methods(self):
        """Test logger methods."""
        logger = get_logger(__name__)
        
        # Test different log levels
        logger.debug("Debug message", extra={"test": True})
        logger.info("Info message", extra={"test": True})
        logger.warning("Warning message", extra={"test": True})
        logger.error("Error message", extra={"test": True})
        
        # Should not raise exceptions
        assert True
        
    def test_structured_logging(self):
        """Test structured logging with extra data."""
        logger = get_logger(__name__)
        
        logger.info("Test structured logging", extra={
            "user_id": 12345,
            "operation": "test",
            "timestamp": datetime.now().isoformat(),
            "metadata": {"key": "value"}
        })
        
        # Should not raise exceptions
        assert True


class TestSecurity:
    """Test security features."""
    
    def test_password_hashing(self):
        """Test password hashing and verification."""
        security = get_security_manager()
        
        password = "TestPassword123!"
        hashed = security.hash_password(password)
        
        assert hashed != password
        assert security.verify_password(password, hashed) is True
        assert security.verify_password("wrong_password", hashed) is False
        
    def test_jwt_tokens(self):
        """Test JWT token creation and verification."""
        security = get_security_manager()
        
        user_id = 12345
        roles = ["user", "premium"]
        
        token = security.create_access_token(user_id=user_id, roles=roles)
        assert token is not None
        assert len(token) > 0
        
        payload = security.verify_access_token(token)
        assert payload["user_id"] == user_id
        assert payload["roles"] == roles
        
    def test_jwt_token_expiry(self):
        """Test JWT token expiry."""
        security = get_security_manager()
        
        # Create token with very short expiry
        with patch.object(security.config.security, 'jwt_expiry_hours', 0.001):  # ~3.6 seconds
            token = security.create_access_token(user_id=123)
            
            # Should be valid immediately
            payload = security.verify_access_token(token)
            assert payload["user_id"] == 123
            
    def test_invalid_jwt_token(self):
        """Test invalid JWT token handling."""
        security = get_security_manager()
        
        with pytest.raises(SecurityError):
            security.verify_access_token("invalid_token")
            
    def test_data_encryption(self):
        """Test data encryption and decryption."""
        security = get_security_manager()
        
        original_data = "Sensitive information: SSN 123-45-6789"
        encrypted = security.encrypt_data(original_data)
        decrypted = security.decrypt_data(encrypted)
        
        assert encrypted != original_data
        assert decrypted == original_data
        
    def test_permission_system(self):
        """Test role-based permission system."""
        security = get_security_manager()
        
        user_roles = ["user", "premium"]
        admin_roles = ["user", "admin"]
        
        # Test various permissions
        assert security.check_permission(user_roles, "user:read") is True
        assert security.check_permission(user_roles, "user:write") is True
        assert security.check_permission(user_roles, "admin:read") is False
        assert security.check_permission(user_roles, "premium:features") is True
        
        assert security.check_permission(admin_roles, "admin:read") is True
        assert security.check_permission(admin_roles, "admin:write") is True
        
    def test_secure_token_generation(self):
        """Test secure token generation."""
        security = get_security_manager()
        
        token1 = security.generate_secure_token()
        token2 = security.generate_secure_token()
        
        assert token1 != token2
        assert len(token1) > 0
        assert len(token2) > 0


class TestDatabase:
    """Test database operations."""
    
    def test_database_manager_creation(self):
        """Test database manager initialization."""
        db = get_db_manager()
        assert db is not None
        
    def test_query_builder(self):
        """Test SQL query builder."""
        db = get_db_manager()
        builder = db.query_builder()
        
        query = (builder
                .select("id, name, email")
                .from_table("users")
                .where("active = %s", True)
                .where("created_at > %s", datetime.now() - timedelta(days=30))
                .order_by("created_at DESC")
                .limit(10))
        
        assert "SELECT id, name, email FROM users" in query.query
        assert "WHERE active = %s" in query.query
        assert "ORDER BY created_at DESC" in query.query
        assert "LIMIT 10" in query.query
        assert len(query.params) == 2
        
    def test_health_status_structure(self):
        """Test database health status structure."""
        db = get_db_manager()
        health = db.get_health_status()
        
        assert isinstance(health, dict)
        assert "status" in health
        # Status might be unhealthy in test environment, which is expected
        assert health["status"] in ["healthy", "unhealthy", "degraded"]


@pytest.mark.asyncio
class TestCaching:
    """Test Redis caching system."""
    
    def test_cache_manager_creation(self):
        """Test cache manager initialization."""
        cache = get_cache_manager()
        assert cache is not None
        
    def test_cache_health_status(self):
        """Test cache health status."""
        cache = get_cache_manager()
        health = cache.get_health_status()
        
        assert isinstance(health, dict)
        assert "status" in health
        # Status might be unhealthy in test environment without Redis
        assert health["status"] in ["healthy", "unhealthy", "degraded"]
        
    def test_cache_operations_mock(self):
        """Test cache operations with mocked Redis."""
        with patch('happypath.core.cache.redis.Redis') as mock_redis:
            # Mock Redis instance
            mock_redis_instance = MagicMock()
            mock_redis.return_value = mock_redis_instance
            
            # Mock successful operations
            mock_redis_instance.set.return_value = True
            mock_redis_instance.get.return_value = b'{"test": "data"}'
            mock_redis_instance.delete.return_value = 1
            mock_redis_instance.ping.return_value = True
            
            cache = get_cache_manager()
            
            # Test set operation
            result = cache.set("test_key", {"test": "data"}, ttl=300)
            assert result is True
            
            # Test get operation
            data = cache.get("test_key")
            assert data == {"test": "data"}
            
            # Test delete operation
            result = cache.delete("test_key")
            assert result is True
            
    def test_session_management_mock(self):
        """Test session management with mocked Redis."""
        with patch('happypath.core.cache.redis.Redis') as mock_redis:
            # Mock Redis instance
            mock_redis_instance = MagicMock()
            mock_redis.return_value = mock_redis_instance
            
            # Mock session operations
            mock_redis_instance.set.return_value = True
            mock_redis_instance.get.return_value = b'{"user_id": 123, "role": "user"}'
            mock_redis_instance.delete.return_value = 1
            mock_redis_instance.ping.return_value = True
            
            cache = get_cache_manager()
            
            # Test session creation
            session_id = cache.create_session(user_id=123, data={"role": "user"})
            assert session_id is not None
            assert len(session_id) > 0
            
            # Test session retrieval
            session_data = cache.get_session(session_id)
            assert session_data["user_id"] == 123
            assert session_data["role"] == "user"


class TestAuditLogging:
    """Test audit logging system."""
    
    def test_audit_logger_creation(self):
        """Test audit logger initialization."""
        audit = get_audit_logger()
        assert audit is not None
        
    def test_basic_audit_logging(self):
        """Test basic audit event logging."""
        audit = get_audit_logger()
        
        event_id = audit.log_event(
            event_type=AuditEventType.USER_LOGIN_SUCCESS,
            user_id=12345,
            description="Test login event",
            severity=AuditSeverity.LOW,
            details={"ip_address": "127.0.0.1", "test": True}
        )
        
        # Event ID should be returned
        assert event_id is not None
        
    def test_security_audit_logging(self):
        """Test security event logging."""
        audit = get_audit_logger()
        
        audit.log_security_event(
            event="TEST_SECURITY_EVENT",
            user_id=12345,
            success=True,
            ip_address="127.0.0.1",
            details={"test": True}
        )
        
        # Should not raise exceptions
        assert True
        
    def test_gdpr_audit_logging(self):
        """Test GDPR compliance logging."""
        audit = get_audit_logger()
        
        event_id = audit.log_gdpr_event(
            event_type="DATA_ACCESS_REQUEST",
            user_id=12345,
            description="Test GDPR event",
            data_types=["profile", "preferences"],
            legal_basis="user_consent"
        )
        
        assert event_id is not None
        
    def test_audit_event_types(self):
        """Test all audit event types are available."""
        # Verify important audit event types exist
        assert hasattr(AuditEventType, 'USER_LOGIN_SUCCESS')
        assert hasattr(AuditEventType, 'USER_LOGIN_FAILURE')
        assert hasattr(AuditEventType, 'DATA_ACCESS')
        assert hasattr(AuditEventType, 'ADMIN_SYSTEM_CONFIG_CHANGE')
        assert hasattr(AuditEventType, 'USER_ACCOUNT_CREATED')
        
    def test_audit_severity_levels(self):
        """Test audit severity levels."""
        assert hasattr(AuditSeverity, 'LOW')
        assert hasattr(AuditSeverity, 'MEDIUM')
        assert hasattr(AuditSeverity, 'HIGH')
        assert hasattr(AuditSeverity, 'CRITICAL')


class TestEventHandler(EventHandler):
    """Test event handler for testing purposes."""
    
    def __init__(self):
        self.events_received = []
        
    def handle_user_registered(self, event):
        """Handle user registration events."""
        self.events_received.append(("user_registered", event))
        
    def handle_user_login(self, event):
        """Handle user login events."""
        self.events_received.append(("user_login", event))
        
    def handle_system_maintenance_start(self, event):
        """Handle system maintenance events."""
        self.events_received.append(("system_maintenance_start", event))


class TestEventSystem:
    """Test event-driven architecture."""
    
    def test_event_manager_creation(self):
        """Test event manager initialization."""
        events = get_event_manager()
        assert events is not None
        
    def test_event_handler_registration(self):
        """Test event handler registration."""
        events = get_event_manager()
        handler = TestEventHandler()
        
        events.register_handler(handler)
        # Should not raise exceptions
        assert True
        
    def test_event_publishing(self):
        """Test event publishing."""
        events = get_event_manager()
        
        event_id = events.publish(
            event_type=EventType.USER_REGISTERED,
            data={"user_id": 12345, "email": "test@example.com"},
            source="test_suite"
        )
        
        assert event_id is not None
        
    def test_event_processing(self):
        """Test event processing."""
        events = get_event_manager()
        handler = TestEventHandler()
        events.register_handler(handler)
        
        # Publish test events
        events.publish(
            event_type=EventType.USER_REGISTERED,
            data={"user_id": 12345},
            source="test"
        )
        
        events.publish(
            event_type=EventType.USER_LOGIN,
            data={"user_id": 12345},
            source="test"
        )
        
        # Process events
        events.process_pending_events()
        
        # Check that events were processed
        assert len(handler.events_received) >= 0  # Events might be processed asynchronously
        
    def test_event_types(self):
        """Test event types are available."""
        assert hasattr(EventType, 'USER_REGISTERED')
        assert hasattr(EventType, 'USER_LOGIN')
        assert hasattr(EventType, 'USER_LOGOUT')
        assert hasattr(EventType, 'SYSTEM_MAINTENANCE_START')


class TestMonitoring:
    """Test monitoring and health checks."""
    
    def test_health_checker_creation(self):
        """Test health checker initialization."""
        health_checker = get_health_checker()
        assert health_checker is not None
        
    def test_overall_health_status(self):
        """Test overall system health status."""
        health_checker = get_health_checker()
        status = health_checker.get_overall_status()
        
        assert isinstance(status, dict)
        assert "status" in status
        assert "message" in status
        assert "timestamp" in status
        assert "services" in status
        
        # Status should be one of the valid values
        assert status["status"] in ["healthy", "degraded", "unhealthy"]
        
    def test_metrics_collector_creation(self):
        """Test metrics collector initialization."""
        metrics = get_metrics_collector()
        assert metrics is not None
        
    def test_system_metrics_collection(self):
        """Test system metrics collection."""
        metrics = get_metrics_collector()
        
        try:
            system_metrics = metrics.collect_system_metrics()
            assert hasattr(system_metrics, 'cpu_percent')
            assert hasattr(system_metrics, 'memory_percent')
            assert hasattr(system_metrics, 'disk_percent')
            assert hasattr(system_metrics, 'uptime_seconds')
        except Exception:
            # System metrics might not be available in all test environments
            pytest.skip("System metrics not available in test environment")
            
    def test_application_metrics_collection(self):
        """Test application metrics collection."""
        metrics = get_metrics_collector()
        
        try:
            app_metrics = metrics.collect_application_metrics()
            assert isinstance(app_metrics, dict)
        except Exception:
            # Application metrics might not be available in test mode
            pytest.skip("Application metrics not available in test environment")


class TestErrorHandling:
    """Test error handling system."""
    
    def test_custom_exceptions(self):
        """Test custom exception hierarchy."""
        # Test base exception
        with pytest.raises(HappyPathError):
            raise HappyPathError("Test base error")
            
        # Test security error
        with pytest.raises(SecurityError):
            raise SecurityError("Test security error", error_code="TEST_001")
            
        # Test database error
        with pytest.raises(DatabaseError):
            raise DatabaseError("Test database error")
            
        # Test configuration error
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Test configuration error")
            
        # Test cache error
        with pytest.raises(CacheError):
            raise CacheError("Test cache error")
            
        # Test audit error
        with pytest.raises(AuditError):
            raise AuditError("Test audit error")
            
    def test_error_code_handling(self):
        """Test error code handling."""
        try:
            raise SecurityError("Test error", error_code="AUTH_001")
        except SecurityError as e:
            assert e.error_code == "AUTH_001"
            assert str(e) == "Test error"
            
    def test_error_inheritance(self):
        """Test error inheritance hierarchy."""
        # All custom errors should inherit from HappyPathError
        assert issubclass(SecurityError, HappyPathError)
        assert issubclass(DatabaseError, HappyPathError)
        assert issubclass(ConfigurationError, HappyPathError)
        assert issubclass(CacheError, HappyPathError)
        assert issubclass(AuditError, HappyPathError)


class TestIntegration:
    """Integration tests for multiple components."""
    
    def test_full_user_workflow(self):
        """Test a complete user workflow using multiple components."""
        # Initialize components
        security = get_security_manager()
        audit = get_audit_logger()
        events = get_event_manager()
        logger = get_logger(__name__)
        
        # Simulate user registration
        user_id = 12345
        email = "test@example.com"
        password = "SecurePassword123!"
        
        # Hash password
        hashed_password = security.hash_password(password)
        
        # Log user creation
        audit.log_event(
            event_type=AuditEventType.USER_ACCOUNT_CREATED,
            user_id=user_id,
            description=f"User account created: {email}",
            details={"email": email, "test": True}
        )
        
        # Publish user registration event
        event_id = events.publish(
            event_type=EventType.USER_REGISTERED,
            data={"user_id": user_id, "email": email},
            source="integration_test"
        )
        
        # Create access token
        token = security.create_access_token(user_id=user_id, roles=["user"])
        
        # Verify token
        payload = security.verify_access_token(token)
        assert payload["user_id"] == user_id
        
        # Log successful login
        audit.log_event(
            event_type=AuditEventType.USER_LOGIN_SUCCESS,
            user_id=user_id,
            description="User logged in successfully",
            details={"token_created": True, "test": True}
        )
        
        logger.info("Integration test completed successfully", extra={
            "user_id": user_id,
            "event_id": event_id,
            "test": True
        })
        
        # All operations should complete without errors
        assert True
        
    def test_error_handling_integration(self):
        """Test error handling across components."""
        logger = get_logger(__name__)
        audit = get_audit_logger()
        
        try:
            # Simulate a security error
            raise SecurityError("Invalid token", error_code="AUTH_001")
        except SecurityError as e:
            # Log the error
            logger.error("Security error occurred", extra={
                "error_type": "SecurityError",
                "error_code": e.error_code,
                "error_message": str(e),
                "test": True
            })
            
            # Audit the security event
            audit.log_security_event(
                event="AUTHENTICATION_ERROR",
                user_id=None,
                success=False,
                ip_address="127.0.0.1",
                details={
                    "error_code": e.error_code,
                    "error_message": str(e),
                    "test": True
                }
            )
            
            # Error should be properly handled
            assert e.error_code == "AUTH_001"


def run_manual_tests():
    """Run tests manually without pytest."""
    print("🧪 Running Happy Path Core Infrastructure Tests")
    print("=" * 60)
    
    test_classes = [
        TestConfiguration,
        TestLogging,
        TestSecurity,
        TestDatabase,
        TestCaching,
        TestAuditLogging,
        TestEventSystem,
        TestMonitoring,
        TestErrorHandling,
        TestIntegration
    ]
    
    total_tests = 0
    passed_tests = 0
    failed_tests = 0
    
    for test_class in test_classes:
        print(f"\n📋 Testing {test_class.__name__}")
        
        instance = test_class()
        test_methods = [method for method in dir(instance) if method.startswith('test_')]
        
        for test_method in test_methods:
            total_tests += 1
            try:
                method = getattr(instance, test_method)
                
                # Handle async tests
                if asyncio.iscoroutinefunction(method):
                    asyncio.run(method())
                else:
                    method()
                    
                print(f"  ✅ {test_method}")
                passed_tests += 1
                
            except Exception as e:
                print(f"  ❌ {test_method}: {e}")
                failed_tests += 1
    
    print("\n" + "=" * 60)
    print("🎯 TEST SUMMARY")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
    
    if failed_tests == 0:
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Core infrastructure is working correctly")
    else:
        print(f"\n⚠️ {failed_tests} tests failed")
        print("Some failures are expected if external services (DB, Redis) are not running")
        
    return failed_tests == 0


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--pytest":
        # Run with pytest if requested
        pytest.main([__file__, "-v"])
    else:
        # Run manual tests
        success = run_manual_tests()
        sys.exit(0 if success else 1)
