# Repository Pattern Documentation

## Overview

The repository pattern implementation provides a clean data access layer for the Happy Path mental health wellness platform. It separates business logic from data access concerns and provides a consistent interface for database operations.

## Architecture

### Base Repository Classes

#### BaseRepository
Generic synchronous repository with common CRUD operations:
- `create(entity)` - Create new entity
- `get_by_id(id)` - Retrieve entity by ID
- `update(entity)` - Update existing entity  
- `delete(id)` - Delete entity by ID
- `list_all(options)` - List entities with filtering/pagination
- `exists(id)` - Check entity existence
- `count(filters)` - Count entities with optional filters

#### AsyncBaseRepository
Asynchronous version with `async/await` support for better performance in async applications.

### Query System

#### QueryOptions
Configurable query parameters:
```python
QueryOptions(
    limit=50,                    # Limit results
    offset=0,                    # Pagination offset
    order_by=['name', '-date'],  # Sorting (- prefix for DESC)
    filters={'active': True},    # WHERE conditions
    include_count=True,          # Include total count
    for_update=False            # SELECT FOR UPDATE
)
```

#### QueryResult
Structured query response:
```python
QueryResult(
    data=[...],          # List of entities
    total_count=100,     # Total count (if requested)
    page=2,             # Current page
    page_size=50,       # Page size
    has_next=True,      # Has next page
    has_previous=True   # Has previous page
)
```

## Specialized Repositories

### UserRepository
Manages user accounts and profiles:

**Key Features:**
- Password hashing with bcrypt
- User authentication and session management
- Profile management with medical information
- User search and filtering
- Account activation/deactivation

**Usage Example:**
```python
# Create user with hashed password
user = user_repo.create_user(
    email="user@example.com",
    username="username",
    password="secure_password",
    first_name="John",
    last_name="Doe"
)

# Authenticate user
auth_user = user_repo.authenticate_user("user@example.com", "secure_password")

# Create profile
profile = user_repo.create_profile(user.id, {
    "bio": "Mental health advocate",
    "emergency_contact_name": "Jane Doe",
    "emergency_contact_phone": "+1-555-0123"
})
```

### AuditRepository
Comprehensive audit logging and compliance:

**Key Features:**
- Structured audit event logging
- Compliance categorization with retention periods
- Security event tracking
- Audit trail queries and analytics
- Data export capabilities

**Usage Example:**
```python
# Log user action
audit_repo.log_user_action(
    user_id=123,
    action=AuditAction.UPDATE.value,
    resource_type="profile",
    resource_id="123",
    details={"section": "personal_info"}
)

# Log security event
audit_repo.log_security_event(
    action="failed_login",
    user_id=123,
    ip_address="192.168.1.100",
    success=False
)

# Generate audit summary
summary = audit_repo.generate_audit_summary(
    start_time=datetime.utcnow() - timedelta(days=30),
    end_time=datetime.utcnow()
)
```

### SessionRepository
User session management with security features:

**Key Features:**
- Session creation with device fingerprinting
- Risk scoring for suspicious activities
- Session validation and cleanup
- Geographic tracking
- Multiple device support

**Usage Example:**
```python
# Create session
session = session_repo.create_session(
    user_id=user.id,
    ip_address="192.168.1.100",
    user_agent="Mozilla/5.0...",
    device_info={"os": "macOS", "browser": "Chrome"},
    location={"country": "US", "state": "CA"}
)

# Validate session
valid_session = session_repo.validate_session(session.token)

# Terminate session
session_repo.terminate_session(session.id, "user_logout")
```

### SubscriptionRepository
Subscription and billing management:

**Key Features:**
- Plan management with features and limits
- Trial period handling
- Billing cycle automation
- Subscription upgrades/downgrades
- Payment tracking

**Usage Example:**
```python
# Create subscription plan
plan = SubscriptionPlan(
    name="Premium Plan",
    price=Decimal('19.99'),
    billing_cycle=BillingCycle.MONTHLY.value,
    features=["unlimited_journaling", "ai_therapy"],
    trial_days=14
)

# Create user subscription
subscription = subscription_repo.create_subscription(
    user_id=user.id,
    plan_id=plan.id,
    start_trial=True
)

# Upgrade subscription
upgraded = subscription_repo.upgrade_subscription(
    subscription.id,
    new_plan_id=premium_plan.id,
    prorate=True
)
```

## Error Handling

### Repository Exceptions
- `RepositoryError` - Base repository exception
- `ValidationError` - Entity validation failed
- `NotFoundError` - Entity not found
- `DuplicateError` - Duplicate entity creation

### Validation
Each repository validates entities before database operations:
```python
def _validate_entity(self, entity, is_update=False):
    if not entity.email:
        raise ValidationError("Email is required")
    
    if not is_update:
        existing = self.find_one_by(email=entity.email)
        if existing:
            raise DuplicateError("Email already exists")
```

## Transaction Support

Repositories support database transactions for data consistency:
```python
# Bulk operations with transaction
with db_manager.transaction():
    for entity in entities:
        repo.create(entity)
```

## Testing

### Unit Testing
Repositories are designed for easy testing with dependency injection:
```python
def test_user_creation():
    mock_db = Mock()
    mock_db.execute_query.return_value = [created_row]
    
    repo = UserRepository(mock_db, mock_logger)
    user = repo.create_user("test@example.com", "testuser", "password")
    
    assert user.email == "test@example.com"
```

### Integration Testing
Test with actual database connections:
```python
def test_user_repository_integration():
    db_manager = get_test_db_manager()
    repo = UserRepository(db_manager)
    
    user = repo.create_user("test@example.com", "testuser", "password")
    retrieved = repo.get_by_id(user.id)
    
    assert retrieved.email == user.email
```

## Performance Considerations

### Connection Pooling
- Database connections are pooled for efficiency
- Repository instances reuse connections

### Query Optimization
- Pagination limits large result sets
- Indexes should be created on frequently queried columns
- Use `QueryOptions.for_update` for row-level locking

### Caching
- Consider caching frequently accessed entities
- Implement cache invalidation on updates

## Security Features

### Data Protection
- Passwords are hashed with bcrypt
- Sensitive audit data is marked for special handling
- Session tokens are cryptographically secure

### Access Control
- Repository methods can be wrapped with authorization checks
- Audit logging tracks all data access

### Compliance
- Configurable data retention periods
- Audit trails for regulatory compliance
- Data export capabilities for GDPR requests

## Best Practices

### Repository Design
1. Keep repositories focused on single entities
2. Use factory functions for repository creation
3. Implement proper validation in `_validate_entity`
4. Handle database errors gracefully

### Entity Design
1. Use dataclasses for entity definitions
2. Implement helper methods for business logic
3. Keep entities immutable where possible
4. Use type hints for better IDE support

### Error Handling
1. Use specific exception types for different error conditions
2. Log errors with appropriate detail levels
3. Don't expose database implementation details

### Testing
1. Mock database dependencies for unit tests
2. Test both success and failure scenarios
3. Verify database calls and parameters
4. Use integration tests for complex queries

## Future Enhancements

### Planned Features
- Read replicas support for query scaling
- Event sourcing integration
- Advanced caching strategies
- Multi-tenant support
- Database migration tools

### Performance Optimizations
- Query result caching
- Lazy loading for relationships
- Bulk operation optimizations
- Connection pooling improvements
