"""
Repository Pattern Sample Code

This file demonstrates how to use the repository pattern implementation
for various database operations across different entities.
"""

import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
import logging

# Import core infrastructure
from backend.happypath.core import get_db_manager, get_logger

# Import repository classes
from backend.happypath.repository import (
    # Entities
    User, UserProfile, AuditEntry, Subscription, SubscriptionPlan, UserSession,
    
    # Repositories
    UserRepository, AuditRepository, SubscriptionRepository, 
    SubscriptionPlanRepository, SessionRepository,
    
    # Enums
    AuditAction, AuditLevel, SubscriptionStatus, BillingCycle,
    
    # Utilities
    QueryOptions,
    
    # Factory functions
    create_user_repository, create_audit_repository, 
    create_subscription_repository, create_session_repository
)


def setup_repositories():
    """Set up repository instances with database connection."""
    # Get database manager and logger
    db_manager = get_db_manager()
    logger = get_logger('repository_sample')
    
    # Create repository instances
    user_repo = create_user_repository(db_manager, logger)
    audit_repo = create_audit_repository(db_manager, logger)
    subscription_repo = create_subscription_repository(db_manager, logger)
    session_repo = create_session_repository(db_manager, logger)
    
    return user_repo, audit_repo, subscription_repo, session_repo


def demonstrate_user_operations():
    """Demonstrate user repository operations."""
    print("=== User Repository Operations ===")
    
    user_repo, audit_repo, _, _ = setup_repositories()
    
    try:
        # Create a new user
        print("Creating new user...")
        user = user_repo.create_user(
            email="john.doe@example.com",
            username="johndoe",
            password="secure_password123",
            first_name="John",
            last_name="Doe"
        )
        print(f"Created user: {user.id} - {user.email}")
        
        # Log the user creation
        audit_repo.log_user_action(
            user_id=user.id,
            action=AuditAction.CREATE.value,
            resource_type="user",
            resource_id=str(user.id),
            details={"email": user.email, "username": user.username}
        )
        
        # Authenticate user
        print("Authenticating user...")
        authenticated_user = user_repo.authenticate_user("john.doe@example.com", "secure_password123")
        if authenticated_user:
            print(f"Authentication successful: {authenticated_user.full_name()}")
        
        # Search users
        print("Searching users...")
        search_results = user_repo.search_users("john", limit=10)
        print(f"Found {len(search_results)} users matching 'john'")
        
        # Create user profile
        print("Creating user profile...")
        profile = user_repo.create_profile(user.id, {
            "bio": "Software developer passionate about mental health",
            "emergency_contact_name": "Jane Doe",
            "emergency_contact_phone": "+1-555-0123"
        })
        print(f"Created profile for user {user.id}")
        
        # Get user with profile
        user_profile = user_repo.get_profile(user.id)
        print(f"User profile bio: {user_profile.bio}")
        
        # Update user
        print("Updating user...")
        user.first_name = "Jonathan"
        updated_user = user_repo.update(user)
        print(f"Updated user name: {updated_user.full_name()}")
        
        return user
        
    except Exception as e:
        print(f"Error in user operations: {e}")
        return None


def demonstrate_subscription_operations(user: User):
    """Demonstrate subscription repository operations."""
    print("\n=== Subscription Repository Operations ===")
    
    _, audit_repo, subscription_repo, _ = setup_repositories()
    
    try:
        # Create subscription plans
        print("Creating subscription plans...")
        
        # Basic plan
        basic_plan = SubscriptionPlan(
            name="Basic Plan",
            description="Essential mental health tracking",
            price=Decimal('9.99'),
            billing_cycle=BillingCycle.MONTHLY.value,
            features=["mood_tracking", "basic_analytics", "daily_checkins"],
            limits={"journal_entries_per_month": 50, "ai_sessions_per_month": 5},
            trial_days=7
        )
        
        plan_repo = SubscriptionPlanRepository(subscription_repo.db, subscription_repo.logger)
        created_basic_plan = plan_repo.create(basic_plan)
        print(f"Created plan: {created_basic_plan.name} - ${created_basic_plan.price}/month")
        
        # Premium plan
        premium_plan = SubscriptionPlan(
            name="Premium Plan",
            description="Complete mental wellness solution",
            price=Decimal('19.99'),
            billing_cycle=BillingCycle.MONTHLY.value,
            features=["mood_tracking", "advanced_analytics", "unlimited_journaling", "ai_therapy", "crisis_support"],
            limits={"journal_entries_per_month": -1, "ai_sessions_per_month": -1},  # unlimited
            trial_days=14
        )
        
        created_premium_plan = plan_repo.create(premium_plan)
        print(f"Created plan: {created_premium_plan.name} - ${created_premium_plan.price}/month")
        
        # Create subscription for user
        print("Creating subscription for user...")
        subscription = subscription_repo.create_subscription(
            user_id=user.id,
            plan_id=created_basic_plan.id,
            start_trial=True
        )
        print(f"Created subscription: {subscription.id} (Status: {subscription.status})")
        print(f"Trial ends: {subscription.trial_end}")
        
        # Log subscription creation
        audit_repo.log_user_action(
            user_id=user.id,
            action=AuditAction.CREATE.value,
            resource_type="subscription",
            resource_id=str(subscription.id),
            details={
                "plan_id": subscription.plan_id,
                "status": subscription.status,
                "trial_end": subscription.trial_end.isoformat() if subscription.trial_end else None
            }
        )
        
        # Get user subscription
        user_subscription = subscription_repo.get_user_subscription(user.id)
        print(f"User subscription status: {user_subscription.status}")
        print(f"Days until trial end: {user_subscription.days_until_trial_end()}")
        
        # Upgrade subscription
        print("Upgrading subscription...")
        upgraded_subscription = subscription_repo.upgrade_subscription(
            subscription.id, 
            created_premium_plan.id,
            prorate=True
        )
        print(f"Upgraded to plan: {upgraded_subscription.plan_id}")
        
        # Get subscription history
        history = subscription_repo.get_user_subscription_history(user.id)
        print(f"User has {len(history)} subscription records")
        
        return subscription
        
    except Exception as e:
        print(f"Error in subscription operations: {e}")
        return None


def demonstrate_session_operations(user: User):
    """Demonstrate session repository operations."""
    print("\n=== Session Repository Operations ===")
    
    _, audit_repo, _, session_repo = setup_repositories()
    
    try:
        # Create user session
        print("Creating user session...")
        session = session_repo.create_session(
            user_id=user.id,
            ip_address="192.168.1.100",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            device_info={
                "os": "macOS",
                "browser": "Chrome",
                "version": "96.0.4664.110"
            },
            location={"country": "US", "state": "CA", "city": "San Francisco"},
            is_remember_me=False
        )
        print(f"Created session: {session.id}")
        print(f"Session token: {session.token[:20]}...")
        print(f"Risk score: {session.risk_score}")
        
        # Log session creation
        audit_repo.log_security_event(
            action="session_created",
            user_id=user.id,
            ip_address=session.ip_address,
            details={
                "session_id": session.id,
                "user_agent": session.user_agent,
                "risk_score": session.risk_score
            }
        )
        
        # Validate session
        print("Validating session...")
        validated_session = session_repo.validate_session(session.token)
        if validated_session:
            print(f"Session validation successful: {validated_session.id}")
        
        # Update session data
        print("Updating session data...")
        session_repo.update_session_data(session.id, {
            "last_page": "/dashboard",
            "feature_flags": ["premium_ui", "beta_features"],
            "preferences": {"theme": "dark", "notifications": True}
        })
        
        # Get user sessions
        user_sessions = session_repo.get_user_sessions(user.id, active_only=True)
        print(f"User has {len(user_sessions)} active sessions")
        
        # Extend session
        print("Extending session...")
        session_repo.extend_session(session.id, timedelta(hours=12))
        
        # Create additional session (different device)
        mobile_session = session_repo.create_session(
            user_id=user.id,
            ip_address="10.0.0.50",
            user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X)",
            device_info={
                "os": "iOS",
                "browser": "Safari",
                "version": "15.0"
            },
            location={"country": "US", "state": "CA", "city": "Los Angeles"},
            is_remember_me=True
        )
        print(f"Created mobile session: {mobile_session.id}")
        
        # Get session analytics
        print("Generating session analytics...")
        analytics = session_repo.generate_session_analytics(
            start_date=datetime.utcnow() - timedelta(days=30)
        )
        print(f"Analytics - Total sessions: {analytics.total_sessions}")
        print(f"Analytics - Unique users: {analytics.unique_users}")
        print(f"Analytics - Suspicious sessions: {analytics.suspicious_sessions}")
        
        return session
        
    except Exception as e:
        print(f"Error in session operations: {e}")
        return None


def demonstrate_audit_operations(user: User):
    """Demonstrate audit repository operations."""
    print("\n=== Audit Repository Operations ===")
    
    _, audit_repo, _, _ = setup_repositories()
    
    try:
        # Log various audit events
        print("Logging audit events...")
        
        # User action
        audit_repo.log_user_action(
            user_id=user.id,
            action=AuditAction.READ.value,
            resource_type="profile",
            resource_id=str(user.id),
            details={"section": "personal_info"}
        )
        
        # System event
        audit_repo.log_system_event(
            action="backup_completed",
            resource_type="database",
            details={"backup_size": "2.5GB", "duration": "45 minutes"}
        )
        
        # Security event
        audit_repo.log_security_event(
            action="failed_login",
            user_id=user.id,
            ip_address="192.168.1.100",
            details={"reason": "invalid_password", "attempt_count": 3},
            success=False
        )
        
        # Data modification with old/new values
        audit_repo.log_audit_event(
            user_id=user.id,
            action=AuditAction.UPDATE.value,
            resource_type="user",
            resource_id=str(user.id),
            old_values={"first_name": "John", "email": "john.doe@example.com"},
            new_values={"first_name": "Jonathan", "email": "john.doe@example.com"},
            level=AuditLevel.MEDIUM.value,
            compliance_category="general"
        )
        
        print("Logged various audit events")
        
        # Query audit logs
        print("Querying audit logs...")
        
        from backend.happypath.repository.audit_repository import AuditQuery
        
        # Get user's audit trail
        user_trail = audit_repo.get_user_audit_trail(user.id, limit=10)
        print(f"User audit trail: {len(user_trail)} entries")
        
        # Get security events
        security_events = audit_repo.get_security_events(
            start_time=datetime.utcnow() - timedelta(hours=24),
            limit=5
        )
        print(f"Recent security events: {len(security_events)} entries")
        
        # Get failed actions
        failed_actions = audit_repo.get_failed_actions(
            start_time=datetime.utcnow() - timedelta(hours=24),
            limit=5
        )
        print(f"Failed actions: {len(failed_actions)} entries")
        
        # Generate audit summary
        print("Generating audit summary...")
        summary = audit_repo.generate_audit_summary(
            start_time=datetime.utcnow() - timedelta(days=7),
            end_time=datetime.utcnow()
        )
        print(f"Audit summary - Total entries: {summary.total_entries}")
        print(f"Audit summary - Success rate: {summary.success_rate:.2%}")
        print(f"Audit summary - Actions breakdown: {summary.actions_breakdown}")
        
        # Export audit data
        print("Exporting audit data...")
        query = AuditQuery(
            user_id=user.id,
            start_time=datetime.utcnow() - timedelta(days=1),
            limit=100
        )
        
        json_export = audit_repo.export_audit_data(query, format="json")
        print(f"Exported audit data: {len(json_export)} characters")
        
        return True
        
    except Exception as e:
        print(f"Error in audit operations: {e}")
        return False


def demonstrate_advanced_queries():
    """Demonstrate advanced query capabilities."""
    print("\n=== Advanced Query Operations ===")
    
    user_repo, audit_repo, subscription_repo, session_repo = setup_repositories()
    
    try:
        # Advanced user queries
        print("Advanced user queries...")
        
        # Get premium users
        premium_users = user_repo.get_premium_users(limit=10)
        print(f"Premium users: {len(premium_users)}")
        
        # Get users by signup date
        recent_users = user_repo.get_users_by_signup_date(
            start_date=datetime.utcnow() - timedelta(days=30)
        )
        print(f"Users signed up in last 30 days: {len(recent_users)}")
        
        # Advanced subscription queries
        print("Advanced subscription queries...")
        
        # Get expiring subscriptions
        expiring_subs = subscription_repo.get_expiring_subscriptions(days=7)
        print(f"Subscriptions expiring in next 7 days: {len(expiring_subs)}")
        
        # Get subscriptions by status
        trial_subs = subscription_repo.get_subscriptions_by_status(
            SubscriptionStatus.TRIAL.value, 
            limit=20
        )
        print(f"Trial subscriptions: {len(trial_subs)}")
        
        # Advanced session queries
        print("Advanced session queries...")
        
        # Get suspicious sessions
        suspicious_sessions = session_repo.get_suspicious_sessions(limit=10)
        print(f"Suspicious sessions: {len(suspicious_sessions)}")
        
        # Get active sessions
        active_sessions = session_repo.get_active_sessions(limit=20)
        print(f"Active sessions: {len(active_sessions)}")
        
        # Custom query with QueryOptions
        print("Custom queries with QueryOptions...")
        
        # Find users with specific criteria
        query_options = QueryOptions(
            filters={
                'is_active': True,
                'is_verified': True
            },
            order_by=['created_at'],
            limit=10,
            include_count=True
        )
        
        result = user_repo.list_all(query_options)
        print(f"Active verified users: {len(result.data)} (Total: {result.total_count})")
        
        return True
        
    except Exception as e:
        print(f"Error in advanced queries: {e}")
        return False


def demonstrate_repository_pattern():
    """Main demonstration of repository pattern usage."""
    print("Repository Pattern Demonstration")
    print("=" * 50)
    
    try:
        # Create a user first
        user = demonstrate_user_operations()
        if not user:
            print("Failed to create user, skipping other demonstrations")
            return
        
        # Demonstrate other operations
        demonstrate_subscription_operations(user)
        demonstrate_session_operations(user)
        demonstrate_audit_operations(user)
        demonstrate_advanced_queries()
        
        print("\n" + "=" * 50)
        print("Repository pattern demonstration completed successfully!")
        
    except Exception as e:
        print(f"Error in demonstration: {e}")


if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run demonstration
    demonstrate_repository_pattern()
