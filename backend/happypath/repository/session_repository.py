"""
Session Repository

Repository implementation for user session management.
Handles session creation, validation, cleanup, and analytics.
"""

from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import secrets
import json
import logging

from .base_repository import BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult
from .base_repository import ValidationError, NotFoundError


class SessionStatus(Enum):
    """Session status enumeration."""
    ACTIVE = "active"
    EXPIRED = "expired"
    TERMINATED = "terminated"
    INVALID = "invalid"


@dataclass
class UserSession:
    """User session entity representation."""
    id: Optional[str] = None  # Session ID (UUID)
    user_id: Optional[int] = None
    token: str = ""  # Session token
    device_info: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    location: Optional[Dict[str, Any]] = None  # Geographic location info
    
    # Session lifecycle
    created_at: Optional[datetime] = None
    last_activity: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    terminated_at: Optional[datetime] = None
    
    # Session metadata
    is_active: bool = True
    is_remember_me: bool = False
    login_method: str = "password"  # password, oauth, sso, etc.
    
    # Security flags
    is_suspicious: bool = False
    risk_score: float = 0.0
    security_flags: Optional[List[str]] = None
    
    # Additional data
    session_data: Optional[Dict[str, Any]] = None  # Custom session data
    
    def is_expired(self) -> bool:
        """Check if session is expired."""
        if not self.expires_at:
            return False
        return datetime.utcnow() > self.expires_at
    
    def is_valid(self) -> bool:
        """Check if session is valid and active."""
        return (
            self.is_active and 
            not self.is_expired() and 
            self.terminated_at is None
        )
    
    def time_until_expiry(self) -> Optional[timedelta]:
        """Get time until session expires."""
        if not self.expires_at:
            return None
        return self.expires_at - datetime.utcnow()
    
    def duration(self) -> Optional[timedelta]:
        """Get session duration."""
        if not self.created_at:
            return None
        end_time = self.terminated_at or self.last_activity or datetime.utcnow()
        return end_time - self.created_at


@dataclass
class SessionAnalytics:
    """Session analytics data."""
    total_sessions: int
    active_sessions: int
    expired_sessions: int
    terminated_sessions: int
    average_duration: Optional[timedelta]
    unique_users: int
    unique_devices: int
    unique_locations: int
    suspicious_sessions: int
    login_methods: Dict[str, int]
    top_user_agents: List[Dict[str, Any]]
    geographic_distribution: Dict[str, int]


class SessionRepository(BaseRepository[UserSession, str]):
    """Repository for session management operations."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "user_sessions", logger)
        
        # Default session settings
        self.default_session_duration = timedelta(hours=24)
        self.remember_me_duration = timedelta(days=30)
        self.cleanup_interval = timedelta(hours=1)
        self.max_sessions_per_user = 10
        
        # Risk scoring factors
        self.risk_factors = {
            'new_device': 0.3,
            'new_location': 0.4,
            'unusual_time': 0.2,
            'multiple_sessions': 0.1,
            'suspicious_user_agent': 0.5
        }
    
    def _to_entity(self, row: Dict[str, Any]) -> UserSession:
        """Convert database row to UserSession entity."""
        return UserSession(
            id=row.get('id'),
            user_id=row.get('user_id'),
            token=row.get('token', ''),
            device_info=row.get('device_info'),
            ip_address=row.get('ip_address'),
            user_agent=row.get('user_agent'),
            location=row.get('location'),
            created_at=row.get('created_at'),
            last_activity=row.get('last_activity'),
            expires_at=row.get('expires_at'),
            terminated_at=row.get('terminated_at'),
            is_active=row.get('is_active', True),
            is_remember_me=row.get('is_remember_me', False),
            login_method=row.get('login_method', 'password'),
            is_suspicious=row.get('is_suspicious', False),
            risk_score=row.get('risk_score', 0.0),
            security_flags=row.get('security_flags', []),
            session_data=row.get('session_data')
        )
    
    def _to_dict(self, entity: UserSession) -> Dict[str, Any]:
        """Convert UserSession entity to dictionary."""
        return {
            'id': entity.id,
            'user_id': entity.user_id,
            'token': entity.token,
            'device_info': entity.device_info,
            'ip_address': entity.ip_address,
            'user_agent': entity.user_agent,
            'location': entity.location,
            'created_at': entity.created_at,
            'last_activity': entity.last_activity,
            'expires_at': entity.expires_at,
            'terminated_at': entity.terminated_at,
            'is_active': entity.is_active,
            'is_remember_me': entity.is_remember_me,
            'login_method': entity.login_method,
            'is_suspicious': entity.is_suspicious,
            'risk_score': entity.risk_score,
            'security_flags': entity.security_flags,
            'session_data': entity.session_data
        }
    
    def _validate_entity(self, entity: UserSession, is_update: bool = False) -> None:
        """Validate UserSession entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if not entity.token:
            raise ValidationError("Session token is required")
        
        if entity.risk_score < 0 or entity.risk_score > 1:
            raise ValidationError("Risk score must be between 0 and 1")
        
        # Set defaults if not provided
        if not entity.created_at:
            entity.created_at = datetime.utcnow()
        
        if not entity.last_activity:
            entity.last_activity = entity.created_at
        
        if not entity.expires_at:
            duration = self.remember_me_duration if entity.is_remember_me else self.default_session_duration
            entity.expires_at = entity.created_at + duration
        
        if not entity.id:
            entity.id = self._generate_session_id()
    
    def create_session(self, user_id: int, ip_address: Optional[str] = None,
                      user_agent: Optional[str] = None, device_info: Optional[Dict[str, Any]] = None,
                      location: Optional[Dict[str, Any]] = None, is_remember_me: bool = False,
                      login_method: str = "password") -> UserSession:
        """
        Create a new user session.
        
        Args:
            user_id: User ID
            ip_address: Client IP address
            user_agent: User agent string
            device_info: Device information
            location: Geographic location
            is_remember_me: Whether this is a "remember me" session
            login_method: Authentication method used
            
        Returns:
            Created UserSession
        """
        # Generate session token
        session_token = self._generate_session_token()
        
        # Calculate risk score
        risk_score = self._calculate_risk_score(
            user_id=user_id,
            ip_address=ip_address,
            user_agent=user_agent,
            device_info=device_info,
            location=location
        )
        
        # Create session entity
        session = UserSession(
            user_id=user_id,
            token=session_token,
            device_info=device_info,
            ip_address=ip_address,
            user_agent=user_agent,
            location=location,
            is_remember_me=is_remember_me,
            login_method=login_method,
            risk_score=risk_score,
            is_suspicious=risk_score > 0.7  # High risk threshold
        )
        
        # Clean up old sessions for user (enforce max sessions)
        self._cleanup_user_sessions(user_id)
        
        created_session = self.create(session)
        
        self.logger.info(f"Created session for user {user_id}", extra={
            "user_id": user_id,
            "session_id": created_session.id,
            "ip_address": ip_address,
            "risk_score": risk_score,
            "operation": "create_session"
        })
        
        return created_session
    
    def validate_session(self, session_token: str) -> Optional[UserSession]:
        """
        Validate a session token and return the session if valid.
        
        Args:
            session_token: Session token to validate
            
        Returns:
            UserSession if valid, None otherwise
        """
        try:
            session = self.find_one_by(token=session_token)
            if not session:
                return None
            
            # Check if session is valid
            if not session.is_valid():
                # Mark as expired if not already
                if session.is_expired() and session.is_active:
                    self._expire_session(session.id)
                return None
            
            # Update last activity
            self.update_last_activity(session.id)
            
            return session
            
        except Exception as e:
            self.logger.error(f"Failed to validate session: {e}")
            return None
    
    def update_last_activity(self, session_id: str) -> bool:
        """
        Update session's last activity timestamp.
        
        Args:
            session_id: Session ID
            
        Returns:
            True if updated successfully
        """
        try:
            query = f"""
                UPDATE {self.table_name}
                SET last_activity = %(timestamp)s
                WHERE id = %(session_id)s AND is_active = true
            """
            
            params = {
                'timestamp': datetime.utcnow(),
                'session_id': session_id
            }
            
            self.db.execute_query(query, params)
            return self.db.get_affected_rows() > 0
            
        except Exception as e:
            self.logger.error(f"Failed to update last activity for session {session_id}: {e}")
            return False
    
    def terminate_session(self, session_id: str, reason: str = "user_logout") -> bool:
        """
        Terminate a session.
        
        Args:
            session_id: Session ID to terminate
            reason: Reason for termination
            
        Returns:
            True if terminated successfully
        """
        try:
            session = self.get_by_id(session_id)
            if not session:
                return False
            
            session.is_active = False
            session.terminated_at = datetime.utcnow()
            
            # Add termination reason to security flags
            if not session.security_flags:
                session.security_flags = []
            session.security_flags.append(f"terminated:{reason}")
            
            self.update(session)
            
            self.logger.info(f"Terminated session {session_id}", extra={
                "session_id": session_id,
                "user_id": session.user_id,
                "reason": reason,
                "operation": "terminate_session"
            })
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to terminate session {session_id}: {e}")
            return False
    
    def terminate_user_sessions(self, user_id: int, except_session_id: Optional[str] = None,
                               reason: str = "user_action") -> int:
        """
        Terminate all sessions for a user.
        
        Args:
            user_id: User ID
            except_session_id: Session ID to exclude from termination
            reason: Reason for termination
            
        Returns:
            Number of sessions terminated
        """
        try:
            # Get active sessions for user
            sessions = self.get_user_sessions(user_id, active_only=True)
            
            terminated_count = 0
            for session in sessions:
                if except_session_id and session.id == except_session_id:
                    continue
                
                if self.terminate_session(session.id, reason):
                    terminated_count += 1
            
            self.logger.info(f"Terminated {terminated_count} sessions for user {user_id}")
            return terminated_count
            
        except Exception as e:
            self.logger.error(f"Failed to terminate sessions for user {user_id}: {e}")
            return 0
    
    def get_user_sessions(self, user_id: int, active_only: bool = False) -> List[UserSession]:
        """
        Get all sessions for a user.
        
        Args:
            user_id: User ID
            active_only: Whether to return only active sessions
            
        Returns:
            List of user sessions
        """
        filters = {'user_id': user_id}
        if active_only:
            filters['is_active'] = True
        
        options = QueryOptions(
            filters=filters,
            order_by=['-created_at']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_active_sessions(self, limit: Optional[int] = None) -> List[UserSession]:
        """Get all active sessions."""
        options = QueryOptions(
            filters={'is_active': True},
            limit=limit,
            order_by=['-last_activity']
        )
        
        result = self.list_all(options)
        return result.data
    
    def get_suspicious_sessions(self, limit: Optional[int] = None) -> List[UserSession]:
        """Get sessions flagged as suspicious."""
        options = QueryOptions(
            filters={'is_suspicious': True, 'is_active': True},
            limit=limit,
            order_by=['-risk_score', '-created_at']
        )
        
        result = self.list_all(options)
        return result.data
    
    def extend_session(self, session_id: str, additional_time: timedelta = None) -> bool:
        """
        Extend session expiration time.
        
        Args:
            session_id: Session ID
            additional_time: Additional time to add (defaults to default duration)
            
        Returns:
            True if extended successfully
        """
        try:
            session = self.get_by_id(session_id)
            if not session or not session.is_valid():
                return False
            
            if additional_time is None:
                additional_time = self.default_session_duration
            
            session.expires_at = datetime.utcnow() + additional_time
            self.update(session)
            
            self.logger.info(f"Extended session {session_id} by {additional_time}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to extend session {session_id}: {e}")
            return False
    
    def update_session_data(self, session_id: str, data: Dict[str, Any]) -> bool:
        """
        Update session's custom data.
        
        Args:
            session_id: Session ID
            data: Data to store in session
            
        Returns:
            True if updated successfully
        """
        try:
            session = self.get_by_id(session_id)
            if not session or not session.is_valid():
                return False
            
            if not session.session_data:
                session.session_data = {}
            
            session.session_data.update(data)
            self.update(session)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to update session data for {session_id}: {e}")
            return False
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired and terminated sessions.
        
        Returns:
            Number of sessions cleaned up
        """
        try:
            current_time = datetime.utcnow()
            
            # Mark expired sessions as inactive
            expire_query = f"""
                UPDATE {self.table_name}
                SET is_active = false
                WHERE is_active = true 
                AND expires_at < %(current_time)s
            """
            
            self.db.execute_query(expire_query, {'current_time': current_time})
            expired_count = self.db.get_affected_rows()
            
            # Delete old terminated sessions (older than 30 days)
            cleanup_threshold = current_time - timedelta(days=30)
            
            delete_query = f"""
                DELETE FROM {self.table_name}
                WHERE (
                    (is_active = false AND terminated_at < %(threshold)s) OR
                    (expires_at < %(threshold)s)
                )
            """
            
            self.db.execute_query(delete_query, {'threshold': cleanup_threshold})
            deleted_count = self.db.get_affected_rows()
            
            total_cleaned = expired_count + deleted_count
            
            if total_cleaned > 0:
                self.logger.info(f"Cleaned up {total_cleaned} sessions ({expired_count} expired, {deleted_count} deleted)")
            
            return total_cleaned
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup expired sessions: {e}")
            return 0
    
    def generate_session_analytics(self, start_date: datetime, 
                                 end_date: Optional[datetime] = None) -> SessionAnalytics:
        """
        Generate session analytics for a time period.
        
        Args:
            start_date: Start of analysis period
            end_date: End of analysis period (defaults to now)
            
        Returns:
            SessionAnalytics with statistics
        """
        end_date = end_date or datetime.utcnow()
        
        try:
            # Basic counts
            counts_query = f"""
                SELECT 
                    COUNT(*) as total_sessions,
                    COUNT(CASE WHEN is_active = true THEN 1 END) as active_sessions,
                    COUNT(CASE WHEN is_active = false AND expires_at < %(end_date)s THEN 1 END) as expired_sessions,
                    COUNT(CASE WHEN terminated_at IS NOT NULL THEN 1 END) as terminated_sessions,
                    COUNT(DISTINCT user_id) as unique_users,
                    COUNT(CASE WHEN is_suspicious = true THEN 1 END) as suspicious_sessions,
                    AVG(EXTRACT(EPOCH FROM (COALESCE(terminated_at, last_activity) - created_at))) as avg_duration_seconds
                FROM {self.table_name}
                WHERE created_at >= %(start_date)s AND created_at <= %(end_date)s
            """
            
            params = {'start_date': start_date, 'end_date': end_date}
            counts_result = self.db.execute_query(counts_query, params)
            counts = counts_result[0] if counts_result else {}
            
            # Login methods breakdown
            methods_query = f"""
                SELECT login_method, COUNT(*) as count
                FROM {self.table_name}
                WHERE created_at >= %(start_date)s AND created_at <= %(end_date)s
                GROUP BY login_method
                ORDER BY count DESC
            """
            
            methods_result = self.db.execute_query(methods_query, params)
            login_methods = {row['login_method']: row['count'] for row in methods_result} if methods_result else {}
            
            # Top user agents
            agents_query = f"""
                SELECT user_agent, COUNT(*) as count
                FROM {self.table_name}
                WHERE created_at >= %(start_date)s AND created_at <= %(end_date)s
                    AND user_agent IS NOT NULL
                GROUP BY user_agent
                ORDER BY count DESC
                LIMIT 10
            """
            
            agents_result = self.db.execute_query(agents_query, params)
            top_user_agents = [
                {'user_agent': row['user_agent'], 'count': row['count']}
                for row in agents_result
            ] if agents_result else []
            
            # Geographic distribution (if location data available)
            geo_query = f"""
                SELECT 
                    COALESCE(location->>'country', 'Unknown') as country,
                    COUNT(*) as count
                FROM {self.table_name}
                WHERE created_at >= %(start_date)s AND created_at <= %(end_date)s
                GROUP BY location->>'country'
                ORDER BY count DESC
                LIMIT 20
            """
            
            geo_result = self.db.execute_query(geo_query, params)
            geographic_distribution = {row['country']: row['count'] for row in geo_result} if geo_result else {}
            
            # Calculate average duration
            avg_duration = None
            if counts.get('avg_duration_seconds'):
                avg_duration = timedelta(seconds=float(counts['avg_duration_seconds']))
            
            return SessionAnalytics(
                total_sessions=counts.get('total_sessions', 0),
                active_sessions=counts.get('active_sessions', 0),
                expired_sessions=counts.get('expired_sessions', 0),
                terminated_sessions=counts.get('terminated_sessions', 0),
                average_duration=avg_duration,
                unique_users=counts.get('unique_users', 0),
                unique_devices=len(top_user_agents),  # Approximation
                unique_locations=len(geographic_distribution),
                suspicious_sessions=counts.get('suspicious_sessions', 0),
                login_methods=login_methods,
                top_user_agents=top_user_agents,
                geographic_distribution=geographic_distribution
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate session analytics: {e}")
            raise
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        import uuid
        return str(uuid.uuid4())
    
    def _generate_session_token(self) -> str:
        """Generate a secure session token."""
        return secrets.token_urlsafe(64)
    
    def _calculate_risk_score(self, user_id: int, ip_address: Optional[str] = None,
                            user_agent: Optional[str] = None, device_info: Optional[Dict[str, Any]] = None,
                            location: Optional[Dict[str, Any]] = None) -> float:
        """
        Calculate risk score for a session.
        
        Args:
            user_id: User ID
            ip_address: IP address
            user_agent: User agent
            device_info: Device information
            location: Location data
            
        Returns:
            Risk score between 0 and 1
        """
        try:
            risk_score = 0.0
            
            # Check for new device
            if device_info:
                device_fingerprint = self._get_device_fingerprint(device_info)
                known_devices = self._get_user_devices(user_id)
                if device_fingerprint not in known_devices:
                    risk_score += self.risk_factors['new_device']
            
            # Check for new location
            if location and 'country' in location:
                user_countries = self._get_user_countries(user_id)
                if location['country'] not in user_countries:
                    risk_score += self.risk_factors['new_location']
            
            # Check for unusual login time
            if self._is_unusual_login_time(user_id):
                risk_score += self.risk_factors['unusual_time']
            
            # Check for multiple active sessions
            active_sessions = len(self.get_user_sessions(user_id, active_only=True))
            if active_sessions >= 3:
                risk_score += self.risk_factors['multiple_sessions']
            
            # Check for suspicious user agent
            if user_agent and self._is_suspicious_user_agent(user_agent):
                risk_score += self.risk_factors['suspicious_user_agent']
            
            return min(risk_score, 1.0)  # Cap at 1.0
            
        except Exception as e:
            self.logger.error(f"Failed to calculate risk score: {e}")
            return 0.5  # Default medium risk
    
    def _cleanup_user_sessions(self, user_id: int) -> None:
        """Clean up old sessions for a user to enforce max sessions limit."""
        try:
            active_sessions = self.get_user_sessions(user_id, active_only=True)
            
            if len(active_sessions) >= self.max_sessions_per_user:
                # Sort by last activity and terminate oldest sessions
                active_sessions.sort(key=lambda s: s.last_activity or s.created_at)
                
                sessions_to_terminate = active_sessions[:-self.max_sessions_per_user + 1]
                for session in sessions_to_terminate:
                    self.terminate_session(session.id, "max_sessions_exceeded")
                    
        except Exception as e:
            self.logger.error(f"Failed to cleanup user sessions for user {user_id}: {e}")
    
    def _expire_session(self, session_id: str) -> None:
        """Mark a session as expired."""
        try:
            query = f"""
                UPDATE {self.table_name}
                SET is_active = false
                WHERE id = %(session_id)s
            """
            
            self.db.execute_query(query, {'session_id': session_id})
            
        except Exception as e:
            self.logger.error(f"Failed to expire session {session_id}: {e}")
    
    def _get_device_fingerprint(self, device_info: Dict[str, Any]) -> str:
        """Generate device fingerprint from device info."""
        import hashlib
        
        # Create a consistent fingerprint from device characteristics
        fingerprint_data = f"{device_info.get('os', '')}{device_info.get('browser', '')}{device_info.get('screen_resolution', '')}"
        return hashlib.sha256(fingerprint_data.encode()).hexdigest()[:16]
    
    def _get_user_devices(self, user_id: int) -> List[str]:
        """Get known device fingerprints for a user."""
        try:
            query = f"""
                SELECT DISTINCT device_info
                FROM {self.table_name}
                WHERE user_id = %(user_id)s 
                AND device_info IS NOT NULL
                AND created_at > %(since)s
            """
            
            # Look at last 90 days
            since = datetime.utcnow() - timedelta(days=90)
            params = {'user_id': user_id, 'since': since}
            
            result = self.db.execute_query(query, params)
            
            devices = []
            for row in result or []:
                if row['device_info']:
                    fingerprint = self._get_device_fingerprint(row['device_info'])
                    devices.append(fingerprint)
            
            return list(set(devices))  # Remove duplicates
            
        except Exception as e:
            self.logger.error(f"Failed to get user devices for user {user_id}: {e}")
            return []
    
    def _get_user_countries(self, user_id: int) -> List[str]:
        """Get known countries for a user."""
        try:
            query = f"""
                SELECT DISTINCT location->>'country' as country
                FROM {self.table_name}
                WHERE user_id = %(user_id)s 
                AND location IS NOT NULL
                AND created_at > %(since)s
            """
            
            # Look at last 90 days
            since = datetime.utcnow() - timedelta(days=90)
            params = {'user_id': user_id, 'since': since}
            
            result = self.db.execute_query(query, params)
            
            countries = [row['country'] for row in result or [] if row['country']]
            return list(set(countries))  # Remove duplicates
            
        except Exception as e:
            self.logger.error(f"Failed to get user countries for user {user_id}: {e}")
            return []
    
    def _is_unusual_login_time(self, user_id: int) -> bool:
        """Check if current time is unusual for user logins."""
        try:
            current_hour = datetime.utcnow().hour
            
            # Get user's typical login hours
            query = f"""
                SELECT EXTRACT(HOUR FROM created_at) as login_hour, COUNT(*) as count
                FROM {self.table_name}
                WHERE user_id = %(user_id)s 
                AND created_at > %(since)s
                GROUP BY EXTRACT(HOUR FROM created_at)
                ORDER BY count DESC
            """
            
            # Look at last 30 days
            since = datetime.utcnow() - timedelta(days=30)
            params = {'user_id': user_id, 'since': since}
            
            result = self.db.execute_query(query, params)
            
            if not result:
                return False  # No history, can't determine
            
            # Consider unusual if current hour is not in top 50% of login hours
            total_logins = sum(row['count'] for row in result)
            cumulative = 0
            
            for row in result:
                cumulative += row['count']
                if int(row['login_hour']) == current_hour:
                    return cumulative / total_logins > 0.5
            
            return True  # Hour not found in history
            
        except Exception as e:
            self.logger.error(f"Failed to check unusual login time for user {user_id}: {e}")
            return False
    
    def _is_suspicious_user_agent(self, user_agent: str) -> bool:
        """Check if user agent is suspicious."""
        suspicious_patterns = [
            'bot', 'crawler', 'spider', 'scraper',
            'curl', 'wget', 'python-requests',
            'automated', 'headless'
        ]
        
        user_agent_lower = user_agent.lower()
        return any(pattern in user_agent_lower for pattern in suspicious_patterns)


class AsyncSessionRepository(AsyncBaseRepository[UserSession, str]):
    """Async version of SessionRepository."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "user_sessions", logger)
        
        # Default session settings
        self.default_session_duration = timedelta(hours=24)
        self.remember_me_duration = timedelta(days=30)
        self.max_sessions_per_user = 10
    
    def _to_entity(self, row: Dict[str, Any]) -> UserSession:
        """Convert database row to UserSession entity."""
        return UserSession(
            id=row.get('id'),
            user_id=row.get('user_id'),
            token=row.get('token', ''),
            device_info=row.get('device_info'),
            ip_address=row.get('ip_address'),
            user_agent=row.get('user_agent'),
            location=row.get('location'),
            created_at=row.get('created_at'),
            last_activity=row.get('last_activity'),
            expires_at=row.get('expires_at'),
            terminated_at=row.get('terminated_at'),
            is_active=row.get('is_active', True),
            is_remember_me=row.get('is_remember_me', False),
            login_method=row.get('login_method', 'password'),
            is_suspicious=row.get('is_suspicious', False),
            risk_score=row.get('risk_score', 0.0),
            security_flags=row.get('security_flags', []),
            session_data=row.get('session_data')
        )
    
    def _to_dict(self, entity: UserSession) -> Dict[str, Any]:
        """Convert UserSession entity to dictionary."""
        return {
            'id': entity.id,
            'user_id': entity.user_id,
            'token': entity.token,
            'device_info': entity.device_info,
            'ip_address': entity.ip_address,
            'user_agent': entity.user_agent,
            'location': entity.location,
            'created_at': entity.created_at,
            'last_activity': entity.last_activity,
            'expires_at': entity.expires_at,
            'terminated_at': entity.terminated_at,
            'is_active': entity.is_active,
            'is_remember_me': entity.is_remember_me,
            'login_method': entity.login_method,
            'is_suspicious': entity.is_suspicious,
            'risk_score': entity.risk_score,
            'security_flags': entity.security_flags,
            'session_data': entity.session_data
        }
    
    async def _validate_entity(self, entity: UserSession, is_update: bool = False) -> None:
        """Async validate UserSession entity."""
        if not entity.user_id:
            raise ValidationError("User ID is required")
        
        if not entity.token:
            raise ValidationError("Session token is required")
        
        if entity.risk_score < 0 or entity.risk_score > 1:
            raise ValidationError("Risk score must be between 0 and 1")
        
        # Set defaults if not provided
        if not entity.created_at:
            entity.created_at = datetime.utcnow()
        
        if not entity.last_activity:
            entity.last_activity = entity.created_at
        
        if not entity.expires_at:
            duration = self.remember_me_duration if entity.is_remember_me else self.default_session_duration
            entity.expires_at = entity.created_at + duration
        
        if not entity.id:
            entity.id = self._generate_session_id()
    
    async def validate_session(self, session_token: str) -> Optional[UserSession]:
        """Async validate session token."""
        try:
            session = await self.find_one_by_async(token=session_token)
            if not session:
                return None
            
            # Check if session is valid
            if not session.is_valid():
                return None
            
            # Update last activity
            await self.update_last_activity_async(session.id)
            
            return session
            
        except Exception as e:
            self.logger.error(f"Failed to validate session: {e}")
            return None
    
    def _generate_session_id(self) -> str:
        """Generate a unique session ID."""
        import uuid
        return str(uuid.uuid4())
