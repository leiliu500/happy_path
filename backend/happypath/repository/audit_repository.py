"""
Audit Repository

Repository implementation for audit logging and compliance tracking.
Handles audit trail creation, querying, and compliance reporting.
"""

from typing import List, Optional, Dict, Any, Union
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import json
import logging

from .base_repository import BaseRepository, AsyncBaseRepository, QueryOptions, QueryResult
from .base_repository import ValidationError, NotFoundError


class AuditAction(Enum):
    """Enumeration of audit actions."""
    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    LOGIN = "login"
    LOGOUT = "logout"
    PERMISSION_GRANTED = "permission_granted"
    PERMISSION_DENIED = "permission_denied"
    DATA_EXPORT = "data_export"
    DATA_IMPORT = "data_import"
    CONFIGURATION_CHANGE = "configuration_change"
    SECURITY_EVENT = "security_event"
    ERROR = "error"
    WARNING = "warning"


class AuditLevel(Enum):
    """Audit severity levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class AuditEntry:
    """Audit log entry representation."""
    id: Optional[int] = None
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    action: str = ""
    resource_type: str = ""
    resource_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    old_values: Optional[Dict[str, Any]] = None
    new_values: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: Optional[datetime] = None
    level: str = AuditLevel.LOW.value
    success: bool = True
    error_message: Optional[str] = None
    
    # Compliance and tracking
    compliance_category: Optional[str] = None
    retention_until: Optional[datetime] = None
    is_sensitive: bool = False
    
    # Metadata
    created_at: Optional[datetime] = None


@dataclass
class AuditQuery:
    """Query parameters for audit searches."""
    user_id: Optional[int] = None
    session_id: Optional[str] = None
    action: Optional[str] = None
    resource_type: Optional[str] = None
    resource_id: Optional[str] = None
    level: Optional[str] = None
    success: Optional[bool] = None
    ip_address: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    compliance_category: Optional[str] = None
    is_sensitive: Optional[bool] = None
    
    # Pagination
    limit: Optional[int] = None
    offset: Optional[int] = None
    order_by: Optional[List[str]] = None


@dataclass
class AuditSummary:
    """Summary statistics for audit data."""
    total_entries: int
    unique_users: int
    unique_sessions: int
    actions_breakdown: Dict[str, int]
    level_breakdown: Dict[str, int]
    success_rate: float
    time_period: Dict[str, datetime]
    most_active_users: List[Dict[str, Any]]
    recent_critical_events: List[AuditEntry]


class AuditRepository(BaseRepository[AuditEntry, int]):
    """Repository for audit logging operations."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "audit_logs", logger)
        
        # Default retention periods by compliance category
        self.retention_periods = {
            'security': timedelta(days=2555),  # 7 years
            'financial': timedelta(days=2555),  # 7 years
            'medical': timedelta(days=2190),    # 6 years
            'general': timedelta(days=1095),    # 3 years
            'system': timedelta(days=365),      # 1 year
            'debug': timedelta(days=30)         # 30 days
        }
    
    def _to_entity(self, row: Dict[str, Any]) -> AuditEntry:
        """Convert database row to AuditEntry entity."""
        return AuditEntry(
            id=row.get('id'),
            user_id=row.get('user_id'),
            session_id=row.get('session_id'),
            action=row.get('action', ''),
            resource_type=row.get('resource_type', ''),
            resource_id=row.get('resource_id'),
            details=row.get('details'),
            old_values=row.get('old_values'),
            new_values=row.get('new_values'),
            ip_address=row.get('ip_address'),
            user_agent=row.get('user_agent'),
            timestamp=row.get('timestamp'),
            level=row.get('level', AuditLevel.LOW.value),
            success=row.get('success', True),
            error_message=row.get('error_message'),
            compliance_category=row.get('compliance_category'),
            retention_until=row.get('retention_until'),
            is_sensitive=row.get('is_sensitive', False),
            created_at=row.get('created_at')
        )
    
    def _to_dict(self, entity: AuditEntry) -> Dict[str, Any]:
        """Convert AuditEntry entity to dictionary."""
        return {
            'id': entity.id,
            'user_id': entity.user_id,
            'session_id': entity.session_id,
            'action': entity.action,
            'resource_type': entity.resource_type,
            'resource_id': entity.resource_id,
            'details': entity.details,
            'old_values': entity.old_values,
            'new_values': entity.new_values,
            'ip_address': entity.ip_address,
            'user_agent': entity.user_agent,
            'timestamp': entity.timestamp,
            'level': entity.level,
            'success': entity.success,
            'error_message': entity.error_message,
            'compliance_category': entity.compliance_category,
            'retention_until': entity.retention_until,
            'is_sensitive': entity.is_sensitive,
            'created_at': entity.created_at
        }
    
    def _validate_entity(self, entity: AuditEntry, is_update: bool = False) -> None:
        """Validate AuditEntry entity."""
        if not entity.action:
            raise ValidationError("Action is required")
        
        if not entity.resource_type:
            raise ValidationError("Resource type is required")
        
        if entity.level not in [level.value for level in AuditLevel]:
            raise ValidationError(f"Invalid audit level: {entity.level}")
        
        # Set default timestamp if not provided
        if not entity.timestamp:
            entity.timestamp = datetime.utcnow()
        
        # Set retention period if not provided
        if not entity.retention_until and entity.compliance_category:
            retention_period = self.retention_periods.get(
                entity.compliance_category, 
                self.retention_periods['general']
            )
            entity.retention_until = entity.timestamp + retention_period
    
    def log_audit_event(self, user_id: Optional[int], action: str, resource_type: str,
                       resource_id: Optional[str] = None, details: Optional[Dict[str, Any]] = None,
                       old_values: Optional[Dict[str, Any]] = None, 
                       new_values: Optional[Dict[str, Any]] = None,
                       ip_address: Optional[str] = None, user_agent: Optional[str] = None,
                       session_id: Optional[str] = None, level: str = AuditLevel.LOW.value,
                       success: bool = True, error_message: Optional[str] = None,
                       compliance_category: str = "general", is_sensitive: bool = False) -> AuditEntry:
        """
        Log an audit event.
        
        Args:
            user_id: ID of the user performing the action
            action: Action being performed
            resource_type: Type of resource being acted upon
            resource_id: ID of the specific resource
            details: Additional details about the action
            old_values: Previous values (for updates)
            new_values: New values (for updates)
            ip_address: IP address of the user
            user_agent: User agent string
            session_id: Session identifier
            level: Audit level (low, medium, high, critical)
            success: Whether the action was successful
            error_message: Error message if action failed
            compliance_category: Compliance category for retention
            is_sensitive: Whether this contains sensitive data
            
        Returns:
            Created AuditEntry
        """
        audit_entry = AuditEntry(
            user_id=user_id,
            session_id=session_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            old_values=old_values,
            new_values=new_values,
            ip_address=ip_address,
            user_agent=user_agent,
            timestamp=datetime.utcnow(),
            level=level,
            success=success,
            error_message=error_message,
            compliance_category=compliance_category,
            is_sensitive=is_sensitive
        )
        
        return self.create(audit_entry)
    
    def log_user_action(self, user_id: int, action: str, resource_type: str,
                       resource_id: Optional[str] = None, **kwargs) -> AuditEntry:
        """Log a user action (convenience method)."""
        return self.log_audit_event(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            **kwargs
        )
    
    def log_system_event(self, action: str, resource_type: str, 
                        details: Optional[Dict[str, Any]] = None, **kwargs) -> AuditEntry:
        """Log a system event (convenience method)."""
        return self.log_audit_event(
            user_id=None,
            action=action,
            resource_type=resource_type,
            details=details,
            compliance_category="system",
            **kwargs
        )
    
    def log_security_event(self, action: str, user_id: Optional[int] = None,
                          ip_address: Optional[str] = None, details: Optional[Dict[str, Any]] = None,
                          success: bool = True, **kwargs) -> AuditEntry:
        """Log a security event (convenience method)."""
        return self.log_audit_event(
            user_id=user_id,
            action=action,
            resource_type="security",
            ip_address=ip_address,
            details=details,
            level=AuditLevel.HIGH.value,
            success=success,
            compliance_category="security",
            **kwargs
        )
    
    def query_audit_logs(self, query: AuditQuery) -> QueryResult:
        """
        Query audit logs with filters.
        
        Args:
            query: AuditQuery with filter parameters
            
        Returns:
            QueryResult with matching audit entries
        """
        try:
            # Build filters
            filters = {}
            if query.user_id is not None:
                filters['user_id'] = query.user_id
            if query.session_id:
                filters['session_id'] = query.session_id
            if query.action:
                filters['action'] = query.action
            if query.resource_type:
                filters['resource_type'] = query.resource_type
            if query.resource_id:
                filters['resource_id'] = query.resource_id
            if query.level:
                filters['level'] = query.level
            if query.success is not None:
                filters['success'] = query.success
            if query.ip_address:
                filters['ip_address'] = query.ip_address
            if query.compliance_category:
                filters['compliance_category'] = query.compliance_category
            if query.is_sensitive is not None:
                filters['is_sensitive'] = query.is_sensitive
            
            # Handle time range filtering
            where_conditions = []
            params = {}
            
            if query.start_time:
                where_conditions.append("timestamp >= %(start_time)s")
                params['start_time'] = query.start_time
            
            if query.end_time:
                where_conditions.append("timestamp <= %(end_time)s")
                params['end_time'] = query.end_time
            
            # Build main query
            query_parts = [f"SELECT * FROM {self.table_name}"]
            
            # Add basic filters
            if filters:
                filter_conditions = []
                for key, value in filters.items():
                    filter_conditions.append(f"{key} = %({key})s")
                    params[key] = value
                where_conditions.extend(filter_conditions)
            
            if where_conditions:
                query_parts.append(f"WHERE {' AND '.join(where_conditions)}")
            
            # Add ordering
            order_by = query.order_by or ['-timestamp']  # Default to newest first
            order_clauses = []
            for order_field in order_by:
                if order_field.startswith('-'):
                    order_clauses.append(f"{order_field[1:]} DESC")
                else:
                    order_clauses.append(f"{order_field} ASC")
            query_parts.append(f"ORDER BY {', '.join(order_clauses)}")
            
            # Get total count
            count_query = f"SELECT COUNT(*) as count FROM {self.table_name}"
            if where_conditions:
                count_query += f" WHERE {' AND '.join(where_conditions)}"
            
            count_result = self.db.execute_query(count_query, params)
            total_count = count_result[0]['count'] if count_result else 0
            
            # Add pagination
            if query.limit:
                query_parts.append(f"LIMIT %(limit)s")
                params['limit'] = query.limit
                
                if query.offset:
                    query_parts.append(f"OFFSET %(offset)s")
                    params['offset'] = query.offset
            
            # Execute query
            sql_query = ' '.join(query_parts)
            result = self.db.execute_query(sql_query, params)
            
            # Convert to entities
            entries = [self._to_entity(row) for row in result] if result else []
            
            # Calculate pagination metadata
            page = None
            page_size = None
            has_next = False
            has_previous = False
            
            if query.limit and query.offset is not None:
                page_size = query.limit
                page = (query.offset // query.limit) + 1
                has_previous = query.offset > 0
                has_next = (query.offset + query.limit) < total_count
            
            return QueryResult(
                data=entries,
                total_count=total_count,
                page=page,
                page_size=page_size,
                has_next=has_next,
                has_previous=has_previous
            )
            
        except Exception as e:
            self.logger.error(f"Failed to query audit logs: {e}")
            raise
    
    def get_user_audit_trail(self, user_id: int, start_time: Optional[datetime] = None,
                           end_time: Optional[datetime] = None, limit: int = 100) -> List[AuditEntry]:
        """
        Get audit trail for a specific user.
        
        Args:
            user_id: User ID to get audit trail for
            start_time: Start of time range
            end_time: End of time range
            limit: Maximum number of entries
            
        Returns:
            List of audit entries for the user
        """
        query = AuditQuery(
            user_id=user_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
            order_by=['-timestamp']
        )
        
        result = self.query_audit_logs(query)
        return result.data
    
    def get_resource_audit_trail(self, resource_type: str, resource_id: str,
                               start_time: Optional[datetime] = None,
                               end_time: Optional[datetime] = None, 
                               limit: int = 100) -> List[AuditEntry]:
        """
        Get audit trail for a specific resource.
        
        Args:
            resource_type: Type of resource
            resource_id: ID of the resource
            start_time: Start of time range
            end_time: End of time range
            limit: Maximum number of entries
            
        Returns:
            List of audit entries for the resource
        """
        query = AuditQuery(
            resource_type=resource_type,
            resource_id=resource_id,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
            order_by=['-timestamp']
        )
        
        result = self.query_audit_logs(query)
        return result.data
    
    def get_security_events(self, start_time: Optional[datetime] = None,
                          end_time: Optional[datetime] = None,
                          success: Optional[bool] = None, limit: int = 100) -> List[AuditEntry]:
        """
        Get security-related audit events.
        
        Args:
            start_time: Start of time range
            end_time: End of time range
            success: Filter by success status
            limit: Maximum number of entries
            
        Returns:
            List of security audit entries
        """
        query = AuditQuery(
            compliance_category="security",
            start_time=start_time,
            end_time=end_time,
            success=success,
            limit=limit,
            order_by=['-timestamp']
        )
        
        result = self.query_audit_logs(query)
        return result.data
    
    def get_failed_actions(self, start_time: Optional[datetime] = None,
                         end_time: Optional[datetime] = None, limit: int = 100) -> List[AuditEntry]:
        """
        Get failed actions from audit logs.
        
        Args:
            start_time: Start of time range
            end_time: End of time range
            limit: Maximum number of entries
            
        Returns:
            List of failed audit entries
        """
        query = AuditQuery(
            success=False,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
            order_by=['-timestamp']
        )
        
        result = self.query_audit_logs(query)
        return result.data
    
    def get_critical_events(self, start_time: Optional[datetime] = None,
                          end_time: Optional[datetime] = None, limit: int = 100) -> List[AuditEntry]:
        """
        Get critical audit events.
        
        Args:
            start_time: Start of time range
            end_time: End of time range
            limit: Maximum number of entries
            
        Returns:
            List of critical audit entries
        """
        query = AuditQuery(
            level=AuditLevel.CRITICAL.value,
            start_time=start_time,
            end_time=end_time,
            limit=limit,
            order_by=['-timestamp']
        )
        
        result = self.query_audit_logs(query)
        return result.data
    
    def generate_audit_summary(self, start_time: datetime, end_time: datetime) -> AuditSummary:
        """
        Generate audit summary for a time period.
        
        Args:
            start_time: Start of analysis period
            end_time: End of analysis period
            
        Returns:
            AuditSummary with statistics
        """
        try:
            # Get basic counts
            base_query = f"""
                SELECT 
                    COUNT(*) as total_entries,
                    COUNT(DISTINCT user_id) as unique_users,
                    COUNT(DISTINCT session_id) as unique_sessions,
                    AVG(CASE WHEN success THEN 1.0 ELSE 0.0 END) as success_rate
                FROM {self.table_name}
                WHERE timestamp >= %(start_time)s AND timestamp <= %(end_time)s
            """
            
            params = {'start_time': start_time, 'end_time': end_time}
            result = self.db.execute_query(base_query, params)
            basic_stats = result[0] if result else {}
            
            # Get actions breakdown
            actions_query = f"""
                SELECT action, COUNT(*) as count
                FROM {self.table_name}
                WHERE timestamp >= %(start_time)s AND timestamp <= %(end_time)s
                GROUP BY action
                ORDER BY count DESC
            """
            
            actions_result = self.db.execute_query(actions_query, params)
            actions_breakdown = {row['action']: row['count'] for row in actions_result} if actions_result else {}
            
            # Get level breakdown
            level_query = f"""
                SELECT level, COUNT(*) as count
                FROM {self.table_name}
                WHERE timestamp >= %(start_time)s AND timestamp <= %(end_time)s
                GROUP BY level
                ORDER BY count DESC
            """
            
            level_result = self.db.execute_query(level_query, params)
            level_breakdown = {row['level']: row['count'] for row in level_result} if level_result else {}
            
            # Get most active users
            users_query = f"""
                SELECT user_id, COUNT(*) as action_count
                FROM {self.table_name}
                WHERE timestamp >= %(start_time)s AND timestamp <= %(end_time)s
                    AND user_id IS NOT NULL
                GROUP BY user_id
                ORDER BY action_count DESC
                LIMIT 10
            """
            
            users_result = self.db.execute_query(users_query, params)
            most_active_users = [
                {'user_id': row['user_id'], 'action_count': row['action_count']}
                for row in users_result
            ] if users_result else []
            
            # Get recent critical events
            critical_query = AuditQuery(
                level=AuditLevel.CRITICAL.value,
                start_time=start_time,
                end_time=end_time,
                limit=10,
                order_by=['-timestamp']
            )
            
            critical_result = self.query_audit_logs(critical_query)
            recent_critical_events = critical_result.data
            
            return AuditSummary(
                total_entries=basic_stats.get('total_entries', 0),
                unique_users=basic_stats.get('unique_users', 0),
                unique_sessions=basic_stats.get('unique_sessions', 0),
                actions_breakdown=actions_breakdown,
                level_breakdown=level_breakdown,
                success_rate=float(basic_stats.get('success_rate', 0.0)),
                time_period={'start': start_time, 'end': end_time},
                most_active_users=most_active_users,
                recent_critical_events=recent_critical_events
            )
            
        except Exception as e:
            self.logger.error(f"Failed to generate audit summary: {e}")
            raise
    
    def cleanup_expired_logs(self) -> int:
        """
        Clean up audit logs that have passed their retention period.
        
        Returns:
            Number of deleted entries
        """
        try:
            current_time = datetime.utcnow()
            
            # Delete expired entries
            delete_query = f"""
                DELETE FROM {self.table_name}
                WHERE retention_until IS NOT NULL 
                AND retention_until < %(current_time)s
            """
            
            self.db.execute_query(delete_query, {'current_time': current_time})
            deleted_count = self.db.get_affected_rows()
            
            if deleted_count > 0:
                self.logger.info(f"Cleaned up {deleted_count} expired audit log entries")
            
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Failed to cleanup expired audit logs: {e}")
            raise
    
    def export_audit_data(self, query: AuditQuery, format: str = "json") -> Union[str, bytes]:
        """
        Export audit data in specified format.
        
        Args:
            query: Query parameters for data to export
            format: Export format ("json", "csv")
            
        Returns:
            Exported data as string or bytes
        """
        try:
            # Log the export action
            self.log_system_event(
                action="data_export",
                resource_type="audit_logs",
                details={"format": format, "query": query.__dict__},
                level=AuditLevel.MEDIUM.value,
                compliance_category="security"
            )
            
            # Get the audit data
            result = self.query_audit_logs(query)
            
            if format.lower() == "json":
                # Convert to JSON
                export_data = {
                    'metadata': {
                        'exported_at': datetime.utcnow().isoformat(),
                        'total_records': len(result.data),
                        'query_parameters': query.__dict__
                    },
                    'audit_entries': [
                        {
                            **self._to_dict(entry),
                            'timestamp': entry.timestamp.isoformat() if entry.timestamp else None,
                            'created_at': entry.created_at.isoformat() if entry.created_at else None,
                            'retention_until': entry.retention_until.isoformat() if entry.retention_until else None
                        }
                        for entry in result.data
                    ]
                }
                return json.dumps(export_data, indent=2, default=str)
            
            elif format.lower() == "csv":
                # Convert to CSV
                import csv
                import io
                
                output = io.StringIO()
                
                if result.data:
                    fieldnames = list(self._to_dict(result.data[0]).keys())
                    writer = csv.DictWriter(output, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for entry in result.data:
                        row = self._to_dict(entry)
                        # Convert datetime objects to ISO format strings
                        for key, value in row.items():
                            if isinstance(value, datetime):
                                row[key] = value.isoformat()
                            elif value is None:
                                row[key] = ''
                        writer.writerow(row)
                
                return output.getvalue()
            
            else:
                raise ValidationError(f"Unsupported export format: {format}")
                
        except Exception as e:
            self.logger.error(f"Failed to export audit data: {e}")
            raise


class AsyncAuditRepository(AsyncBaseRepository[AuditEntry, int]):
    """Async version of AuditRepository."""
    
    def __init__(self, db_manager, logger: logging.Logger = None):
        super().__init__(db_manager, "audit_logs", logger)
        
        # Default retention periods
        self.retention_periods = {
            'security': timedelta(days=2555),  # 7 years
            'financial': timedelta(days=2555),  # 7 years
            'medical': timedelta(days=2190),    # 6 years
            'general': timedelta(days=1095),    # 3 years
            'system': timedelta(days=365),      # 1 year
            'debug': timedelta(days=30)         # 30 days
        }
    
    def _to_entity(self, row: Dict[str, Any]) -> AuditEntry:
        """Convert database row to AuditEntry entity."""
        return AuditEntry(
            id=row.get('id'),
            user_id=row.get('user_id'),
            session_id=row.get('session_id'),
            action=row.get('action', ''),
            resource_type=row.get('resource_type', ''),
            resource_id=row.get('resource_id'),
            details=row.get('details'),
            old_values=row.get('old_values'),
            new_values=row.get('new_values'),
            ip_address=row.get('ip_address'),
            user_agent=row.get('user_agent'),
            timestamp=row.get('timestamp'),
            level=row.get('level', AuditLevel.LOW.value),
            success=row.get('success', True),
            error_message=row.get('error_message'),
            compliance_category=row.get('compliance_category'),
            retention_until=row.get('retention_until'),
            is_sensitive=row.get('is_sensitive', False),
            created_at=row.get('created_at')
        )
    
    def _to_dict(self, entity: AuditEntry) -> Dict[str, Any]:
        """Convert AuditEntry entity to dictionary."""
        return {
            'id': entity.id,
            'user_id': entity.user_id,
            'session_id': entity.session_id,
            'action': entity.action,
            'resource_type': entity.resource_type,
            'resource_id': entity.resource_id,
            'details': entity.details,
            'old_values': entity.old_values,
            'new_values': entity.new_values,
            'ip_address': entity.ip_address,
            'user_agent': entity.user_agent,
            'timestamp': entity.timestamp,
            'level': entity.level,
            'success': entity.success,
            'error_message': entity.error_message,
            'compliance_category': entity.compliance_category,
            'retention_until': entity.retention_until,
            'is_sensitive': entity.is_sensitive,
            'created_at': entity.created_at
        }
    
    async def _validate_entity(self, entity: AuditEntry, is_update: bool = False) -> None:
        """Async validate AuditEntry entity."""
        if not entity.action:
            raise ValidationError("Action is required")
        
        if not entity.resource_type:
            raise ValidationError("Resource type is required")
        
        if entity.level not in [level.value for level in AuditLevel]:
            raise ValidationError(f"Invalid audit level: {entity.level}")
        
        # Set default timestamp if not provided
        if not entity.timestamp:
            entity.timestamp = datetime.utcnow()
        
        # Set retention period if not provided
        if not entity.retention_until and entity.compliance_category:
            retention_period = self.retention_periods.get(
                entity.compliance_category, 
                self.retention_periods['general']
            )
            entity.retention_until = entity.timestamp + retention_period
    
    async def log_audit_event(self, user_id: Optional[int], action: str, resource_type: str,
                             **kwargs) -> AuditEntry:
        """Async version of log_audit_event."""
        audit_entry = AuditEntry(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            timestamp=datetime.utcnow(),
            **kwargs
        )
        
        return await self.create(audit_entry)
