"""
Setup script for initializing the Happy Path core infrastructure.
Run this to initialize all core components and verify they work correctly.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from happypath.core import (
    get_config, initialize_config, Environment,
    setup_logging, get_logger,
    get_db_manager,
    get_cache_manager,
    get_health_checker,
    get_metrics_collector,
    get_audit_logger,
    get_security_manager,
    get_event_manager
)


def print_banner():
    """Print setup banner."""
    print("=" * 60)
    print("🎯 Happy Path Core Infrastructure Setup")
    print("=" * 60)
    print()


def check_environment():
    """Check if required environment variables are set."""
    print("📋 Checking environment configuration...")
    
    required_vars = {
        "DB_HOST": "Database host",
        "DB_NAME": "Database name",
        "DB_USER": "Database username",
        "DB_PASSWORD": "Database password",
        "SECRET_KEY": "Application secret key",
        "JWT_SECRET": "JWT secret key",
        "ENCRYPTION_KEY": "Data encryption key"
    }
    
    missing_vars = []
    for var, description in required_vars.items():
        if not os.getenv(var):
            missing_vars.append(f"  - {var}: {description}")
    
    if missing_vars:
        print("❌ Missing required environment variables:")
        print("\n".join(missing_vars))
        print("\nPlease set these environment variables before running setup.")
        return False
    
    print("✅ Environment configuration looks good!")
    return True


def setup_configuration():
    """Initialize configuration."""
    print("\n⚙️ Initializing configuration...")
    
    try:
        config = initialize_config()
        print(f"✅ Configuration initialized for {config.env.value} environment")
        
        # Print configuration summary (without sensitive data)
        config_summary = config.to_dict()
        print("\n📋 Configuration Summary:")
        for section, settings in config_summary.items():
            if isinstance(settings, dict):
                print(f"  {section}:")
                for key, value in settings.items():
                    print(f"    {key}: {value}")
            else:
                print(f"  {section}: {settings}")
        
        return config
    except Exception as e:
        print(f"❌ Configuration initialization failed: {e}")
        return None


def setup_logging_system():
    """Initialize logging system."""
    print("\n📝 Setting up logging system...")
    
    try:
        setup_logging()
        logger = get_logger(__name__)
        logger.info("Logging system initialized successfully")
        print("✅ Logging system configured")
        return logger
    except Exception as e:
        print(f"❌ Logging setup failed: {e}")
        return None


def test_database_connection():
    """Test database connectivity."""
    print("\n🗄️ Testing database connection...")
    
    try:
        db_manager = get_db_manager()
        health_status = db_manager.get_health_status()
        
        if health_status.get("status") == "healthy":
            print("✅ Database connection successful")
            print(f"  Database: {health_status.get('database_name')}")
            print(f"  Tables: {health_status.get('table_count')}")
            print(f"  Active connections: {health_status.get('active_connections')}")
            return True
        else:
            print("❌ Database health check failed")
            print(f"  Error: {health_status.get('error')}")
            return False
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_cache_connection():
    """Test Redis cache connectivity."""
    print("\n🗃️ Testing cache connection...")
    
    try:
        cache_manager = get_cache_manager()
        health_status = cache_manager.get_health_status()
        
        if health_status.get("status") == "healthy":
            print("✅ Cache connection successful")
            print(f"  Response time: {health_status.get('response_time_ms', 0):.2f}ms")
            return True
        else:
            print("❌ Cache health check failed")
            print(f"  Error: {health_status.get('message')}")
            return False
    except Exception as e:
        print(f"❌ Cache connection failed: {e}")
        return False


def test_security_components():
    """Test security components."""
    print("\n🔐 Testing security components...")
    
    try:
        security_manager = get_security_manager()
        
        # Test password hashing
        test_password = "TestPassword123!"
        hashed = security_manager.hash_password(test_password)
        verified = security_manager.verify_password(test_password, hashed)
        
        if verified:
            print("✅ Password hashing works correctly")
        else:
            print("❌ Password hashing verification failed")
            return False
        
        # Test token generation
        token = security_manager.generate_secure_token()
        if len(token) > 0:
            print("✅ Token generation works correctly")
        else:
            print("❌ Token generation failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Security component test failed: {e}")
        return False


def test_audit_system():
    """Test audit logging system."""
    print("\n📊 Testing audit system...")
    
    try:
        from happypath.core.auditing import AuditEventType, AuditSeverity
        
        audit_logger = get_audit_logger()
        event_id = audit_logger.log_event(
            event_type=AuditEventType.ADMIN_SYSTEM_CONFIG_CHANGE,
            description="Core infrastructure setup test",
            severity=AuditSeverity.LOW,
            details={"test": True, "component": "setup_script"}
        )
        
        if event_id:
            print("✅ Audit logging works correctly")
            print(f"  Test audit event ID: {event_id}")
            return True
        else:
            print("❌ Audit logging failed")
            return False
    except Exception as e:
        print(f"❌ Audit system test failed: {e}")
        return False


def test_event_system():
    """Test event management system."""
    print("\n📡 Testing event system...")
    
    try:
        from happypath.core.events import EventType
        
        event_manager = get_event_manager()
        
        # Test synchronous event publishing
        event_id = event_manager.publish(
            event_type=EventType.SYSTEM_MAINTENANCE_START,
            data={"component": "setup_test", "test": True},
            source="setup_script"
        )
        
        if event_id:
            print("✅ Event system works correctly")
            print(f"  Test event ID: {event_id}")
            return True
        else:
            print("❌ Event system failed")
            return False
    except Exception as e:
        print(f"❌ Event system test failed: {e}")
        return False


def run_health_checks():
    """Run comprehensive health checks."""
    print("\n🏥 Running health checks...")
    
    try:
        health_checker = get_health_checker()
        health_status = health_checker.get_overall_status()
        
        print(f"Overall Status: {health_status['status'].upper()}")
        print(f"Message: {health_status['message']}")
        
        print("\nService Status:")
        for service, status in health_status['services'].items():
            status_emoji = "✅" if status['status'] == "healthy" else "⚠️" if status['status'] == "degraded" else "❌"
            print(f"  {status_emoji} {service}: {status['status']}")
            if status.get('response_time_ms'):
                print(f"    Response time: {status['response_time_ms']:.2f}ms")
        
        return health_status['status'] in ['healthy', 'degraded']
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False


def display_metrics():
    """Display system metrics."""
    print("\n📈 System metrics:")
    
    try:
        metrics_collector = get_metrics_collector()
        system_metrics = metrics_collector.collect_system_metrics()
        
        print(f"  CPU Usage: {system_metrics.cpu_percent:.1f}%")
        print(f"  Memory Usage: {system_metrics.memory_percent:.1f}%")
        print(f"  Memory Available: {system_metrics.memory_available_mb:.0f} MB")
        print(f"  Disk Usage: {system_metrics.disk_percent:.1f}%")
        print(f"  Disk Free: {system_metrics.disk_free_gb:.1f} GB")
        print(f"  Uptime: {system_metrics.uptime_seconds:.0f} seconds")
        
    except Exception as e:
        print(f"❌ Metrics collection failed: {e}")


def main():
    """Main setup function."""
    print_banner()
    
    # Step 1: Check environment
    if not check_environment():
        sys.exit(1)
    
    # Step 2: Initialize configuration
    config = setup_configuration()
    if not config:
        sys.exit(1)
    
    # Step 3: Setup logging
    logger = setup_logging_system()
    if not logger:
        sys.exit(1)
    
    # Step 4: Test database
    if not test_database_connection():
        print("\n⚠️ Database connection failed. Please check your database configuration.")
        print("You can continue with other components, but database-dependent features won't work.")
    
    # Step 5: Test cache
    if not test_cache_connection():
        print("\n⚠️ Cache connection failed. Please check your Redis configuration.")
        print("You can continue without cache, but performance may be affected.")
    
    # Step 6: Test security
    if not test_security_components():
        print("\n❌ Security components failed. This is critical - setup cannot continue.")
        sys.exit(1)
    
    # Step 7: Test audit system
    if not test_audit_system():
        print("\n⚠️ Audit system failed. Compliance features may not work correctly.")
    
    # Step 8: Test event system
    if not test_event_system():
        print("\n⚠️ Event system failed. Real-time features may not work correctly.")
    
    # Step 9: Run health checks
    if not run_health_checks():
        print("\n⚠️ Some health checks failed. Please review the issues above.")
    
    # Step 10: Display metrics
    display_metrics()
    
    print("\n" + "=" * 60)
    print("🎉 Happy Path Core Infrastructure Setup Complete!")
    print("=" * 60)
    print("\n✅ Core infrastructure is ready for use.")
    print("\n📚 Next steps:")
    print("  1. Review any warnings or errors above")
    print("  2. Set up your application-specific components")
    print("  3. Configure monitoring and alerting")
    print("  4. Run database migrations if needed")
    print("  5. Start your application services")
    print("\n📖 Documentation: See backend/docs/core.md for detailed guides")
    print("🔧 Configuration: See backend/happypath/core/config.py for all settings")


if __name__ == "__main__":
    main()
