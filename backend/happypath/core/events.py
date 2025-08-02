"""
Event management system for the Happy Path platform.
Provides event-driven architecture with pub/sub capabilities.
"""

import asyncio
import json
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Callable, Awaitable, Union
from dataclasses import dataclass, asdict
from enum import Enum
import uuid
import threading
from collections import defaultdict

from .config import get_config
from .logging import get_logger
from .database import execute_query
from .cache import get_cache_manager
from .exceptions import HappyPathError

logger = get_logger(__name__)


class EventType(Enum):
    """System event types."""
    # User events
    USER_REGISTERED = "user_registered"
    USER_LOGIN = "user_login"
    USER_LOGOUT = "user_logout"
    USER_PROFILE_UPDATED = "user_profile_updated"
    
    # Subscription events
    SUBSCRIPTION_CREATED = "subscription_created"
    SUBSCRIPTION_UPDATED = "subscription_updated"
    SUBSCRIPTION_CANCELLED = "subscription_cancelled"
    PAYMENT_PROCESSED = "payment_processed"
    PAYMENT_FAILED = "payment_failed"
    
    # Health events
    MOOD_ENTRY_CREATED = "mood_entry_created"
    JOURNAL_ENTRY_CREATED = "journal_entry_created"
    ASSESSMENT_COMPLETED = "assessment_completed"
    
    # Crisis events
    CRISIS_DETECTED = "crisis_detected"
    CRISIS_ESCALATED = "crisis_escalated"
    CRISIS_RESOLVED = "crisis_resolved"
    
    # Provider events
    PROVIDER_MESSAGE_SENT = "provider_message_sent"
    APPOINTMENT_SCHEDULED = "appointment_scheduled"
    APPOINTMENT_CANCELLED = "appointment_cancelled"
    
    # System events
    SYSTEM_MAINTENANCE_START = "system_maintenance_start"
    SYSTEM_MAINTENANCE_END = "system_maintenance_end"
    BACKUP_COMPLETED = "backup_completed"
    HEALTH_CHECK_FAILED = "health_check_failed"


@dataclass
class Event:
    """Event data structure."""
    event_id: str
    event_type: EventType
    source: str
    timestamp: datetime
    data: Dict[str, Any]
    user_id: Optional[str] = None
    correlation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class EventHandler:
    """Base class for event handlers."""
    
    def __init__(self, name: str):
        self.name = name
    
    async def handle(self, event: Event) -> bool:
        """Handle an event. Return True if handled successfully."""
        raise NotImplementedError
    
    def can_handle(self, event_type: EventType) -> bool:
        """Check if this handler can handle the event type."""
        return True


class EventManager:
    """Central event management system."""
    
    def __init__(self):
        self.config = get_config()
        self.cache = get_cache_manager()
        self._handlers: Dict[EventType, List[EventHandler]] = defaultdict(list)
        self._async_handlers: Dict[EventType, List[Callable]] = defaultdict(list)
        self._sync_handlers: Dict[EventType, List[Callable]] = defaultdict(list)
        self._event_store_enabled = True
        self._lock = threading.Lock()
    
    def register_handler(self, event_type: EventType, handler: Union[EventHandler, Callable]):
        """Register an event handler."""
        with self._lock:
            if isinstance(handler, EventHandler):
                self._handlers[event_type].append(handler)
            elif asyncio.iscoroutinefunction(handler):
                self._async_handlers[event_type].append(handler)
            else:
                self._sync_handlers[event_type].append(handler)
        
        logger.info(f"Event handler registered for {event_type.value}")
    
    def unregister_handler(self, event_type: EventType, handler: Union[EventHandler, Callable]):
        """Unregister an event handler."""
        with self._lock:
            if isinstance(handler, EventHandler):
                if handler in self._handlers[event_type]:
                    self._handlers[event_type].remove(handler)
            elif asyncio.iscoroutinefunction(handler):
                if handler in self._async_handlers[event_type]:
                    self._async_handlers[event_type].remove(handler)
            else:
                if handler in self._sync_handlers[event_type]:
                    self._sync_handlers[event_type].remove(handler)
        
        logger.info(f"Event handler unregistered for {event_type.value}")
    
    async def publish_async(
        self,
        event_type: EventType,
        data: Dict[str, Any],
        source: str,
        user_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Publish an event asynchronously."""
        event = Event(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            source=source,
            timestamp=datetime.now(timezone.utc),
            data=data,
            user_id=user_id,
            correlation_id=correlation_id,
            metadata=metadata or {}
        )
        
        # Store event if enabled
        if self._event_store_enabled:
            await self._store_event(event)
        
        # Handle event
        await self._handle_event_async(event)
        
        logger.debug(f"Event published: {event_type.value} - {event.event_id}")
        return event.event_id
    
    def publish(
        self,
        event_type: EventType,
        data: Dict[str, Any],
        source: str,
        user_id: Optional[str] = None,
        correlation_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Publish an event synchronously."""
        event = Event(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            source=source,
            timestamp=datetime.now(timezone.utc),
            data=data,
            user_id=user_id,
            correlation_id=correlation_id,
            metadata=metadata or {}
        )
        
        # Store event if enabled
        if self._event_store_enabled:
            self._store_event_sync(event)
        
        # Handle event synchronously
        self._handle_event_sync(event)
        
        logger.debug(f"Event published: {event_type.value} - {event.event_id}")
        return event.event_id
    
    async def _handle_event_async(self, event: Event):
        """Handle event with async handlers."""
        try:
            # Run object-based handlers
            for handler in self._handlers[event.event_type]:
                try:
                    await handler.handle(event)
                except Exception as e:
                    logger.error(f"Event handler {handler.name} failed: {e}")
            
            # Run async function handlers
            for handler in self._async_handlers[event.event_type]:
                try:
                    await handler(event)
                except Exception as e:
                    logger.error(f"Async event handler failed: {e}")
            
            # Run sync function handlers in thread pool
            for handler in self._sync_handlers[event.event_type]:
                try:
                    await asyncio.get_event_loop().run_in_executor(None, handler, event)
                except Exception as e:
                    logger.error(f"Sync event handler failed: {e}")
                    
        except Exception as e:
            logger.error(f"Event handling failed for {event.event_type.value}: {e}")
    
    def _handle_event_sync(self, event: Event):
        """Handle event with sync handlers only."""
        try:
            # Run sync function handlers
            for handler in self._sync_handlers[event.event_type]:
                try:
                    handler(event)
                except Exception as e:
                    logger.error(f"Sync event handler failed: {e}")
                    
        except Exception as e:
            logger.error(f"Sync event handling failed for {event.event_type.value}: {e}")
    
    async def _store_event(self, event: Event):
        """Store event in database asynchronously."""
        try:
            query = """
                INSERT INTO event_log (
                    event_id, event_type, source, timestamp, data, 
                    user_id, correlation_id, metadata
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Use thread pool for database operation
            await asyncio.get_event_loop().run_in_executor(
                None,
                execute_query,
                query,
                (
                    event.event_id,
                    event.event_type.value,
                    event.source,
                    event.timestamp,
                    json.dumps(event.data),
                    event.user_id,
                    event.correlation_id,
                    json.dumps(event.metadata) if event.metadata else None
                ),
                False,
                False
            )
            
        except Exception as e:
            logger.error(f"Failed to store event {event.event_id}: {e}")
    
    def _store_event_sync(self, event: Event):
        """Store event in database synchronously."""
        try:
            query = """
                INSERT INTO event_log (
                    event_id, event_type, source, timestamp, data, 
                    user_id, correlation_id, metadata
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            execute_query(
                query,
                (
                    event.event_id,
                    event.event_type.value,
                    event.source,
                    event.timestamp,
                    json.dumps(event.data),
                    event.user_id,
                    event.correlation_id,
                    json.dumps(event.metadata) if event.metadata else None
                ),
                fetch_all=False
            )
            
        except Exception as e:
            logger.error(f"Failed to store event {event.event_id}: {e}")
    
    def get_events(
        self,
        event_types: Optional[List[EventType]] = None,
        user_id: Optional[str] = None,
        source: Optional[str] = None,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get events from the event store."""
        try:
            where_conditions = []
            params = []
            
            if event_types:
                placeholders = ', '.join(['%s'] * len(event_types))
                where_conditions.append(f"event_type IN ({placeholders})")
                params.extend([et.value for et in event_types])
            
            if user_id:
                where_conditions.append("user_id = %s")
                params.append(user_id)
            
            if source:
                where_conditions.append("source = %s")
                params.append(source)
            
            if start_date:
                where_conditions.append("timestamp >= %s")
                params.append(start_date)
            
            if end_date:
                where_conditions.append("timestamp <= %s")
                params.append(end_date)
            
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            
            query = f"""
                SELECT event_id, event_type, source, timestamp, data, 
                       user_id, correlation_id, metadata
                FROM event_log
                WHERE {where_clause}
                ORDER BY timestamp DESC
                LIMIT %s
            """
            
            params.append(limit)
            return execute_query(query, params)
            
        except Exception as e:
            logger.error(f"Failed to get events: {e}")
            return []
    
    def get_event_stats(self, hours: int = 24) -> Dict[str, Any]:
        """Get event statistics."""
        try:
            start_time = datetime.now(timezone.utc) - timedelta(hours=hours)
            
            query = """
                SELECT 
                    event_type,
                    COUNT(*) as count,
                    MIN(timestamp) as first_event,
                    MAX(timestamp) as last_event
                FROM event_log
                WHERE timestamp >= %s
                GROUP BY event_type
                ORDER BY count DESC
            """
            
            results = execute_query(query, (start_time,))
            
            total_events = sum(row['count'] for row in results)
            
            return {
                "period_hours": hours,
                "total_events": total_events,
                "event_types": results,
                "generated_at": datetime.now(timezone.utc)
            }
            
        except Exception as e:
            logger.error(f"Failed to get event stats: {e}")
            return {"error": str(e)}


class NotificationHandler(EventHandler):
    """Handler for sending notifications based on events."""
    
    def __init__(self):
        super().__init__("notification_handler")
        self.notification_events = {
            EventType.CRISIS_DETECTED,
            EventType.PAYMENT_FAILED,
            EventType.APPOINTMENT_SCHEDULED,
            EventType.PROVIDER_MESSAGE_SENT
        }
    
    async def handle(self, event: Event) -> bool:
        """Handle notification events."""
        if event.event_type not in self.notification_events:
            return True
        
        try:
            if event.event_type == EventType.CRISIS_DETECTED:
                await self._handle_crisis_notification(event)
            elif event.event_type == EventType.PAYMENT_FAILED:
                await self._handle_payment_failed_notification(event)
            elif event.event_type == EventType.APPOINTMENT_SCHEDULED:
                await self._handle_appointment_notification(event)
            elif event.event_type == EventType.PROVIDER_MESSAGE_SENT:
                await self._handle_provider_message_notification(event)
            
            return True
            
        except Exception as e:
            logger.error(f"Notification handler failed: {e}")
            return False
    
    async def _handle_crisis_notification(self, event: Event):
        """Handle crisis detection notifications."""
        # Send immediate alerts to emergency contacts
        user_id = event.user_id
        crisis_level = event.data.get("crisis_level", "medium")
        
        logger.info(f"Crisis detected for user {user_id}, level: {crisis_level}")
        
        # TODO: Implement actual notification sending
        # - Send SMS to emergency contacts
        # - Email crisis support team
        # - Create urgent support ticket
    
    async def _handle_payment_failed_notification(self, event: Event):
        """Handle payment failure notifications."""
        user_id = event.user_id
        amount = event.data.get("amount", 0)
        
        logger.info(f"Payment failed for user {user_id}, amount: ${amount}")
        
        # TODO: Implement payment failure notifications
        # - Email user about failed payment
        # - Schedule retry attempt
        # - Update subscription status if needed
    
    async def _handle_appointment_notification(self, event: Event):
        """Handle appointment notifications."""
        user_id = event.user_id
        appointment_time = event.data.get("appointment_time")
        
        logger.info(f"Appointment scheduled for user {user_id} at {appointment_time}")
        
        # TODO: Implement appointment notifications
        # - Send confirmation email
        # - Schedule reminder notifications
        # - Update calendar
    
    async def _handle_provider_message_notification(self, event: Event):
        """Handle provider message notifications."""
        recipient_id = event.data.get("recipient_id")
        sender_name = event.data.get("sender_name", "Healthcare Provider")
        
        logger.info(f"Provider message sent to user {recipient_id} from {sender_name}")
        
        # TODO: Implement provider message notifications
        # - Send push notification
        # - Email notification (if enabled)
        # - Update unread message count


class AuditEventHandler(EventHandler):
    """Handler for auditing significant events."""
    
    def __init__(self):
        super().__init__("audit_event_handler")
        self.audit_events = {
            EventType.USER_LOGIN,
            EventType.USER_LOGOUT,
            EventType.PAYMENT_PROCESSED,
            EventType.CRISIS_DETECTED,
            EventType.SUBSCRIPTION_CREATED
        }
    
    async def handle(self, event: Event) -> bool:
        """Handle audit events."""
        if event.event_type not in self.audit_events:
            return True
        
        try:
            from .auditing import get_audit_logger, AuditEventType, AuditSeverity
            
            audit_logger = get_audit_logger()
            
            # Map event types to audit event types
            audit_type_mapping = {
                EventType.USER_LOGIN: AuditEventType.USER_LOGIN,
                EventType.USER_LOGOUT: AuditEventType.USER_LOGOUT,
                EventType.PAYMENT_PROCESSED: AuditEventType.PAYMENT_PROCESSED,
                EventType.CRISIS_DETECTED: AuditEventType.CRISIS_DETECTED,
                EventType.SUBSCRIPTION_CREATED: AuditEventType.SUBSCRIPTION_CREATED
            }
            
            audit_type = audit_type_mapping.get(event.event_type)
            if audit_type:
                audit_logger.log_event(
                    event_type=audit_type,
                    user_id=event.user_id,
                    description=f"Event: {event.event_type.value}",
                    details=event.data,
                    severity=AuditSeverity.MEDIUM
                )
            
            return True
            
        except Exception as e:
            logger.error(f"Audit event handler failed: {e}")
            return False


# Global instance
_event_manager: Optional[EventManager] = None


def get_event_manager() -> EventManager:
    """Get the global event manager instance."""
    global _event_manager
    if _event_manager is None:
        _event_manager = EventManager()
        
        # Register default handlers
        _event_manager.register_handler(EventType.CRISIS_DETECTED, NotificationHandler())
        _event_manager.register_handler(EventType.PAYMENT_FAILED, NotificationHandler())
        _event_manager.register_handler(EventType.USER_LOGIN, AuditEventHandler())
        
    return _event_manager


# Convenience functions
async def publish_event(
    event_type: EventType,
    data: Dict[str, Any],
    source: str,
    user_id: Optional[str] = None,
    correlation_id: Optional[str] = None
) -> str:
    """Publish an event asynchronously."""
    return await get_event_manager().publish_async(
        event_type, data, source, user_id, correlation_id
    )


def publish_event_sync(
    event_type: EventType,
    data: Dict[str, Any],
    source: str,
    user_id: Optional[str] = None,
    correlation_id: Optional[str] = None
) -> str:
    """Publish an event synchronously."""
    return get_event_manager().publish(
        event_type, data, source, user_id, correlation_id
    )


def event_handler(event_type: EventType):
    """Decorator for registering event handlers."""
    def decorator(func: Callable):
        get_event_manager().register_handler(event_type, func)
        return func
    return decorator


# Event helpers for common use cases
async def user_registered_event(user_id: str, email: str, source: str = "auth_service"):
    """Publish user registration event."""
    await publish_event(
        EventType.USER_REGISTERED,
        {"email": email, "registration_source": source},
        source,
        user_id
    )


async def crisis_detected_event(user_id: str, crisis_level: str, details: Dict[str, Any], source: str = "crisis_service"):
    """Publish crisis detection event."""
    await publish_event(
        EventType.CRISIS_DETECTED,
        {"crisis_level": crisis_level, **details},
        source,
        user_id
    )


async def payment_processed_event(user_id: str, amount: float, currency: str, payment_method: str, source: str = "payment_service"):
    """Publish payment processed event."""
    await publish_event(
        EventType.PAYMENT_PROCESSED,
        {
            "amount": amount,
            "currency": currency,
            "payment_method": payment_method
        },
        source,
        user_id
    )
