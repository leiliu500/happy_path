"""
Base Repository Classes

Provides abstract base classes for implementing the repository pattern.
Includes common database operations, transaction handling, and query utilities.
"""

import asyncio
from abc import ABC, abstractmethod
from typing import (
    Any, Dict, List, Optional, Union, Tuple, Generic, TypeVar,
    Callable, AsyncGenerator, Generator
)
from datetime import datetime, timedelta
from dataclasses import dataclass
import logging

# Type variables for generic repository
T = TypeVar('T')  # Entity type
ID = TypeVar('ID')  # ID type (usually int or str)


@dataclass
class QueryResult:
    """Represents the result of a database query."""
    data: List[Dict[str, Any]]
    total_count: Optional[int] = None
    page: Optional[int] = None
    page_size: Optional[int] = None
    has_next: bool = False
    has_previous: bool = False


@dataclass
class QueryOptions:
    """Options for database queries."""
    limit: Optional[int] = None
    offset: Optional[int] = None
    order_by: Optional[List[str]] = None
    filters: Optional[Dict[str, Any]] = None
    include_count: bool = False
    for_update: bool = False  # SELECT FOR UPDATE


class RepositoryError(Exception):
    """Base exception for repository operations."""
    
    def __init__(self, message: str, error_code: str = None, details: Dict[str, Any] = None):
        super().__init__(message)
        self.error_code = error_code
        self.details = details or {}


class ValidationError(RepositoryError):
    """Raised when data validation fails."""
    pass


class NotFoundError(RepositoryError):
    """Raised when requested entity is not found."""
    pass


class DuplicateError(RepositoryError):
    """Raised when attempting to create duplicate entity."""
    pass


class BaseRepository(ABC, Generic[T, ID]):
    """
    Abstract base repository class for synchronous database operations.
    
    Provides common CRUD operations and query utilities that can be
    inherited by specific repository implementations.
    """
    
    def __init__(self, db_manager, table_name: str, logger: logging.Logger = None):
        """
        Initialize the repository.
        
        Args:
            db_manager: Database manager instance
            table_name: Primary table name for this repository
            logger: Optional logger instance
        """
        self.db = db_manager
        self.table_name = table_name
        self.logger = logger or logging.getLogger(self.__class__.__name__)
        
    # Abstract methods that must be implemented by subclasses
    
    @abstractmethod
    def _to_entity(self, row: Dict[str, Any]) -> T:
        """Convert database row to entity object."""
        pass
        
    @abstractmethod
    def _to_dict(self, entity: T) -> Dict[str, Any]:
        """Convert entity object to dictionary for database operations."""
        pass
        
    @abstractmethod
    def _validate_entity(self, entity: T, is_update: bool = False) -> None:
        """Validate entity before database operations."""
        pass
        
    # Common CRUD operations
    
    def create(self, entity: T) -> T:
        """
        Create a new entity in the database.
        
        Args:
            entity: Entity to create
            
        Returns:
            Created entity with populated ID and metadata
            
        Raises:
            ValidationError: If entity validation fails
            DuplicateError: If entity already exists
        """
        try:
            self._validate_entity(entity, is_update=False)
            data = self._to_dict(entity)
            
            # Remove ID if present (will be auto-generated)
            data.pop('id', None)
            
            # Add creation timestamp
            data['created_at'] = datetime.utcnow()
            data['updated_at'] = datetime.utcnow()
            
            # Build insert query
            columns = list(data.keys())
            placeholders = [f"%({col})s" for col in columns]
            
            query = f"""
                INSERT INTO {self.table_name} ({', '.join(columns)})
                VALUES ({', '.join(placeholders)})
                RETURNING *
            """
            
            result = self.db.execute_query(query, data)
            if not result:
                raise RepositoryError(f"Failed to create {self.table_name} record")
                
            created_entity = self._to_entity(result[0])
            
            self.logger.info(f"Created {self.table_name} record", extra={
                "table": self.table_name,
                "id": getattr(created_entity, 'id', None),
                "operation": "create"
            })
            
            return created_entity
            
        except Exception as e:
            if "duplicate key" in str(e).lower():
                raise DuplicateError(f"Duplicate {self.table_name} record", details={"entity": str(entity)})
            self.logger.error(f"Failed to create {self.table_name} record: {e}")
            raise RepositoryError(f"Failed to create {self.table_name} record: {e}")
    
    def get_by_id(self, entity_id: ID) -> Optional[T]:
        """
        Retrieve entity by ID.
        
        Args:
            entity_id: Primary key of the entity
            
        Returns:
            Entity if found, None otherwise
        """
        try:
            query = f"SELECT * FROM {self.table_name} WHERE id = %(id)s"
            result = self.db.execute_query(query, {"id": entity_id})
            
            if result:
                return self._to_entity(result[0])
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get {self.table_name} by ID {entity_id}: {e}")
            raise RepositoryError(f"Failed to retrieve {self.table_name} record: {e}")
    
    def get_by_id_or_raise(self, entity_id: ID) -> T:
        """
        Retrieve entity by ID or raise NotFoundError.
        
        Args:
            entity_id: Primary key of the entity
            
        Returns:
            Entity
            
        Raises:
            NotFoundError: If entity not found
        """
        entity = self.get_by_id(entity_id)
        if entity is None:
            raise NotFoundError(f"{self.table_name} with ID {entity_id} not found")
        return entity
    
    def update(self, entity: T) -> T:
        """
        Update existing entity.
        
        Args:
            entity: Entity to update (must have ID)
            
        Returns:
            Updated entity
            
        Raises:
            ValidationError: If entity validation fails
            NotFoundError: If entity not found
        """
        try:
            self._validate_entity(entity, is_update=True)
            data = self._to_dict(entity)
            entity_id = data.get('id')
            
            if not entity_id:
                raise ValidationError("Entity must have ID for update operation")
            
            # Check if entity exists
            existing = self.get_by_id(entity_id)
            if not existing:
                raise NotFoundError(f"{self.table_name} with ID {entity_id} not found")
            
            # Remove ID from update data and add updated timestamp
            update_data = {k: v for k, v in data.items() if k != 'id'}
            update_data['updated_at'] = datetime.utcnow()
            
            # Build update query
            set_clauses = [f"{col} = %({col})s" for col in update_data.keys()]
            query = f"""
                UPDATE {self.table_name}
                SET {', '.join(set_clauses)}
                WHERE id = %(id)s
                RETURNING *
            """
            
            params = {**update_data, 'id': entity_id}
            result = self.db.execute_query(query, params)
            
            if not result:
                raise RepositoryError(f"Failed to update {self.table_name} record")
                
            updated_entity = self._to_entity(result[0])
            
            self.logger.info(f"Updated {self.table_name} record", extra={
                "table": self.table_name,
                "id": entity_id,
                "operation": "update"
            })
            
            return updated_entity
            
        except (ValidationError, NotFoundError):
            raise
        except Exception as e:
            self.logger.error(f"Failed to update {self.table_name} record: {e}")
            raise RepositoryError(f"Failed to update {self.table_name} record: {e}")
    
    def delete(self, entity_id: ID) -> bool:
        """
        Delete entity by ID.
        
        Args:
            entity_id: Primary key of the entity
            
        Returns:
            True if deleted, False if not found
        """
        try:
            query = f"DELETE FROM {self.table_name} WHERE id = %(id)s"
            result = self.db.execute_query(query, {"id": entity_id})
            
            deleted = self.db.get_affected_rows() > 0
            
            if deleted:
                self.logger.info(f"Deleted {self.table_name} record", extra={
                    "table": self.table_name,
                    "id": entity_id,
                    "operation": "delete"
                })
            
            return deleted
            
        except Exception as e:
            self.logger.error(f"Failed to delete {self.table_name} record {entity_id}: {e}")
            raise RepositoryError(f"Failed to delete {self.table_name} record: {e}")
    
    def delete_or_raise(self, entity_id: ID) -> None:
        """
        Delete entity by ID or raise NotFoundError.
        
        Args:
            entity_id: Primary key of the entity
            
        Raises:
            NotFoundError: If entity not found
        """
        deleted = self.delete(entity_id)
        if not deleted:
            raise NotFoundError(f"{self.table_name} with ID {entity_id} not found")
    
    def list_all(self, options: QueryOptions = None) -> QueryResult:
        """
        List all entities with optional filtering and pagination.
        
        Args:
            options: Query options for filtering, ordering, and pagination
            
        Returns:
            QueryResult with entities and metadata
        """
        try:
            options = options or QueryOptions()
            
            # Build base query
            query_parts = [f"SELECT * FROM {self.table_name}"]
            params = {}
            
            # Add WHERE clause if filters provided
            if options.filters:
                where_clauses = []
                for key, value in options.filters.items():
                    param_name = f"filter_{key}"
                    if isinstance(value, list):
                        placeholders = ', '.join([f"%({param_name}_{i})s" for i in range(len(value))])
                        where_clauses.append(f"{key} IN ({placeholders})")
                        for i, v in enumerate(value):
                            params[f"{param_name}_{i}"] = v
                    else:
                        where_clauses.append(f"{key} = %({param_name})s")
                        params[param_name] = value
                
                if where_clauses:
                    query_parts.append(f"WHERE {' AND '.join(where_clauses)}")
            
            # Add ORDER BY clause
            if options.order_by:
                order_clauses = []
                for order_field in options.order_by:
                    if order_field.startswith('-'):
                        order_clauses.append(f"{order_field[1:]} DESC")
                    else:
                        order_clauses.append(f"{order_field} ASC")
                query_parts.append(f"ORDER BY {', '.join(order_clauses)}")
            
            # Get total count if requested
            total_count = None
            if options.include_count:
                count_query = f"SELECT COUNT(*) as count FROM {self.table_name}"
                if options.filters:
                    where_clause = query_parts[1] if len(query_parts) > 1 and query_parts[1].startswith('WHERE') else None
                    if where_clause:
                        count_query += f" {where_clause}"
                
                count_result = self.db.execute_query(count_query, params)
                total_count = count_result[0]['count'] if count_result else 0
            
            # Add LIMIT and OFFSET
            if options.limit:
                query_parts.append(f"LIMIT %(limit)s")
                params['limit'] = options.limit
                
                if options.offset:
                    query_parts.append(f"OFFSET %(offset)s")
                    params['offset'] = options.offset
            
            # Execute query
            query = ' '.join(query_parts)
            result = self.db.execute_query(query, params)
            
            # Convert to entities
            entities = [self._to_entity(row) for row in result] if result else []
            
            # Calculate pagination metadata
            page = None
            page_size = None
            has_next = False
            has_previous = False
            
            if options.limit and options.offset is not None:
                page_size = options.limit
                page = (options.offset // options.limit) + 1
                has_previous = options.offset > 0
                
                if total_count is not None:
                    has_next = (options.offset + options.limit) < total_count
                else:
                    # If we don't have total count, check if we got a full page
                    has_next = len(entities) == options.limit
            
            return QueryResult(
                data=entities,
                total_count=total_count,
                page=page,
                page_size=page_size,
                has_next=has_next,
                has_previous=has_previous
            )
            
        except Exception as e:
            self.logger.error(f"Failed to list {self.table_name} records: {e}")
            raise RepositoryError(f"Failed to list {self.table_name} records: {e}")
    
    def exists(self, entity_id: ID) -> bool:
        """
        Check if entity exists by ID.
        
        Args:
            entity_id: Primary key of the entity
            
        Returns:
            True if exists, False otherwise
        """
        try:
            query = f"SELECT 1 FROM {self.table_name} WHERE id = %(id)s LIMIT 1"
            result = self.db.execute_query(query, {"id": entity_id})
            return bool(result)
            
        except Exception as e:
            self.logger.error(f"Failed to check existence of {self.table_name} {entity_id}: {e}")
            raise RepositoryError(f"Failed to check {self.table_name} existence: {e}")
    
    def count(self, filters: Dict[str, Any] = None) -> int:
        """
        Count entities with optional filters.
        
        Args:
            filters: Optional filters to apply
            
        Returns:
            Count of matching entities
        """
        try:
            query_parts = [f"SELECT COUNT(*) as count FROM {self.table_name}"]
            params = {}
            
            if filters:
                where_clauses = []
                for key, value in filters.items():
                    param_name = f"filter_{key}"
                    where_clauses.append(f"{key} = %({param_name})s")
                    params[param_name] = value
                
                if where_clauses:
                    query_parts.append(f"WHERE {' AND '.join(where_clauses)}")
            
            query = ' '.join(query_parts)
            result = self.db.execute_query(query, params)
            
            return result[0]['count'] if result else 0
            
        except Exception as e:
            self.logger.error(f"Failed to count {self.table_name} records: {e}")
            raise RepositoryError(f"Failed to count {self.table_name} records: {e}")
    
    def find_by(self, **kwargs) -> List[T]:
        """
        Find entities by field values.
        
        Args:
            **kwargs: Field name/value pairs to filter by
            
        Returns:
            List of matching entities
        """
        options = QueryOptions(filters=kwargs)
        result = self.list_all(options)
        return result.data
    
    def find_one_by(self, **kwargs) -> Optional[T]:
        """
        Find single entity by field values.
        
        Args:
            **kwargs: Field name/value pairs to filter by
            
        Returns:
            First matching entity or None
        """
        options = QueryOptions(filters=kwargs, limit=1)
        result = self.list_all(options)
        return result.data[0] if result.data else None
    
    def find_one_by_or_raise(self, **kwargs) -> T:
        """
        Find single entity by field values or raise NotFoundError.
        
        Args:
            **kwargs: Field name/value pairs to filter by
            
        Returns:
            First matching entity
            
        Raises:
            NotFoundError: If no entity found
        """
        entity = self.find_one_by(**kwargs)
        if entity is None:
            filter_desc = ', '.join([f"{k}={v}" for k, v in kwargs.items()])
            raise NotFoundError(f"{self.table_name} with {filter_desc} not found")
        return entity
    
    def bulk_create(self, entities: List[T]) -> List[T]:
        """
        Create multiple entities in a single transaction.
        
        Args:
            entities: List of entities to create
            
        Returns:
            List of created entities with IDs
        """
        if not entities:
            return []
        
        try:
            created_entities = []
            
            with self.db.transaction():
                for entity in entities:
                    created = self.create(entity)
                    created_entities.append(created)
            
            self.logger.info(f"Bulk created {len(created_entities)} {self.table_name} records")
            return created_entities
            
        except Exception as e:
            self.logger.error(f"Failed to bulk create {self.table_name} records: {e}")
            raise RepositoryError(f"Failed to bulk create {self.table_name} records: {e}")
    
    def bulk_update(self, entities: List[T]) -> List[T]:
        """
        Update multiple entities in a single transaction.
        
        Args:
            entities: List of entities to update
            
        Returns:
            List of updated entities
        """
        if not entities:
            return []
        
        try:
            updated_entities = []
            
            with self.db.transaction():
                for entity in entities:
                    updated = self.update(entity)
                    updated_entities.append(updated)
            
            self.logger.info(f"Bulk updated {len(updated_entities)} {self.table_name} records")
            return updated_entities
            
        except Exception as e:
            self.logger.error(f"Failed to bulk update {self.table_name} records: {e}")
            raise RepositoryError(f"Failed to bulk update {self.table_name} records: {e}")


class AsyncBaseRepository(ABC, Generic[T, ID]):
    """
    Abstract base repository class for asynchronous database operations.
    
    Similar to BaseRepository but with async/await support for better
    performance in async applications.
    """
    
    def __init__(self, db_manager, table_name: str, logger: logging.Logger = None):
        """
        Initialize the async repository.
        
        Args:
            db_manager: Async database manager instance
            table_name: Primary table name for this repository
            logger: Optional logger instance
        """
        self.db = db_manager
        self.table_name = table_name
        self.logger = logger or logging.getLogger(self.__class__.__name__)
    
    # Abstract methods (same as BaseRepository)
    
    @abstractmethod
    def _to_entity(self, row: Dict[str, Any]) -> T:
        """Convert database row to entity object."""
        pass
        
    @abstractmethod
    def _to_dict(self, entity: T) -> Dict[str, Any]:
        """Convert entity object to dictionary for database operations."""
        pass
        
    @abstractmethod
    async def _validate_entity(self, entity: T, is_update: bool = False) -> None:
        """Validate entity before database operations."""
        pass
    
    # Async CRUD operations
    
    async def create(self, entity: T) -> T:
        """Async version of create operation."""
        try:
            await self._validate_entity(entity, is_update=False)
            data = self._to_dict(entity)
            
            # Remove ID if present (will be auto-generated)
            data.pop('id', None)
            
            # Add creation timestamp
            data['created_at'] = datetime.utcnow()
            data['updated_at'] = datetime.utcnow()
            
            # Build insert query
            columns = list(data.keys())
            placeholders = [f"%({col})s" for col in columns]
            
            query = f"""
                INSERT INTO {self.table_name} ({', '.join(columns)})
                VALUES ({', '.join(placeholders)})
                RETURNING *
            """
            
            result = await self.db.execute_query_async(query, data)
            if not result:
                raise RepositoryError(f"Failed to create {self.table_name} record")
                
            created_entity = self._to_entity(result[0])
            
            self.logger.info(f"Created {self.table_name} record", extra={
                "table": self.table_name,
                "id": getattr(created_entity, 'id', None),
                "operation": "create"
            })
            
            return created_entity
            
        except Exception as e:
            if "duplicate key" in str(e).lower():
                raise DuplicateError(f"Duplicate {self.table_name} record", details={"entity": str(entity)})
            self.logger.error(f"Failed to create {self.table_name} record: {e}")
            raise RepositoryError(f"Failed to create {self.table_name} record: {e}")
    
    async def get_by_id(self, entity_id: ID) -> Optional[T]:
        """Async version of get_by_id operation."""
        try:
            query = f"SELECT * FROM {self.table_name} WHERE id = %(id)s"
            result = await self.db.execute_query_async(query, {"id": entity_id})
            
            if result:
                return self._to_entity(result[0])
            return None
            
        except Exception as e:
            self.logger.error(f"Failed to get {self.table_name} by ID {entity_id}: {e}")
            raise RepositoryError(f"Failed to retrieve {self.table_name} record: {e}")
    
    async def update(self, entity: T) -> T:
        """Async version of update operation."""
        try:
            await self._validate_entity(entity, is_update=True)
            data = self._to_dict(entity)
            entity_id = data.get('id')
            
            if not entity_id:
                raise ValidationError("Entity must have ID for update operation")
            
            # Check if entity exists
            existing = await self.get_by_id(entity_id)
            if not existing:
                raise NotFoundError(f"{self.table_name} with ID {entity_id} not found")
            
            # Remove ID from update data and add updated timestamp
            update_data = {k: v for k, v in data.items() if k != 'id'}
            update_data['updated_at'] = datetime.utcnow()
            
            # Build update query
            set_clauses = [f"{col} = %({col})s" for col in update_data.keys()]
            query = f"""
                UPDATE {self.table_name}
                SET {', '.join(set_clauses)}
                WHERE id = %(id)s
                RETURNING *
            """
            
            params = {**update_data, 'id': entity_id}
            result = await self.db.execute_query_async(query, params)
            
            if not result:
                raise RepositoryError(f"Failed to update {self.table_name} record")
                
            updated_entity = self._to_entity(result[0])
            
            self.logger.info(f"Updated {self.table_name} record", extra={
                "table": self.table_name,
                "id": entity_id,
                "operation": "update"
            })
            
            return updated_entity
            
        except (ValidationError, NotFoundError):
            raise
        except Exception as e:
            self.logger.error(f"Failed to update {self.table_name} record: {e}")
            raise RepositoryError(f"Failed to update {self.table_name} record: {e}")
    
    async def delete(self, entity_id: ID) -> bool:
        """Async version of delete operation."""
        try:
            query = f"DELETE FROM {self.table_name} WHERE id = %(id)s"
            result = await self.db.execute_query_async(query, {"id": entity_id})
            
            deleted = await self.db.get_affected_rows_async() > 0
            
            if deleted:
                self.logger.info(f"Deleted {self.table_name} record", extra={
                    "table": self.table_name,
                    "id": entity_id,
                    "operation": "delete"
                })
            
            return deleted
            
        except Exception as e:
            self.logger.error(f"Failed to delete {self.table_name} record {entity_id}: {e}")
            raise RepositoryError(f"Failed to delete {self.table_name} record: {e}")
    
    # Additional async methods would follow the same pattern...
    # For brevity, I'll include just the essential ones here
    
    async def list_all(self, options: QueryOptions = None) -> QueryResult:
        """Async version of list_all operation."""
        # Implementation similar to sync version but with await
        # Would be implemented with async database calls
        pass
    
    async def exists(self, entity_id: ID) -> bool:
        """Async version of exists check."""
        try:
            query = f"SELECT 1 FROM {self.table_name} WHERE id = %(id)s LIMIT 1"
            result = await self.db.execute_query_async(query, {"id": entity_id})
            return bool(result)
            
        except Exception as e:
            self.logger.error(f"Failed to check existence of {self.table_name} {entity_id}: {e}")
            raise RepositoryError(f"Failed to check {self.table_name} existence: {e}")


# Utility functions for repositories

def build_where_clause(filters: Dict[str, Any]) -> Tuple[str, Dict[str, Any]]:
    """
    Build WHERE clause and parameters from filters dictionary.
    
    Args:
        filters: Dictionary of field name/value pairs
        
    Returns:
        Tuple of (where_clause, parameters)
    """
    if not filters:
        return "", {}
    
    where_clauses = []
    params = {}
    
    for key, value in filters.items():
        param_name = f"filter_{key}"
        
        if value is None:
            where_clauses.append(f"{key} IS NULL")
        elif isinstance(value, list):
            if not value:
                continue
            placeholders = ', '.join([f"%({param_name}_{i})s" for i in range(len(value))])
            where_clauses.append(f"{key} IN ({placeholders})")
            for i, v in enumerate(value):
                params[f"{param_name}_{i}"] = v
        elif isinstance(value, dict):
            # Support for operators like {'gte': 100}, {'lt': 50}
            for op, op_value in value.items():
                operator_map = {
                    'eq': '=',
                    'ne': '!=', 
                    'gt': '>',
                    'gte': '>=',
                    'lt': '<',
                    'lte': '<=',
                    'like': 'LIKE',
                    'ilike': 'ILIKE'
                }
                
                if op in operator_map:
                    op_param = f"{param_name}_{op}"
                    where_clauses.append(f"{key} {operator_map[op]} %({op_param})s")
                    params[op_param] = op_value
        else:
            where_clauses.append(f"{key} = %({param_name})s")
            params[param_name] = value
    
    where_clause = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
    return where_clause, params


def build_order_clause(order_by: List[str]) -> str:
    """
    Build ORDER BY clause from list of field names.
    
    Args:
        order_by: List of field names, prefix with '-' for DESC
        
    Returns:
        ORDER BY clause string
    """
    if not order_by:
        return ""
    
    order_clauses = []
    for order_field in order_by:
        if order_field.startswith('-'):
            order_clauses.append(f"{order_field[1:]} DESC")
        else:
            order_clauses.append(f"{order_field} ASC")
    
    return f"ORDER BY {', '.join(order_clauses)}"
