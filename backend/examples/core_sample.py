#!/usr/bin/env python3
"""
Happy Path Core Infrastructure Usage Example.

This example demonstrates how to use all components of the core module:
- Configuration management
- Database operations
- Security features
- Caching
- Audit logging
- Event system
- Monitoring & health checks
- Structured logging

Run this example to see the core infrastructure in action:
    cd backend/examples
    python core_sample.py
"""

import os
import sys
import asyncio
from datetime import datetime, timedelta
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir))

# Import all core components
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

# Import specific classes and enums
from happypath.core.auditing import AuditEventType, AuditSeverity
from happypath.core.events import EventType, EventHandler
from happypath.core.exceptions import HappyPathError, SecurityError


class SampleUserEventHandler(EventHandler):
    """Sample event handler for user-related events."""
    
    def __init__(self):
        self.logger = get_logger(__name__)
    
    def handle_user_registered(self, event):
        """Handle user registration events."""
        user_data = event.data
        self.logger.info(f"Processing user registration for user {user_data.get('user_id')}")
        
        # Simulate sending welcome email
        print(f"📧 Sending welcome email to {user_data.get('email')}")
        
        # Log audit event
        audit = get_audit_logger()
        audit.log_event(
            event_type=AuditEventType.USER_ACCOUNT_CREATED,
            user_id=user_data.get('user_id'),
            description=f"Welcome email sent to {user_data.get('email')}",
            details={"email_sent": True, "template": "welcome"}
        )
    
    def handle_user_login(self, event):
        """Handle user login events."""
        login_data = event.data
        self.logger.info(f"Processing login for user {login_data.get('user_id')}")
        
        # Update user's last login cache
        cache = get_cache_manager()
        cache.set(
            f"user:{login_data.get('user_id')}:last_login",
            datetime.now().isoformat(),
            ttl=86400  # 24 hours
        )


def setup_environment_variables():
    """Set up minimal environment variables for demo purposes."""
    print("🔧 Setting up demo environment variables...")
    
    # Only set if not already present
    env_vars = {
        "DB_HOST": "localhost",
        "DB_PORT": "5432", 
        "DB_NAME": "happypath_demo",
        "DB_USER": "demo_user",
        "DB_PASSWORD": "demo_password",
        "SECRET_KEY": "demo-secret-key-for-testing-only",
        "JWT_SECRET": "demo-jwt-secret-for-testing-only",
        "ENCRYPTION_KEY": "demo-encryption-key-32-bytes-long!",
        "REDIS_HOST": "localhost",
        "REDIS_PORT": "6379",
        "ENVIRONMENT": "development",
        "LOG_LEVEL": "INFO"
    }
    
    for key, value in env_vars.items():
        if not os.getenv(key):
            os.environ[key] = value
    
    print("✅ Environment variables configured for demo")


def demonstrate_configuration():
    """Demonstrate configuration management."""
    print("\n" + "="*60)
    print("📋 CONFIGURATION MANAGEMENT DEMO")
    print("="*60)
    
    # Initialize configuration
    config = initialize_config()
    print(f"✅ Configuration initialized for {config.env.value} environment")
    
    # Access various configuration sections
    print(f"📊 Database configuration:")
    print(f"  Host: {config.database.host}")
    print(f"  Port: {config.database.port}")
    print(f"  Database: {config.database.name}")
    
    print(f"🔐 Security configuration:")
    print(f"  JWT Expiry: {config.security.jwt_expiry_hours} hours")
    print(f"  Password Min Length: {config.security.password_min_length}")
    
    print(f"🗃️ Cache configuration:")
    print(f"  Redis Host: {config.cache.host}")
    print(f"  Redis Port: {config.cache.port}")
    
    # Feature flags
    print(f"🚩 Feature flags:")
    print(f"  Audit Logging: {config.features.enable_audit_logging}")
    print(f"  Metrics Collection: {config.features.enable_metrics_collection}")
    print(f"  Rate Limiting: {config.features.enable_rate_limiting}")


def demonstrate_logging():
    """Demonstrate structured logging."""
    print("\n" + "="*60)
    print("📝 STRUCTURED LOGGING DEMO")
    print("="*60)
    
    # Setup logging
    setup_logging()
    logger = get_logger(__name__)
    
    print("✅ Logging system initialized")
    
    # Different log levels with structured data
    logger.info("Application started", extra={
        "component": "sample_app",
        "version": "1.0.0",
        "startup_time": datetime.now().isoformat()
    })
    
    logger.debug("Processing user request", extra={
        "user_id": 12345,
        "endpoint": "/api/users/profile",
        "request_id": "req_abc123"
    })
    
    logger.warning("Rate limit approaching", extra={
        "user_id": 12345,
        "current_requests": 95,
        "limit": 100,
        "window_minutes": 15
    })
    
    # Simulate an error
    try:
        raise ValueError("Sample error for demonstration")
    except Exception as e:
        logger.error("Sample error occurred", extra={
            "error_type": type(e).__name__,
            "error_message": str(e),
            "user_id": 12345
        })
    
    print("📋 Check your logs to see structured JSON output")


def demonstrate_security():
    """Demonstrate security features."""
    print("\n" + "="*60)
    print("🔐 SECURITY FEATURES DEMO")
    print("="*60)
    
    security = get_security_manager()
    
    # Password hashing
    print("🔒 Password Security:")
    password = "MySecurePassword123!"
    hashed = security.hash_password(password)
    is_valid = security.verify_password(password, hashed)
    print(f"  Password hashed: {hashed[:50]}...")
    print(f"  Verification: {'✅ Valid' if is_valid else '❌ Invalid'}")
    
    # JWT tokens
    print("\n🎫 JWT Token Management:")
    user_id = 12345
    roles = ["user", "premium"]
    token = security.create_access_token(user_id=user_id, roles=roles)
    print(f"  Token created: {token[:50]}...")
    
    # Verify token
    try:
        payload = security.verify_access_token(token)
        print(f"  Token verified: User ID {payload.get('user_id')}, Roles: {payload.get('roles')}")
    except SecurityError as e:
        print(f"  Token verification failed: {e}")
    
    # Data encryption
    print("\n🔒 Data Encryption:")
    sensitive_data = "Social Security Number: 123-45-6789"
    encrypted = security.encrypt_data(sensitive_data)
    decrypted = security.decrypt_data(encrypted)
    print(f"  Original: {sensitive_data}")
    print(f"  Encrypted: {encrypted}")
    print(f"  Decrypted: {decrypted}")
    print(f"  Match: {'✅ Yes' if sensitive_data == decrypted else '❌ No'}")
    
    # Permission checking
    print("\n👮 Permission System:")
    user_roles = ["user", "premium"]
    permissions_to_check = [
        "user:read",
        "user:write", 
        "admin:read",
        "premium:features"
    ]
    
    for permission in permissions_to_check:
        has_permission = security.check_permission(user_roles, permission)
        status = "✅ Allowed" if has_permission else "❌ Denied"
        print(f"  {permission}: {status}")


def demonstrate_database():
    """Demonstrate database operations."""
    print("\n" + "="*60)
    print("🗄️ DATABASE OPERATIONS DEMO")
    print("="*60)
    
    try:
        db = get_db_manager()
        
        # Health check
        health = db.get_health_status()
        print(f"Database Status: {health.get('status', 'unknown').upper()}")
        
        if health.get('status') == 'healthy':
            print(f"  Database: {health.get('database_name')}")
            print(f"  Active Connections: {health.get('active_connections')}")
            print(f"  Tables: {health.get('table_count')}")
        
        # Query builder demonstration
        print("\n📊 Query Builder Demo:")
        query_builder = db.query_builder()
        
        # Build a sample query
        query = (query_builder
                .select("id, email, created_at")
                .from_table("users")
                .where("active = %s", True)
                .where("created_at > %s", datetime.now() - timedelta(days=30))
                .order_by("created_at DESC")
                .limit(10))
        
        print(f"  Built query: {query.query}")
        print(f"  Parameters: {query.params}")
        
        # Note: We won't execute since demo database might not exist
        print("  (Query built successfully - execution skipped for demo)")
        
    except Exception as e:
        print(f"⚠️ Database connection failed (expected in demo): {e}")
        print("  This is normal if you haven't set up a database yet")


def demonstrate_caching():
    """Demonstrate Redis caching."""
    print("\n" + "="*60)
    print("🗃️ CACHING SYSTEM DEMO")
    print("="*60)
    
    try:
        cache = get_cache_manager()
        
        # Health check
        health = cache.get_health_status()
        print(f"Cache Status: {health.get('status', 'unknown').upper()}")
        
        if health.get('status') == 'healthy':
            print(f"  Response Time: {health.get('response_time_ms', 0):.2f}ms")
            
            # Basic caching operations
            print("\n📦 Basic Cache Operations:")
            
            # Set values
            cache.set("demo:user:12345", {"name": "John Doe", "email": "john@example.com"}, ttl=300)
            cache.set("demo:counter", 42, ttl=60)
            cache.set("demo:settings", {"theme": "dark", "notifications": True}, ttl=3600)
            
            # Get values
            user_data = cache.get("demo:user:12345")
            counter = cache.get("demo:counter")
            settings = cache.get("demo:settings")
            
            print(f"  User data: {user_data}")
            print(f"  Counter: {counter}")
            print(f"  Settings: {settings}")
            
            # Session management
            print("\n👤 Session Management:")
            session_id = cache.create_session(
                user_id=12345,
                data={"role": "premium", "login_time": datetime.now().isoformat()}
            )
            print(f"  Session created: {session_id}")
            
            session_data = cache.get_session(session_id)
            print(f"  Session data: {session_data}")
            
            # Cleanup demo data
            cache.delete("demo:user:12345")
            cache.delete("demo:counter")
            cache.delete("demo:settings")
            cache.invalidate_session(session_id)
            print("  Demo cache data cleaned up")
            
    except Exception as e:
        print(f"⚠️ Cache connection failed (expected in demo): {e}")
        print("  This is normal if you haven't set up Redis yet")


def demonstrate_audit_logging():
    """Demonstrate audit logging system."""
    print("\n" + "="*60)
    print("📊 AUDIT LOGGING DEMO")
    print("="*60)
    
    audit = get_audit_logger()
    
    # Log various types of events
    print("📝 Logging audit events...")
    
    # User authentication events
    login_event_id = audit.log_event(
        event_type=AuditEventType.USER_LOGIN_SUCCESS,
        user_id=12345,
        description="User logged in successfully",
        severity=AuditSeverity.LOW,
        details={
            "ip_address": "192.168.1.100",
            "user_agent": "Mozilla/5.0 (Demo Browser)",
            "login_method": "password"
        }
    )
    print(f"  ✅ Login event logged: {login_event_id}")
    
    # Data access events
    data_access_event_id = audit.log_event(
        event_type=AuditEventType.DATA_ACCESS,
        user_id=12345,
        description="User accessed patient records",
        severity=AuditSeverity.MEDIUM,
        details={
            "resource_type": "patient_records",
            "record_count": 5,
            "access_reason": "treatment_review"
        }
    )
    print(f"  ✅ Data access event logged: {data_access_event_id}")
    
    # Administrative events
    admin_event_id = audit.log_event(
        event_type=AuditEventType.ADMIN_SYSTEM_CONFIG_CHANGE,
        user_id=1,
        description="System configuration updated",
        severity=AuditSeverity.HIGH,
        details={
            "config_section": "security_settings",
            "changes": ["jwt_expiry_hours", "rate_limit_window"],
            "previous_values": {"jwt_expiry_hours": 24, "rate_limit_window": 3600}
        }
    )
    print(f"  ✅ Admin event logged: {admin_event_id}")
    
    # Security monitoring
    print("\n🛡️ Security event monitoring:")
    audit.log_security_event(
        event="SUSPICIOUS_LOGIN_ATTEMPT",
        user_id=12345,
        success=False,
        ip_address="203.0.113.1",
        details={
            "reason": "multiple_failed_attempts",
            "attempt_count": 5,
            "time_window": "5_minutes"
        }
    )
    print("  ✅ Security event logged")
    
    # GDPR compliance tracking
    gdpr_event_id = audit.log_gdpr_event(
        event_type="DATA_EXPORT_REQUEST",
        user_id=12345,
        description="User requested data export",
        data_types=["profile", "activity_logs", "preferences"],
        legal_basis="user_consent"
    )
    print(f"  ✅ GDPR event logged: {gdpr_event_id}")


def demonstrate_event_system():
    """Demonstrate event-driven architecture."""
    print("\n" + "="*60)
    print("📡 EVENT SYSTEM DEMO")
    print("="*60)
    
    events = get_event_manager()
    
    # Register event handler
    handler = SampleUserEventHandler()
    events.register_handler(handler)
    print("✅ Event handler registered")
    
    # Publish events
    print("\n📤 Publishing events:")
    
    # User registration event
    registration_event_id = events.publish(
        event_type=EventType.USER_REGISTERED,
        data={
            "user_id": 12345,
            "email": "john.doe@example.com",
            "registration_date": datetime.now().isoformat(),
            "plan": "premium"
        },
        source="user_service"
    )
    print(f"  ✅ User registration event published: {registration_event_id}")
    
    # User login event
    login_event_id = events.publish(
        event_type=EventType.USER_LOGIN,
        data={
            "user_id": 12345,
            "login_time": datetime.now().isoformat(),
            "ip_address": "192.168.1.100"
        },
        source="auth_service"
    )
    print(f"  ✅ User login event published: {login_event_id}")
    
    # System events
    maintenance_event_id = events.publish(
        event_type=EventType.SYSTEM_MAINTENANCE_START,
        data={
            "maintenance_type": "database_update",
            "estimated_duration": "30_minutes",
            "affected_services": ["api", "web_app"]
        },
        source="admin_service"
    )
    print(f"  ✅ Maintenance event published: {maintenance_event_id}")
    
    # Process events (this would normally run in background)
    print("\n📥 Processing events...")
    events.process_pending_events()
    print("  ✅ Events processed")


def demonstrate_monitoring():
    """Demonstrate monitoring and health checks."""
    print("\n" + "="*60)
    print("🏥 MONITORING & HEALTH CHECKS DEMO")
    print("="*60)
    
    # Health checks
    health_checker = get_health_checker()
    health_status = health_checker.get_overall_status()
    
    print(f"Overall System Status: {health_status['status'].upper()}")
    print(f"Message: {health_status['message']}")
    print(f"Timestamp: {health_status['timestamp']}")
    
    print("\n🔧 Individual Service Status:")
    for service, status in health_status['services'].items():
        status_emoji = "✅" if status['status'] == "healthy" else "⚠️" if status['status'] == "degraded" else "❌"
        print(f"  {status_emoji} {service}: {status['status']}")
        if status.get('response_time_ms'):
            print(f"    Response time: {status['response_time_ms']:.2f}ms")
        if status.get('message'):
            print(f"    Message: {status['message']}")
    
    # System metrics
    print("\n📈 System Metrics:")
    metrics_collector = get_metrics_collector()
    
    try:
        system_metrics = metrics_collector.collect_system_metrics()
        print(f"  CPU Usage: {system_metrics.cpu_percent:.1f}%")
        print(f"  Memory Usage: {system_metrics.memory_percent:.1f}%")
        print(f"  Memory Available: {system_metrics.memory_available_mb:.0f} MB")
        print(f"  Disk Usage: {system_metrics.disk_percent:.1f}%")
        print(f"  Disk Free: {system_metrics.disk_free_gb:.1f} GB")
        print(f"  System Uptime: {system_metrics.uptime_seconds:.0f} seconds")
    except Exception as e:
        print(f"  ⚠️ Could not collect system metrics: {e}")
    
    # Application metrics
    try:
        app_metrics = metrics_collector.collect_application_metrics()
        print(f"\n📊 Application Metrics:")
        print(f"  Total Requests: {app_metrics.get('total_requests', 'N/A')}")
        print(f"  Active Sessions: {app_metrics.get('active_sessions', 'N/A')}")
        print(f"  Cache Hit Rate: {app_metrics.get('cache_hit_rate', 'N/A')}")
        print(f"  Average Response Time: {app_metrics.get('avg_response_time_ms', 'N/A')}ms")
    except Exception as e:
        print(f"  ℹ️ Application metrics not available in demo mode")


def demonstrate_error_handling():
    """Demonstrate error handling system."""
    print("\n" + "="*60)
    print("🚨 ERROR HANDLING DEMO")
    print("="*60)
    
    logger = get_logger(__name__)
    
    # Custom exception hierarchy
    print("📋 Custom Exception Hierarchy:")
    
    try:
        # Simulate a security error
        raise SecurityError("Invalid authentication token", error_code="AUTH_001")
    except SecurityError as e:
        logger.error("Security error caught", extra={
            "error_type": "SecurityError",
            "error_code": e.error_code,
            "error_message": str(e)
        })
        print(f"  ✅ SecurityError handled: {e}")
    
    try:
        # Simulate a general application error
        raise HappyPathError("Something went wrong in the application")
    except HappyPathError as e:
        logger.error("Application error caught", extra={
            "error_type": "HappyPathError",
            "error_message": str(e)
        })
        print(f"  ✅ HappyPathError handled: {e}")
    
    print("📝 Error handling logged with structured data")


async def demonstrate_async_operations():
    """Demonstrate asynchronous operations."""
    print("\n" + "="*60)
    print("⚡ ASYNC OPERATIONS DEMO")
    print("="*60)
    
    logger = get_logger(__name__)
    
    # Simulate async database operations
    print("🗄️ Simulating async database operations...")
    
    async def fetch_user_data(user_id):
        """Simulate async user data fetch."""
        await asyncio.sleep(0.1)  # Simulate I/O delay
        return {
            "id": user_id,
            "name": f"User {user_id}",
            "email": f"user{user_id}@example.com"
        }
    
    async def process_multiple_users():
        """Process multiple users concurrently."""
        user_ids = [1, 2, 3, 4, 5]
        
        # Process users concurrently
        tasks = [fetch_user_data(user_id) for user_id in user_ids]
        results = await asyncio.gather(*tasks)
        
        for user_data in results:
            logger.info("Processed user data", extra={
                "user_id": user_data["id"],
                "operation": "async_fetch"
            })
            print(f"  ✅ Processed user {user_data['id']}: {user_data['name']}")
    
    await process_multiple_users()
    
    # Simulate async event processing
    print("\n📡 Simulating async event processing...")
    events = get_event_manager()
    
    # In a real application, this would run in background
    await asyncio.sleep(0.1)  # Simulate processing time
    print("  ✅ Async event processing completed")


def main():
    """Main demo function."""
    print("🎯 Happy Path Core Infrastructure Demo")
    print("=" * 60)
    print("This demo showcases all components of the core infrastructure.")
    print("Some operations may show warnings if external services (DB, Redis) aren't running.")
    print("This is expected and demonstrates graceful error handling.")
    print()
    
    # Setup
    setup_environment_variables()
    
    # Run all demonstrations
    demonstrate_configuration()
    demonstrate_logging()
    demonstrate_security()
    demonstrate_database()
    demonstrate_caching()
    demonstrate_audit_logging()
    demonstrate_event_system()
    demonstrate_monitoring()
    demonstrate_error_handling()
    
    # Async demo
    print("\n⚡ Running async operations demo...")
    asyncio.run(demonstrate_async_operations())
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 DEMO COMPLETED SUCCESSFULLY!")
    print("="*60)
    print("✅ All core infrastructure components demonstrated")
    print("📖 Check the logs to see structured JSON output")
    print("🔧 Customize the configuration and try with real services")
    print("\nNext steps:")
    print("  1. Set up PostgreSQL database")
    print("  2. Set up Redis cache")
    print("  3. Configure environment variables for production")
    print("  4. Run the setup script: python happypath/core/setup.py")
    print("  5. Build your application using these core components")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        sys.exit(1)
