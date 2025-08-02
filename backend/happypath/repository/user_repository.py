"""
User Repository

Repository implementation for user management operations.
Handles user CRUD operations, authentication, and profile management.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
import bcrypt
import logging

from .base_repository import BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult
from .base_repository import ValidationError, NotFoundError, DuplicateError


@dataclass
class User:
    """User entity representation."""
    id: Optional[int] = None
    email: str = ""
    username: str = ""
    password_hash: str = ""
    first_name: str = ""
    last_name: str = ""
    phone: Optional[str] = None
    date_of_birth: Optional[datetime] = None
    timezone: str = "UTC"
    is_active: bool = True
    is_verified: bool = False
    is_premium: bool = False
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Profile preferences
    preferences: Optional[Dict[str, Any]] = None
    notification_settings: Optional[Dict[str, Any]] = None
    
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}".strip()
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated (has valid ID)."""
        return self.id is not None
    
    def has_premium_access(self) -> bool:
        """Check if user has premium access."""
        return self.is_premium and self.is_active


@dataclass 
class UserProfile:
    """Extended user profile information."""
    user_id: int
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    therapist_name: Optional[str] = None
    therapist_contact: Optional[str] = None
    medical_conditions: Optional[List[str]] = None
    medications: Optional[List[str]] = None
    crisis_plan: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class UserRepository(BaseRepository[User, int]):
    """Repository for user management operations."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "users", logger)
        self.profile_table = "user_profiles"
    
    def _to_entity(self, row: Dict[str, Any]) -> User:
        """Convert database row to User entity."""
        return User(
            id=row.get('id'),
            email=row.get('email', ''),
            username=row.get('username', ''),
            password_hash=row.get('password_hash', ''),
            first_name=row.get('first_name', ''),
            last_name=row.get('last_name', ''),
            phone=row.get('phone'),
            date_of_birth=row.get('date_of_birth'),
            timezone=row.get('timezone', 'UTC'),
            is_active=row.get('is_active', True),
            is_verified=row.get('is_verified', False),
            is_premium=row.get('is_premium', False),
            last_login=row.get('last_login'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at'),
            preferences=row.get('preferences'),
            notification_settings=row.get('notification_settings')
        )
    
    def _to_dict(self, entity: User) -> Dict[str, Any]:
        """Convert User entity to dictionary."""
        return {
            'id': entity.id,
            'email': entity.email,
            'username': entity.username,
            'password_hash': entity.password_hash,
            'first_name': entity.first_name,
            'last_name': entity.last_name,
            'phone': entity.phone,
            'date_of_birth': entity.date_of_birth,
            'timezone': entity.timezone,
            'is_active': entity.is_active,
            'is_verified': entity.is_verified,
            'is_premium': entity.is_premium,
            'last_login': entity.last_login,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at,
            'preferences': entity.preferences,
            'notification_settings': entity.notification_settings
        }
    
    def _validate_entity(self, entity: User, is_update: bool = False) -> None:
        """Validate User entity."""
        if not entity.email:
            raise ValidationError("Email is required")
        
        if not entity.username:
            raise ValidationError("Username is required")
        
        if not is_update and not entity.password_hash:
            raise ValidationError("Password is required for new users")
        
        # Email format validation (basic)
        if '@' not in entity.email or '.' not in entity.email:
            raise ValidationError("Invalid email format")
        
        # Username validation
        if len(entity.username) < 3:
            raise ValidationError("Username must be at least 3 characters")
        
        if not entity.username.isalnum():
            raise ValidationError("Username must contain only letters and numbers")
        
        # Check for uniqueness (if not update or email/username changed)
        if not is_update:
            # Check email uniqueness
            existing_email = self.find_one_by(email=entity.email)
            if existing_email:
                raise DuplicateError("Email already exists")
            
            # Check username uniqueness
            existing_username = self.find_one_by(username=entity.username)
            if existing_username:
                raise DuplicateError("Username already exists")
    
    def create_user(self, email: str, username: str, password: str, 
                   first_name: str = "", last_name: str = "", **kwargs) -> User:
        """
        Create a new user with hashed password.
        
        Args:
            email: User email address
            username: Unique username
            password: Plain text password (will be hashed)
            first_name: User's first name
            last_name: User's last name
            **kwargs: Additional user fields
            
        Returns:
            Created User entity
        """
        # Hash the password
        password_hash = self._hash_password(password)
        
        # Create user entity
        user = User(
            email=email,
            username=username,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )
        
        return self.create(user)
    
    def authenticate_user(self, email_or_username: str, password: str) -> Optional[User]:
        """
        Authenticate user by email/username and password.
        
        Args:
            email_or_username: Email address or username
            password: Plain text password
            
        Returns:
            User entity if authentication successful, None otherwise
        """
        try:
            # Try to find user by email first, then username
            user = self.find_one_by(email=email_or_username)
            if not user:
                user = self.find_one_by(username=email_or_username)
            
            if not user:
                return None
            
            # Check if user is active
            if not user.is_active:
                return None
            
            # Verify password
            if not self._verify_password(password, user.password_hash):
                return None
            
            # Update last login
            user.last_login = datetime.utcnow()
            self.update(user)
            
            self.logger.info(f"User authenticated", extra={
                "user_id": user.id,
                "email": user.email,
                "operation": "authenticate"
            })
            
            return user
            
        except Exception as e:
            self.logger.error(f"Authentication failed for {email_or_username}: {e}")
            return None
    
    def change_password(self, user_id: int, old_password: str, new_password: str) -> bool:
        """
        Change user password with old password verification.
        
        Args:
            user_id: User ID
            old_password: Current password for verification
            new_password: New password to set
            
        Returns:
            True if password changed successfully
            
        Raises:
            NotFoundError: If user not found
            ValidationError: If old password is incorrect
        """
        user = self.get_by_id_or_raise(user_id)
        
        # Verify old password
        if not self._verify_password(old_password, user.password_hash):
            raise ValidationError("Current password is incorrect")
        
        # Update with new password
        user.password_hash = self._hash_password(new_password)
        self.update(user)
        
        self.logger.info(f"Password changed for user {user_id}")
        return True
    
    def reset_password(self, email: str, new_password: str) -> bool:
        """
        Reset user password (admin operation).
        
        Args:
            email: User email
            new_password: New password to set
            
        Returns:
            True if password reset successfully
            
        Raises:
            NotFoundError: If user not found
        """
        user = self.find_one_by_or_raise(email=email)
        user.password_hash = self._hash_password(new_password)
        self.update(user)
        
        self.logger.info(f"Password reset for user {user.id}")
        return True
    
    def activate_user(self, user_id: int) -> User:
        """Activate user account."""
        user = self.get_by_id_or_raise(user_id)
        user.is_active = True
        return self.update(user)
    
    def deactivate_user(self, user_id: int) -> User:
        """Deactivate user account."""
        user = self.get_by_id_or_raise(user_id)
        user.is_active = False
        return self.update(user)
    
    def verify_user(self, user_id: int) -> User:
        """Mark user as verified."""
        user = self.get_by_id_or_raise(user_id)
        user.is_verified = True
        return self.update(user)
    
    def upgrade_to_premium(self, user_id: int) -> User:
        """Upgrade user to premium."""
        user = self.get_by_id_or_raise(user_id)
        user.is_premium = True
        return self.update(user)
    
    def downgrade_from_premium(self, user_id: int) -> User:
        """Downgrade user from premium."""
        user = self.get_by_id_or_raise(user_id)
        user.is_premium = False
        return self.update(user)
    
    def update_last_login(self, user_id: int) -> User:
        """Update user's last login timestamp."""
        user = self.get_by_id_or_raise(user_id)
        user.last_login = datetime.utcnow()
        return self.update(user)
    
    def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email address."""
        return self.find_one_by(email=email)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        return self.find_one_by(username=username)
    
    def search_users(self, query: str, limit: int = 50) -> List[User]:
        """
        Search users by name, email, or username.
        
        Args:
            query: Search query
            limit: Maximum results to return
            
        Returns:
            List of matching users
        """
        try:
            search_query = f"""
                SELECT * FROM {self.table_name}
                WHERE 
                    is_active = true AND (
                        LOWER(first_name) LIKE LOWER(%(query)s) OR
                        LOWER(last_name) LIKE LOWER(%(query)s) OR
                        LOWER(email) LIKE LOWER(%(query)s) OR
                        LOWER(username) LIKE LOWER(%(query)s)
                    )
                ORDER BY 
                    CASE 
                        WHEN LOWER(username) = LOWER(%(exact_query)s) THEN 1
                        WHEN LOWER(email) = LOWER(%(exact_query)s) THEN 2
                        ELSE 3
                    END,
                    first_name, last_name
                LIMIT %(limit)s
            """
            
            params = {
                'query': f"%{query}%",
                'exact_query': query,
                'limit': limit
            }
            
            result = self.db.execute_query(search_query, params)
            return [self._to_entity(row) for row in result] if result else []
            
        except Exception as e:
            self.logger.error(f"Failed to search users: {e}")
            raise
    
    def get_active_users(self, limit: int = None) -> List[User]:
        """Get all active users."""
        options = QueryOptions(
            filters={'is_active': True},
            limit=limit,
            order_by=['first_name', 'last_name']
        )
        result = self.list_all(options)
        return result.data
    
    def get_premium_users(self, limit: int = None) -> List[User]:
        """Get all premium users."""
        options = QueryOptions(
            filters={'is_premium': True, 'is_active': True},
            limit=limit,
            order_by=['created_at']
        )
        result = self.list_all(options)
        return result.data
    
    def get_users_by_signup_date(self, start_date: datetime, 
                                end_date: datetime = None) -> List[User]:
        """
        Get users who signed up within date range.
        
        Args:
            start_date: Start of date range
            end_date: End of date range (defaults to now)
            
        Returns:
            List of users
        """
        end_date = end_date or datetime.utcnow()
        
        try:
            query = f"""
                SELECT * FROM {self.table_name}
                WHERE created_at >= %(start_date)s 
                AND created_at <= %(end_date)s
                ORDER BY created_at DESC
            """
            
            params = {
                'start_date': start_date,
                'end_date': end_date
            }
            
            result = self.db.execute_query(query, params)
            return [self._to_entity(row) for row in result] if result else []
            
        except Exception as e:
            self.logger.error(f"Failed to get users by signup date: {e}")
            raise
    
    # User Profile Operations
    
    def create_profile(self, user_id: int, profile_data: Dict[str, Any]) -> UserProfile:
        """Create user profile."""
        try:
            # Ensure user exists
            self.get_by_id_or_raise(user_id)
            
            data = {
                'user_id': user_id,
                'created_at': datetime.utcnow(),
                'updated_at': datetime.utcnow(),
                **profile_data
            }
            
            # Convert lists to JSON for storage
            if 'medical_conditions' in data and isinstance(data['medical_conditions'], list):
                data['medical_conditions'] = data['medical_conditions']
            if 'medications' in data and isinstance(data['medications'], list):
                data['medications'] = data['medications']
            
            columns = list(data.keys())
            placeholders = [f"%({col})s" for col in columns]
            
            query = f"""
                INSERT INTO {self.profile_table} ({', '.join(columns)})
                VALUES ({', '.join(placeholders)})
                RETURNING *
            """
            
            result = self.db.execute_query(query, data)
            if not result:
                raise Exception("Failed to create profile")
            
            return self._row_to_profile(result[0])
            
        except Exception as e:
            self.logger.error(f"Failed to create profile for user {user_id}: {e}")
            raise
    
    def get_profile(self, user_id: int) -> Optional[UserProfile]:
        """Get user profile by user ID."""
        try:
            query = f"SELECT * FROM {self.profile_table} WHERE user_id = %(user_id)s"
            result = self.db.execute_query(query, {"user_id": user_id})
            
            if result:
                return self._row_to_profile(result[0])
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get profile for user {user_id}: {e}")
            raise
    
    def update_profile(self, user_id: int, profile_data: Dict[str, Any]) -> UserProfile:
        """Update user profile."""
        try:
            # Check if profile exists
            existing = self.get_profile(user_id)
            if not existing:
                raise NotFoundError(f"Profile for user {user_id} not found")
            
            # Prepare update data
            update_data = {
                **profile_data,
                'updated_at': datetime.utcnow()
            }
            
            # Convert lists to JSON for storage
            if 'medical_conditions' in update_data and isinstance(update_data['medical_conditions'], list):
                update_data['medical_conditions'] = update_data['medical_conditions']
            if 'medications' in update_data and isinstance(update_data['medications'], list):
                update_data['medications'] = update_data['medications']
            
            set_clauses = [f"{col} = %({col})s" for col in update_data.keys()]
            query = f"""
                UPDATE {self.profile_table}
                SET {', '.join(set_clauses)}
                WHERE user_id = %(user_id)s
                RETURNING *
            """
            
            params = {**update_data, 'user_id': user_id}
            result = self.db.execute_query(query, params)
            
            if not result:
                raise Exception("Failed to update profile")
                
            return self._row_to_profile(result[0])
            
        except Exception as e:
            self.logger.error(f"Failed to update profile for user {user_id}: {e}")
            raise
    
    def _row_to_profile(self, row: Dict[str, Any]) -> UserProfile:
        """Convert database row to UserProfile."""
        return UserProfile(
            user_id=row['user_id'],
            bio=row.get('bio'),
            avatar_url=row.get('avatar_url'),
            emergency_contact_name=row.get('emergency_contact_name'),
            emergency_contact_phone=row.get('emergency_contact_phone'),
            therapist_name=row.get('therapist_name'),
            therapist_contact=row.get('therapist_contact'),
            medical_conditions=row.get('medical_conditions', []),
            medications=row.get('medications', []),
            crisis_plan=row.get('crisis_plan'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at')
        )
    
    # Password utilities
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


class AsyncUserRepository(AsyncBaseRepository[User, int]):
    """Async version of UserRepository."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "users", logger)
        self.profile_table = "user_profiles"
    
    def _to_entity(self, row: Dict[str, Any]) -> User:
        """Convert database row to User entity."""
        return User(
            id=row.get('id'),
            email=row.get('email', ''),
            username=row.get('username', ''),
            password_hash=row.get('password_hash', ''),
            first_name=row.get('first_name', ''),
            last_name=row.get('last_name', ''),
            phone=row.get('phone'),
            date_of_birth=row.get('date_of_birth'),
            timezone=row.get('timezone', 'UTC'),
            is_active=row.get('is_active', True),
            is_verified=row.get('is_verified', False),
            is_premium=row.get('is_premium', False),
            last_login=row.get('last_login'),
            created_at=row.get('created_at'),
            updated_at=row.get('updated_at'),
            preferences=row.get('preferences'),
            notification_settings=row.get('notification_settings')
        )
    
    def _to_dict(self, entity: User) -> Dict[str, Any]:
        """Convert User entity to dictionary."""
        return {
            'id': entity.id,
            'email': entity.email,
            'username': entity.username,
            'password_hash': entity.password_hash,
            'first_name': entity.first_name,
            'last_name': entity.last_name,
            'phone': entity.phone,
            'date_of_birth': entity.date_of_birth,
            'timezone': entity.timezone,
            'is_active': entity.is_active,
            'is_verified': entity.is_verified,
            'is_premium': entity.is_premium,
            'last_login': entity.last_login,
            'created_at': entity.created_at,
            'updated_at': entity.updated_at,
            'preferences': entity.preferences,
            'notification_settings': entity.notification_settings
        }
    
    async def _validate_entity(self, entity: User, is_update: bool = False) -> None:
        """Async validate User entity."""
        if not entity.email:
            raise ValidationError("Email is required")
        
        if not entity.username:
            raise ValidationError("Username is required")
        
        if not is_update and not entity.password_hash:
            raise ValidationError("Password is required for new users")
        
        # Email format validation (basic)
        if '@' not in entity.email or '.' not in entity.email:
            raise ValidationError("Invalid email format")
        
        # Username validation
        if len(entity.username) < 3:
            raise ValidationError("Username must be at least 3 characters")
        
        if not entity.username.isalnum():
            raise ValidationError("Username must contain only letters and numbers")
    
    async def authenticate_user(self, email_or_username: str, password: str) -> Optional[User]:
        """Async authenticate user."""
        try:
            # Try to find user by email first, then username
            user = await self.find_one_by_async(email=email_or_username)
            if not user:
                user = await self.find_one_by_async(username=email_or_username)
            
            if not user:
                return None
            
            # Check if user is active
            if not user.is_active:
                return None
            
            # Verify password
            if not self._verify_password(password, user.password_hash):
                return None
            
            # Update last login
            user.last_login = datetime.utcnow()
            await self.update(user)
            
            return user
            
        except Exception as e:
            self.logger.error(f"Authentication failed for {email_or_username}: {e}")
            return None
    
    # Additional async methods would follow similar patterns...
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def _verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash."""
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
