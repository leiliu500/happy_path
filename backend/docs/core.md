# Happy Path Core Infrastructure

The Happy Path core infrastructure provides enterprise-grade backend services for the mental health wellness platform. This comprehensive system includes database management, security, monitoring, caching, audit logging, and event handling.

## 🏗️ Architecture Overview

The core infrastructure consists of 8 specialized modules:

```
backend/happypath/core/
├── __init__.py           # Main module interface
├── config.py             # Configuration management
├── database.py           # PostgreSQL utilities
├── security.py           # Authentication & encryption
├── monitoring.py         # Health checks & metrics
├── auditing.py          # Audit logging & compliance
├── cache.py             # Redis caching layer
├── events.py            # Event-driven architecture
├── logging.py           # Structured logging
├── exceptions.py        # Error handling
└── setup.py            # Infrastructure setup script
```

Requirements and documentation are located at:
```
backend/
├── requirements.txt     # Python dependencies
└── docs/
    └── core.md         # Core infrastructure documentation
```

## 🚀 Quick Start

### 1. Environment Setup

First, set up your environment variables:

```bash
# Database Configuration
export DB_HOST="localhost"
export DB_PORT="5432"
export DB_NAME="happypath_db"
export DB_USER="your_db_user"
export DB_PASSWORD="your_db_password"

# Security Configuration
export SECRET_KEY="your-super-secret-key-here"
export JWT_SECRET="your-jwt-secret-key"
export ENCRYPTION_KEY="your-32-byte-encryption-key"

# Redis Configuration (optional)
export REDIS_HOST="localhost"
export REDIS_PORT="6379"
export REDIS_PASSWORD=""

# Environment
export ENVIRONMENT="development"  # or "production", "staging"
```

### 2. Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Run Setup Script

```bash
cd backend
python happypath/core/setup.py
```

This will test all components and verify your configuration.

## 📖 Core Components

### Configuration Management (`config.py`)

Centralized configuration with environment-based settings:

```python
from happypath.core import get_config, initialize_config

# Initialize configuration
config = initialize_config()

# Access configuration
print(f"Database host: {config.database.host}")
print(f"Environment: {config.env}")
```

### Database Management (`database.py`)

PostgreSQL connection pooling and query utilities:

```python
from happypath.core import get_db_manager

# Get database manager
db = get_db_manager()

# Execute queries
result = db.execute_query("SELECT * FROM users WHERE id = %s", (user_id,))

# Use query builder
query = db.query_builder().select("*").from_table("users").where("active = %s", True)
users = query.execute()

# Health check
health = db.get_health_status()
```

### Security Framework (`security.py`)

Comprehensive security with JWT, encryption, and role-based access:

```python
from happypath.core import get_security_manager

security = get_security_manager()

# Password management
hashed = security.hash_password("user_password")
is_valid = security.verify_password("user_password", hashed)

# JWT tokens
token = security.create_access_token(user_id=123, roles=["user"])
payload = security.verify_access_token(token)

# Encryption
encrypted = security.encrypt_data("sensitive_data")
decrypted = security.decrypt_data(encrypted)

# Permissions
has_permission = security.check_permission(user_roles, "user:read")
```

### Monitoring & Health Checks (`monitoring.py`)

System monitoring and performance metrics:

```python
from happypath.core import get_health_checker, get_metrics_collector

# Health checks
health = get_health_checker()
status = health.get_overall_status()

# Metrics collection
metrics = get_metrics_collector()
system_metrics = metrics.collect_system_metrics()
db_metrics = metrics.collect_database_metrics()
```

### Audit Logging (`auditing.py`)

Comprehensive audit trail and compliance tracking:

```python
from happypath.core import get_audit_logger
from happypath.core.auditing import AuditEventType, AuditSeverity

audit = get_audit_logger()

# Log events
event_id = audit.log_event(
    event_type=AuditEventType.USER_LOGIN_SUCCESS,
    user_id=123,
    description="User logged in successfully",
    details={"ip_address": "192.168.1.1"}
)

# Security monitoring
audit.log_security_event(
    event="LOGIN_ATTEMPT",
    user_id=123,
    success=True,
    ip_address="192.168.1.1"
)
```

### Redis Caching (`cache.py`)

High-performance caching with decorators:

```python
from happypath.core import get_cache_manager

cache = get_cache_manager()

# Basic caching
cache.set("user:123", user_data, ttl=3600)
user_data = cache.get("user:123")

# Cache decorator
@cache.cached(ttl=3600, key_prefix="user")
def get_user(user_id):
    return fetch_user_from_db(user_id)

# Session management
session_id = cache.create_session(user_id=123, data={"role": "user"})
session_data = cache.get_session(session_id)
```

### Event System (`events.py`)

Event-driven architecture with pub/sub:

```python
from happypath.core import get_event_manager
from happypath.core.events import EventType

events = get_event_manager()

# Publish events
event_id = events.publish(
    event_type=EventType.USER_REGISTERED,
    data={"user_id": 123, "email": "user@example.com"},
    source="user_service"
)

# Event handlers
class UserEventHandler(EventHandler):
    def handle_user_registered(self, event):
        # Send welcome email
        send_welcome_email(event.data["email"])

events.register_handler(UserEventHandler())
```

### Structured Logging (`logging.py`)

JSON-formatted logging with security filtering:

```python
from happypath.core import get_logger, setup_logging

# Setup logging (usually done once at startup)
setup_logging()

# Get logger
logger = get_logger(__name__)

# Log messages
logger.info("User operation completed", extra={
    "user_id": 123,
    "operation": "profile_update",
    "duration_ms": 45
})

logger.error("Database connection failed", extra={
    "error": str(exception),
    "retry_count": 3
})
```

## 🔧 Configuration Options

The system supports extensive configuration through environment variables:

### Database Settings
- `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`
- `DB_POOL_MIN_SIZE`, `DB_POOL_MAX_SIZE`
- `DB_TIMEOUT`, `DB_SSL_MODE`

### Security Settings
- `SECRET_KEY`, `JWT_SECRET`, `ENCRYPTION_KEY`
- `JWT_EXPIRY_HOURS`, `PASSWORD_MIN_LENGTH`
- `RATE_LIMIT_REQUESTS`, `RATE_LIMIT_WINDOW`

### Redis Settings
- `REDIS_HOST`, `REDIS_PORT`, `REDIS_PASSWORD`
- `REDIS_DB`, `REDIS_TIMEOUT`

### Feature Flags
- `ENABLE_AUDIT_LOGGING`, `ENABLE_METRICS_COLLECTION`
- `ENABLE_RATE_LIMITING`, `ENABLE_CACHING`

## 🛡️ Security Features

- **JWT Authentication**: Secure token-based authentication
- **Password Security**: Bcrypt hashing with configurable rounds
- **Data Encryption**: Fernet encryption for sensitive data
- **Role-based Access**: Granular permission system
- **Rate Limiting**: Protection against abuse
- **Audit Logging**: Complete security event tracking
- **Input Validation**: Built-in sanitization and validation

## 📊 Monitoring & Observability

- **Health Checks**: Comprehensive system health monitoring
- **Performance Metrics**: CPU, memory, disk, and database metrics
- **Audit Trail**: Complete audit logging for compliance
- **Error Tracking**: Structured error logging and reporting
- **Event Monitoring**: Real-time event tracking and notifications

## 🔄 Event-Driven Architecture

The event system supports:
- Synchronous and asynchronous event processing
- Event handlers with automatic registration
- Built-in event types for common operations
- Integration with audit logging
- Notification system for critical events

## 🏥 Health Monitoring

Built-in health checks for:
- Database connectivity and performance
- Redis cache availability
- System resources (CPU, memory, disk)
- Application components
- External service dependencies

## 📋 Compliance & Auditing

- **GDPR Compliance**: Data processing and retention tracking
- **HIPAA Support**: Healthcare data audit requirements
- **SOC 2**: Security and availability controls
- **Audit Reports**: Automated compliance reporting
- **Data Retention**: Configurable retention policies

## 🚨 Error Handling

Hierarchical exception system:
- `HappyPathError`: Base application error
- `DatabaseError`: Database-related errors
- `SecurityError`: Security and authentication errors
- `ConfigurationError`: Configuration issues
- `CacheError`: Redis cache errors
- `AuditError`: Audit logging errors

## 🔧 Development & Testing

### Running Tests
```bash
# Run setup script to test all components
python happypath/core/setup.py

# Check health status
from happypath.core import get_health_checker
health = get_health_checker()
print(health.get_overall_status())
```

### Environment Configuration
```bash
# Development
export ENVIRONMENT="development"
export LOG_LEVEL="DEBUG"

# Production
export ENVIRONMENT="production"
export LOG_LEVEL="INFO"
```

## 📚 Integration Examples

### Web Application Integration
```python
from flask import Flask
from happypath.core import initialize_config, setup_logging, get_db_manager

app = Flask(__name__)

# Initialize core infrastructure
config = initialize_config()
setup_logging()
db = get_db_manager()

@app.route("/health")
def health_check():
    health = get_health_checker()
    return health.get_overall_status()
```

### Background Service Integration
```python
import asyncio
from happypath.core import get_event_manager, get_audit_logger

async def background_worker():
    events = get_event_manager()
    audit = get_audit_logger()
    
    # Process events
    await events.process_pending_events()
    
    # Log activity
    audit.log_event(
        event_type=AuditEventType.SYSTEM_BACKGROUND_TASK,
        description="Background worker completed"
    )

if __name__ == "__main__":
    asyncio.run(background_worker())
```

## 📞 Support & Documentation

- **Setup Issues**: Run `python happypath/core/setup.py` for diagnostic information
- **Configuration**: All settings documented in `config.py`
- **Security**: Review `security.py` for authentication and encryption
- **Monitoring**: Use `monitoring.py` for health checks and metrics
- **Compliance**: Check `auditing.py` for audit requirements

The Happy Path core infrastructure provides a robust, secure, and scalable foundation for building mental health wellness applications with enterprise-grade requirements.
