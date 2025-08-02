"""
Repository Pattern Test Suite

Comprehensive tests for the repository pattern implementation including
base repository functionality and specialized repositories.
"""

import pytest
import asyncio
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import Mock, MagicMock, patch
import logging

# Import repository classes and entities
from backend.happypath.repository import (
    # Base classes
    BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult,
    RepositoryError, ValidationError, NotFoundError, DuplicateError,
    
    # User repository
    User, UserProfile, UserRepository, AsyncUserRepository,
    
    # Audit repository  
    AuditEntry, AuditQuery, AuditAction, AuditLevel, AuditRepository,
    
    # Session repository
    UserSession, SessionStatus, SessionRepository,
    
    # Subscription repository
    SubscriptionPlan, Subscription, SubscriptionStatus, BillingCycle,
    SubscriptionPlanRepository, SubscriptionRepository,
    
    # Factory functions
    create_user_repository, create_audit_repository
)


class TestBaseRepository:
    """Test cases for BaseRepository functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_db = Mock()
        self.mock_logger = Mock()
        
        # Create a concrete implementation for testing
        class TestEntity:
            def __init__(self, id=None, name="", value=0):
                self.id = id
                self.name = name
                self.value = value
        
        class TestRepository(BaseRepository[TestEntity, int]):
            def _to_entity(self, row):
                return TestEntity(
                    id=row.get('id'),
                    name=row.get('name', ''),
                    value=row.get('value', 0)
                )
            
            def _to_dict(self, entity):
                return {
                    'id': entity.id,
                    'name': entity.name,
                    'value': entity.value
                }
            
            def _validate_entity(self, entity, is_update=False):
                if not entity.name:
                    raise ValidationError("Name is required")
        
        self.TestEntity = TestEntity
        self.repository = TestRepository(self.mock_db, "test_entities", self.mock_logger)
    
    def test_create_entity(self):
        """Test entity creation."""
        # Mock database response
        created_row = {
            'id': 1,
            'name': 'Test Entity',
            'value': 42,
            'created_at': datetime.utcnow(),
            'updated_at': datetime.utcnow()
        }
        self.mock_db.execute_query.return_value = [created_row]
        
        # Create entity
        entity = self.TestEntity(name="Test Entity", value=42)
        result = self.repository.create(entity)
        
        # Assertions
        assert result.id == 1
        assert result.name == "Test Entity"
        assert result.value == 42
        
        # Verify database call
        self.mock_db.execute_query.assert_called_once()
        call_args = self.mock_db.execute_query.call_args
        assert "INSERT INTO test_entities" in call_args[0][0]
    
    def test_create_validation_error(self):
        """Test validation error during creation."""
        entity = self.TestEntity(name="", value=42)  # Empty name should fail
        
        with pytest.raises(ValidationError) as exc_info:
            self.repository.create(entity)
        
        assert "Name is required" in str(exc_info.value)
    
    def test_get_by_id(self):
        """Test getting entity by ID."""
        # Mock database response
        row = {'id': 1, 'name': 'Test Entity', 'value': 42}
        self.mock_db.execute_query.return_value = [row]
        
        result = self.repository.get_by_id(1)
        
        assert result is not None
        assert result.id == 1
        assert result.name == "Test Entity"
        
        # Verify database call
        self.mock_db.execute_query.assert_called_once()
        call_args = self.mock_db.execute_query.call_args
        assert "SELECT * FROM test_entities WHERE id" in call_args[0][0]
        assert call_args[1]['id'] == 1
    
    def test_get_by_id_not_found(self):
        """Test getting non-existent entity."""
        self.mock_db.execute_query.return_value = []
        
        result = self.repository.get_by_id(999)
        
        assert result is None
    
    def test_get_by_id_or_raise_not_found(self):
        """Test get_by_id_or_raise with non-existent entity."""
        self.mock_db.execute_query.return_value = []
        
        with pytest.raises(NotFoundError) as exc_info:
            self.repository.get_by_id_or_raise(999)
        
        assert "with ID 999 not found" in str(exc_info.value)
    
    def test_update_entity(self):
        """Test entity update."""
        # Mock existing entity check
        existing_row = {'id': 1, 'name': 'Old Name', 'value': 10}
        updated_row = {
            'id': 1, 
            'name': 'Updated Name', 
            'value': 20,
            'updated_at': datetime.utcnow()
        }
        
        self.mock_db.execute_query.side_effect = [
            [existing_row],  # get_by_id call
            [updated_row]    # update call
        ]
        
        entity = self.TestEntity(id=1, name="Updated Name", value=20)
        result = self.repository.update(entity)
        
        assert result.id == 1
        assert result.name == "Updated Name"
        assert result.value == 20
        
        # Verify two database calls (check + update)
        assert self.mock_db.execute_query.call_count == 2
    
    def test_update_not_found(self):
        """Test updating non-existent entity."""
        self.mock_db.execute_query.return_value = []  # Entity not found
        
        entity = self.TestEntity(id=999, name="Test", value=1)
        
        with pytest.raises(NotFoundError):
            self.repository.update(entity)
    
    def test_delete_entity(self):
        """Test entity deletion."""
        self.mock_db.execute_query.return_value = []
        self.mock_db.get_affected_rows.return_value = 1
        
        result = self.repository.delete(1)
        
        assert result is True
        
        # Verify database call
        self.mock_db.execute_query.assert_called_once()
        call_args = self.mock_db.execute_query.call_args
        assert "DELETE FROM test_entities WHERE id" in call_args[0][0]
    
    def test_delete_not_found(self):
        """Test deleting non-existent entity."""
        self.mock_db.execute_query.return_value = []
        self.mock_db.get_affected_rows.return_value = 0
        
        result = self.repository.delete(999)
        
        assert result is False
    
    def test_list_all_with_filters(self):
        """Test listing entities with filters."""
        rows = [
            {'id': 1, 'name': 'Entity 1', 'value': 10},
            {'id': 2, 'name': 'Entity 2', 'value': 20}
        ]
        count_row = {'count': 2}
        
        self.mock_db.execute_query.side_effect = [
            [count_row],  # count query
            rows          # main query
        ]
        
        options = QueryOptions(
            filters={'value': 10},
            limit=10,
            include_count=True
        )
        
        result = self.repository.list_all(options)
        
        assert len(result.data) == 2
        assert result.total_count == 2
        assert result.data[0].name == "Entity 1"
    
    def test_exists(self):
        """Test entity existence check."""
        self.mock_db.execute_query.return_value = [{'id': 1}]
        
        result = self.repository.exists(1)
        
        assert result is True
        
        # Verify database call
        call_args = self.mock_db.execute_query.call_args
        assert "SELECT 1 FROM test_entities WHERE id" in call_args[0][0]
    
    def test_count(self):
        """Test entity count."""
        self.mock_db.execute_query.return_value = [{'count': 5}]
        
        result = self.repository.count()
        
        assert result == 5
    
    def test_find_by(self):
        """Test finding entities by criteria."""
        rows = [{'id': 1, 'name': 'Test', 'value': 42}]
        count_row = {'count': 1}
        
        self.mock_db.execute_query.side_effect = [
            [count_row],  # count query
            rows          # main query
        ]
        
        result = self.repository.find_by(name="Test")
        
        assert len(result) == 1
        assert result[0].name == "Test"


class TestUserRepository:
    """Test cases for UserRepository."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_db = Mock()
        self.mock_logger = Mock()
        self.user_repo = UserRepository(self.mock_db, self.mock_logger)
    
    def test_create_user(self):
        """Test user creation with password hashing."""
        # Mock database response
        created_row = {
            'id': 1,
            'email': 'test@example.com',
            'username': 'testuser',
            'password_hash': 'hashed_password',
            'first_name': 'Test',
            'last_name': 'User',
            'is_active': True,
            'created_at': datetime.utcnow()
        }
        self.mock_db.execute_query.return_value = [created_row]
        
        # Mock password hashing
        with patch.object(self.user_repo, '_hash_password', return_value='hashed_password'):
            user = self.user_repo.create_user(
                email="test@example.com",
                username="testuser", 
                password="test_password",
                first_name="Test",
                last_name="User"
            )
        
        assert user.id == 1
        assert user.email == "test@example.com"
        assert user.username == "testuser"
        assert user.full_name() == "Test User"
    
    def test_authenticate_user_success(self):
        """Test successful user authentication."""
        # Mock database response
        user_row = {
            'id': 1,
            'email': 'test@example.com',
            'username': 'testuser',
            'password_hash': 'hashed_password',
            'is_active': True,
            'last_login': None
        }
        updated_row = {**user_row, 'last_login': datetime.utcnow()}
        
        self.mock_db.execute_query.side_effect = [
            [user_row],    # find user by email
            [updated_row]  # update last_login
        ]
        
        # Mock password verification
        with patch.object(self.user_repo, '_verify_password', return_value=True):
            user = self.user_repo.authenticate_user("test@example.com", "test_password")
        
        assert user is not None
        assert user.email == "test@example.com"
        assert user.is_authenticated()
    
    def test_authenticate_user_wrong_password(self):
        """Test authentication with wrong password."""
        user_row = {
            'id': 1,
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'is_active': True
        }
        self.mock_db.execute_query.return_value = [user_row]
        
        # Mock password verification failure
        with patch.object(self.user_repo, '_verify_password', return_value=False):
            user = self.user_repo.authenticate_user("test@example.com", "wrong_password")
        
        assert user is None
    
    def test_authenticate_inactive_user(self):
        """Test authentication of inactive user."""
        user_row = {
            'id': 1,
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'is_active': False
        }
        self.mock_db.execute_query.return_value = [user_row]
        
        user = self.user_repo.authenticate_user("test@example.com", "test_password")
        
        assert user is None
    
    def test_change_password(self):
        """Test password change."""
        user_row = {
            'id': 1,
            'password_hash': 'old_hashed_password'
        }
        updated_row = {
            **user_row,
            'password_hash': 'new_hashed_password',
            'updated_at': datetime.utcnow()
        }
        
        self.mock_db.execute_query.side_effect = [
            [user_row],    # get user
            [updated_row]  # update user
        ]
        
        with patch.object(self.user_repo, '_verify_password', return_value=True):
            with patch.object(self.user_repo, '_hash_password', return_value='new_hashed_password'):
                result = self.user_repo.change_password(1, "old_password", "new_password")
        
        assert result is True
    
    def test_change_password_wrong_old_password(self):
        """Test password change with wrong old password."""
        user_row = {'id': 1, 'password_hash': 'old_hashed_password'}
        self.mock_db.execute_query.return_value = [user_row]
        
        with patch.object(self.user_repo, '_verify_password', return_value=False):
            with pytest.raises(ValidationError) as exc_info:
                self.user_repo.change_password(1, "wrong_old_password", "new_password")
        
        assert "Current password is incorrect" in str(exc_info.value)
    
    def test_search_users(self):
        """Test user search functionality."""
        search_results = [
            {'id': 1, 'first_name': 'John', 'last_name': 'Doe', 'email': 'john@example.com', 'username': 'johndoe'},
            {'id': 2, 'first_name': 'Jane', 'last_name': 'Smith', 'email': 'jane@example.com', 'username': 'janesmith'}
        ]
        self.mock_db.execute_query.return_value = search_results
        
        users = self.user_repo.search_users("john", limit=10)
        
        assert len(users) == 2
        assert users[0].first_name == "John"
        
        # Verify search query
        call_args = self.mock_db.execute_query.call_args
        assert "LIKE LOWER" in call_args[0][0]
        assert call_args[1]['query'] == "%john%"


class TestAuditRepository:
    """Test cases for AuditRepository."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_db = Mock()
        self.mock_logger = Mock()
        self.audit_repo = AuditRepository(self.mock_db, self.mock_logger)
    
    def test_log_audit_event(self):
        """Test logging an audit event."""
        # Mock database response
        created_row = {
            'id': 1,
            'user_id': 123,
            'action': 'create',
            'resource_type': 'user',
            'resource_id': '123',
            'timestamp': datetime.utcnow(),
            'level': 'low',
            'success': True,
            'created_at': datetime.utcnow()
        }
        self.mock_db.execute_query.return_value = [created_row]
        
        audit_entry = self.audit_repo.log_audit_event(
            user_id=123,
            action=AuditAction.CREATE.value,
            resource_type="user",
            resource_id="123",
            details={"email": "test@example.com"},
            level=AuditLevel.LOW.value
        )
        
        assert audit_entry.id == 1
        assert audit_entry.user_id == 123
        assert audit_entry.action == "create"
        assert audit_entry.resource_type == "user"
    
    def test_log_user_action(self):
        """Test logging a user action (convenience method)."""
        created_row = {
            'id': 1,
            'user_id': 123,
            'action': 'read',
            'resource_type': 'profile',
            'timestamp': datetime.utcnow(),
            'created_at': datetime.utcnow()
        }
        self.mock_db.execute_query.return_value = [created_row]
        
        audit_entry = self.audit_repo.log_user_action(
            user_id=123,
            action=AuditAction.READ.value,
            resource_type="profile"
        )
        
        assert audit_entry.user_id == 123
        assert audit_entry.action == "read"
    
    def test_log_security_event(self):
        """Test logging a security event."""
        created_row = {
            'id': 1,
            'user_id': 123,
            'action': 'failed_login',
            'resource_type': 'security',
            'level': 'high',
            'success': False,
            'compliance_category': 'security',
            'timestamp': datetime.utcnow(),
            'created_at': datetime.utcnow()
        }
        self.mock_db.execute_query.return_value = [created_row]
        
        audit_entry = self.audit_repo.log_security_event(
            action="failed_login",
            user_id=123,
            success=False
        )
        
        assert audit_entry.action == "failed_login"
        assert audit_entry.level == AuditLevel.HIGH.value
        assert audit_entry.success is False
    
    def test_get_user_audit_trail(self):
        """Test getting user audit trail."""
        audit_rows = [
            {
                'id': 1,
                'user_id': 123,
                'action': 'login',
                'resource_type': 'auth',
                'timestamp': datetime.utcnow(),
                'success': True
            },
            {
                'id': 2,
                'user_id': 123,
                'action': 'update',
                'resource_type': 'profile',
                'timestamp': datetime.utcnow() - timedelta(hours=1),
                'success': True
            }
        ]
        
        # Mock count and main queries
        count_row = {'count': 2}
        self.mock_db.execute_query.side_effect = [
            [count_row],  # count query
            audit_rows    # main query
        ]
        
        trail = self.audit_repo.get_user_audit_trail(123, limit=10)
        
        assert len(trail) == 2
        assert trail[0].action == "login"
        assert trail[1].action == "update"
    
    def test_generate_audit_summary(self):
        """Test generating audit summary."""
        # Mock summary queries
        basic_stats = {
            'total_entries': 100,
            'unique_users': 25,
            'unique_sessions': 40,
            'success_rate': 0.95
        }
        
        actions_breakdown = [
            {'action': 'login', 'count': 50},
            {'action': 'update', 'count': 30},
            {'action': 'create', 'count': 20}
        ]
        
        level_breakdown = [
            {'level': 'low', 'count': 70},
            {'level': 'medium', 'count': 25},
            {'level': 'high', 'count': 5}
        ]
        
        active_users = [
            {'user_id': 1, 'action_count': 25},
            {'user_id': 2, 'action_count': 20}
        ]
        
        self.mock_db.execute_query.side_effect = [
            [basic_stats],      # basic stats
            actions_breakdown,  # actions
            level_breakdown,    # levels
            active_users        # active users
        ]
        
        # Mock the query_audit_logs method for critical events
        with patch.object(self.audit_repo, 'query_audit_logs') as mock_query:
            mock_query.return_value = Mock(data=[])
            
            summary = self.audit_repo.generate_audit_summary(
                start_time=datetime.utcnow() - timedelta(days=7),
                end_time=datetime.utcnow()
            )
        
        assert summary.total_entries == 100
        assert summary.unique_users == 25
        assert summary.success_rate == 0.95
        assert summary.actions_breakdown['login'] == 50


class TestSessionRepository:
    """Test cases for SessionRepository."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_db = Mock()
        self.mock_logger = Mock()
        self.session_repo = SessionRepository(self.mock_db, self.mock_logger)
    
    def test_create_session(self):
        """Test session creation."""
        created_row = {
            'id': 'session_123',
            'user_id': 1,
            'token': 'secure_token_123',
            'ip_address': '192.168.1.100',
            'is_active': True,
            'risk_score': 0.2,
            'created_at': datetime.utcnow()
        }
        self.mock_db.execute_query.return_value = [created_row]
        
        # Mock token generation and risk calculation
        with patch.object(self.session_repo, '_generate_session_token', return_value='secure_token_123'):
            with patch.object(self.session_repo, '_calculate_risk_score', return_value=0.2):
                with patch.object(self.session_repo, '_cleanup_user_sessions'):
                    session = self.session_repo.create_session(
                        user_id=1,
                        ip_address='192.168.1.100',
                        user_agent='Mozilla/5.0...'
                    )
        
        assert session.user_id == 1
        assert session.token == 'secure_token_123'
        assert session.risk_score == 0.2
    
    def test_validate_session_success(self):
        """Test successful session validation."""
        session_row = {
            'id': 'session_123',
            'user_id': 1,
            'token': 'valid_token',
            'is_active': True,
            'expires_at': datetime.utcnow() + timedelta(hours=24),
            'terminated_at': None
        }
        
        self.mock_db.execute_query.side_effect = [
            [session_row],  # find session
            []              # update last activity
        ]
        
        # Mock update_last_activity
        with patch.object(self.session_repo, 'update_last_activity', return_value=True):
            session = self.session_repo.validate_session('valid_token')
        
        assert session is not None
        assert session.token == 'valid_token'
    
    def test_validate_session_expired(self):
        """Test validation of expired session."""
        session_row = {
            'id': 'session_123',
            'user_id': 1,
            'token': 'expired_token',
            'is_active': True,
            'expires_at': datetime.utcnow() - timedelta(hours=1),  # Expired
            'terminated_at': None
        }
        
        self.mock_db.execute_query.return_value = [session_row]
        
        session = self.session_repo.validate_session('expired_token')
        
        assert session is None
    
    def test_terminate_session(self):
        """Test session termination."""
        session_row = {
            'id': 'session_123',
            'user_id': 1,
            'is_active': True,
            'security_flags': []
        }
        updated_row = {
            **session_row,
            'is_active': False,
            'terminated_at': datetime.utcnow(),
            'security_flags': ['terminated:user_logout']
        }
        
        self.mock_db.execute_query.side_effect = [
            [session_row],  # get session
            [updated_row]   # update session
        ]
        
        result = self.session_repo.terminate_session('session_123', 'user_logout')
        
        assert result is True
    
    def test_cleanup_expired_sessions(self):
        """Test cleanup of expired sessions."""
        self.mock_db.get_affected_rows.side_effect = [5, 3]  # 5 expired, 3 deleted
        
        cleaned_count = self.session_repo.cleanup_expired_sessions()
        
        assert cleaned_count == 8
        assert self.mock_db.execute_query.call_count == 2


class TestSubscriptionRepository:
    """Test cases for SubscriptionRepository."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_db = Mock()
        self.mock_logger = Mock()
        self.subscription_repo = SubscriptionRepository(self.mock_db, self.mock_logger)
        
        # Mock plan repository
        self.mock_plan_repo = Mock()
        self.subscription_repo.plan_repo = self.mock_plan_repo
    
    def test_create_subscription_with_trial(self):
        """Test creating subscription with trial period."""
        # Mock plan
        plan = Mock()
        plan.id = 1
        plan.trial_days = 7
        plan.price = Decimal('9.99')
        plan.billing_cycle = BillingCycle.MONTHLY.value
        
        self.mock_plan_repo.get_by_id_or_raise.return_value = plan
        
        # Mock database response
        created_row = {
            'id': 1,
            'user_id': 123,
            'plan_id': 1,
            'status': SubscriptionStatus.TRIAL.value,
            'trial_start': datetime.utcnow(),
            'trial_end': datetime.utcnow() + timedelta(days=7),
            'created_at': datetime.utcnow()
        }
        self.mock_db.execute_query.return_value = [created_row]
        
        subscription = self.subscription_repo.create_subscription(
            user_id=123,
            plan_id=1,
            start_trial=True
        )
        
        assert subscription.user_id == 123
        assert subscription.plan_id == 1
        assert subscription.status == SubscriptionStatus.TRIAL.value
        assert subscription.is_trial()
    
    def test_cancel_subscription(self):
        """Test subscription cancellation."""
        subscription_row = {
            'id': 1,
            'user_id': 123,
            'status': SubscriptionStatus.ACTIVE.value,
            'current_period_end': datetime.utcnow() + timedelta(days=15)
        }
        
        updated_row = {
            **subscription_row,
            'canceled_at': datetime.utcnow(),
            'cancellation_reason': 'user_request',
            'ends_at': subscription_row['current_period_end']
        }
        
        self.mock_db.execute_query.side_effect = [
            [subscription_row],  # get subscription
            [updated_row]        # update subscription
        ]
        
        subscription = self.subscription_repo.cancel_subscription(1, 'user_request')
        
        assert subscription.cancellation_reason == 'user_request'
        assert subscription.ends_at is not None
    
    def test_upgrade_subscription(self):
        """Test subscription upgrade."""
        # Mock current subscription
        subscription_row = {
            'id': 1,
            'user_id': 123,
            'plan_id': 1,
            'status': SubscriptionStatus.ACTIVE.value,
            'next_billing_date': datetime.utcnow() + timedelta(days=15)
        }
        
        # Mock plans
        old_plan = Mock()
        old_plan.id = 1
        old_plan.price = Decimal('9.99')
        
        new_plan = Mock()
        new_plan.id = 2
        new_plan.price = Decimal('19.99')
        
        self.mock_plan_repo.get_by_id_or_raise.side_effect = [new_plan, old_plan]
        
        updated_row = {
            **subscription_row,
            'plan_id': 2,
            'next_payment_amount': float(new_plan.price)
        }
        
        self.mock_db.execute_query.side_effect = [
            [subscription_row],  # get subscription
            [updated_row]        # update subscription
        ]
        
        subscription = self.subscription_repo.upgrade_subscription(1, 2, prorate=True)
        
        assert subscription.plan_id == 2
        assert subscription.next_payment_amount == new_plan.price


class TestRepositoryFactory:
    """Test repository factory functions."""
    
    def test_create_user_repository(self):
        """Test user repository factory."""
        mock_db = Mock()
        mock_logger = Mock()
        
        repo = create_user_repository(mock_db, mock_logger)
        
        assert isinstance(repo, UserRepository)
        assert repo.db == mock_db
        assert repo.logger == mock_logger
    
    def test_create_audit_repository(self):
        """Test audit repository factory."""
        mock_db = Mock()
        
        repo = create_audit_repository(mock_db)
        
        assert isinstance(repo, AuditRepository)
        assert repo.db == mock_db


class TestAsyncRepository:
    """Test async repository functionality."""
    
    @pytest.mark.asyncio
    async def test_async_user_repository_authenticate(self):
        """Test async user authentication."""
        mock_db = Mock()
        mock_logger = Mock()
        repo = AsyncUserRepository(mock_db, mock_logger)
        
        # Mock async methods
        repo.find_one_by_async = Mock(return_value=None)
        
        # Test non-existent user
        user = await repo.authenticate_user("nonexistent@example.com", "password")
        
        assert user is None


def test_query_options():
    """Test QueryOptions dataclass."""
    options = QueryOptions(
        limit=10,
        offset=20,
        order_by=['name', '-created_at'],
        filters={'active': True, 'type': 'premium'},
        include_count=True
    )
    
    assert options.limit == 10
    assert options.offset == 20
    assert options.order_by == ['name', '-created_at']
    assert options.filters == {'active': True, 'type': 'premium'}
    assert options.include_count is True


def test_query_result():
    """Test QueryResult dataclass."""
    data = [Mock(), Mock(), Mock()]
    
    result = QueryResult(
        data=data,
        total_count=100,
        page=2,
        page_size=10,
        has_next=True,
        has_previous=True
    )
    
    assert len(result.data) == 3
    assert result.total_count == 100
    assert result.page == 2
    assert result.has_next is True


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
