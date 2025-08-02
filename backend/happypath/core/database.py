"""
Database management for the Happy Path platform.
Provides connection pooling, query execution, and transaction management.
"""

import asyncio
import logging
from contextlib import asynccontextmanager, contextmanager
from typing import Any, Dict, List, Optional, Tuple, Union
from datetime import datetime, timezone
import uuid

import asyncpg
import psycopg2
from psycopg2 import pool, sql
from psycopg2.extras import RealDictCursor, execute_values

from .config import get_config
from .exceptions import DatabaseError, ConnectionError, QueryError, TransactionError
from .logging import get_logger

logger = get_logger(__name__)


class DatabaseManager:
    """Main database manager with connection pooling and query utilities."""
    
    def __init__(self):
        self.config = get_config()
        self._pool: Optional[pool.ThreadedConnectionPool] = None
        self._async_pool: Optional[asyncpg.Pool] = None
        self._initialized = False
    
    def initialize(self):
        """Initialize the database connection pool."""
        if self._initialized:
            return
        
        try:
            # Create synchronous connection pool
            self._pool = psycopg2.pool.ThreadedConnectionPool(
                minconn=1,
                maxconn=self.config.database.pool_size,
                host=self.config.database.host,
                port=self.config.database.port,
                database=self.config.database.database,
                user=self.config.database.username,
                password=self.config.database.password,
                application_name=self.config.database.application_name,
                sslmode=self.config.database.ssl_mode,
                cursor_factory=RealDictCursor
            )
            
            self._initialized = True
            logger.info("Database connection pool initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize database connection pool: {e}")
            raise ConnectionError(f"Database initialization failed: {e}")
    
    async def initialize_async(self):
        """Initialize async database connection pool."""
        if self._async_pool:
            return
        
        try:
            self._async_pool = await asyncpg.create_pool(
                host=self.config.database.host,
                port=self.config.database.port,
                database=self.config.database.database,
                user=self.config.database.username,
                password=self.config.database.password,
                min_size=1,
                max_size=self.config.database.pool_size,
                command_timeout=60,
                server_settings={
                    'application_name': self.config.database.application_name,
                    'timezone': 'UTC'
                }
            )
            logger.info("Async database connection pool initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize async database pool: {e}")
            raise ConnectionError(f"Async database initialization failed: {e}")
    
    @contextmanager
    def get_connection(self):
        """Get a database connection from the pool."""
        if not self._initialized:
            self.initialize()
        
        connection = None
        try:
            connection = self._pool.getconn()
            if connection is None:
                raise ConnectionError("Failed to get connection from pool")
            
            # Test connection
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            
            yield connection
            
        except Exception as e:
            if connection:
                connection.rollback()
            logger.error(f"Database connection error: {e}")
            raise ConnectionError(f"Connection error: {e}")
        finally:
            if connection:
                self._pool.putconn(connection)
    
    @asynccontextmanager
    async def get_async_connection(self):
        """Get an async database connection from the pool."""
        if not self._async_pool:
            await self.initialize_async()
        
        async with self._async_pool.acquire() as connection:
            yield connection
    
    def execute_query(
        self, 
        query: str, 
        params: Optional[Union[Dict, Tuple, List]] = None,
        fetch_one: bool = False,
        fetch_all: bool = True
    ) -> Union[List[Dict], Dict, None]:
        """Execute a SQL query and return results."""
        with self.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    cursor.execute(query, params)
                    
                    if fetch_one:
                        result = cursor.fetchone()
                        return dict(result) if result else None
                    elif fetch_all:
                        results = cursor.fetchall()
                        return [dict(row) for row in results]
                    else:
                        return None
                        
            except Exception as e:
                logger.error(f"Query execution failed: {e}, Query: {query[:100]}...")
                raise QueryError(f"Query execution failed: {e}")
    
    async def execute_async_query(
        self,
        query: str,
        params: Optional[Union[List, Tuple]] = None,
        fetch_one: bool = False,
        fetch_all: bool = True
    ) -> Union[List[Dict], Dict, None]:
        """Execute an async SQL query and return results."""
        async with self.get_async_connection() as conn:
            try:
                if fetch_one:
                    result = await conn.fetchrow(query, *(params or []))
                    return dict(result) if result else None
                elif fetch_all:
                    results = await conn.fetch(query, *(params or []))
                    return [dict(row) for row in results]
                else:
                    await conn.execute(query, *(params or []))
                    return None
                    
            except Exception as e:
                logger.error(f"Async query execution failed: {e}, Query: {query[:100]}...")
                raise QueryError(f"Async query execution failed: {e}")
    
    def execute_transaction(self, operations: List[Tuple[str, Optional[Union[Dict, Tuple, List]]]]) -> bool:
        """Execute multiple queries in a transaction."""
        with self.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    for query, params in operations:
                        cursor.execute(query, params)
                    conn.commit()
                    return True
                    
            except Exception as e:
                conn.rollback()
                logger.error(f"Transaction failed: {e}")
                raise TransactionError(f"Transaction failed: {e}")
    
    def execute_batch_insert(
        self,
        table: str,
        columns: List[str],
        data: List[Union[Dict, Tuple, List]],
        page_size: int = 1000
    ) -> int:
        """Execute batch insert operation."""
        if not data:
            return 0
        
        with self.get_connection() as conn:
            try:
                with conn.cursor() as cursor:
                    # Prepare insert query
                    placeholders = ', '.join(['%s'] * len(columns))
                    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
                    
                    # Convert data to tuples if needed
                    if isinstance(data[0], dict):
                        data = [tuple(row[col] for col in columns) for row in data]
                    
                    # Execute batch insert
                    execute_values(
                        cursor,
                        query,
                        data,
                        page_size=page_size
                    )
                    
                    conn.commit()
                    return len(data)
                    
            except Exception as e:
                conn.rollback()
                logger.error(f"Batch insert failed: {e}")
                raise QueryError(f"Batch insert failed: {e}")
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get database health status."""
        try:
            with self.get_connection() as conn:
                with conn.cursor() as cursor:
                    # Check basic connectivity
                    cursor.execute("SELECT 1 as status")
                    basic_check = cursor.fetchone()
                    
                    # Get database stats
                    cursor.execute("""
                        SELECT 
                            current_database() as database_name,
                            version() as version,
                            current_timestamp as current_time,
                            (SELECT count(*) FROM pg_stat_activity WHERE state = 'active') as active_connections
                    """)
                    stats = cursor.fetchone()
                    
                    # Get table counts
                    cursor.execute("""
                        SELECT 
                            count(*) as table_count
                        FROM information_schema.tables 
                        WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
                    """)
                    table_info = cursor.fetchone()
                    
                    return {
                        "status": "healthy" if basic_check else "unhealthy",
                        "database_name": stats["database_name"],
                        "version": stats["version"],
                        "current_time": stats["current_time"],
                        "active_connections": stats["active_connections"],
                        "table_count": table_info["table_count"],
                        "pool_size": self.config.database.pool_size,
                        "checked_at": datetime.now(timezone.utc)
                    }
                    
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy",
                "error": str(e),
                "checked_at": datetime.now(timezone.utc)
            }
    
    def close(self):
        """Close database connection pools."""
        if self._pool:
            self._pool.closeall()
            self._pool = None
        
        if self._async_pool:
            asyncio.create_task(self._async_pool.close())
            self._async_pool = None
        
        self._initialized = False
        logger.info("Database connection pools closed")


# Global database manager instance
_db_manager: Optional[DatabaseManager] = None


def get_db_manager() -> DatabaseManager:
    """Get the global database manager instance."""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
        _db_manager.initialize()
    return _db_manager


def get_db_connection():
    """Get a database connection context manager."""
    return get_db_manager().get_connection()


def execute_query(
    query: str,
    params: Optional[Union[Dict, Tuple, List]] = None,
    fetch_one: bool = False,
    fetch_all: bool = True
) -> Union[List[Dict], Dict, None]:
    """Execute a SQL query using the global database manager."""
    return get_db_manager().execute_query(query, params, fetch_one, fetch_all)


def execute_transaction(operations: List[Tuple[str, Optional[Union[Dict, Tuple, List]]]]) -> bool:
    """Execute a transaction using the global database manager."""
    return get_db_manager().execute_transaction(operations)


class QueryBuilder:
    """SQL query builder utility class."""
    
    def __init__(self, table: str):
        self.table = table
        self._select_fields = []
        self._where_conditions = []
        self._joins = []
        self._order_by = []
        self._limit_count = None
        self._offset_count = None
        self._params = {}
    
    def select(self, *fields: str) -> 'QueryBuilder':
        """Add SELECT fields."""
        self._select_fields.extend(fields)
        return self
    
    def where(self, condition: str, **params) -> 'QueryBuilder':
        """Add WHERE condition."""
        self._where_conditions.append(condition)
        self._params.update(params)
        return self
    
    def join(self, table: str, on_condition: str) -> 'QueryBuilder':
        """Add JOIN clause."""
        self._joins.append(f"JOIN {table} ON {on_condition}")
        return self
    
    def left_join(self, table: str, on_condition: str) -> 'QueryBuilder':
        """Add LEFT JOIN clause."""
        self._joins.append(f"LEFT JOIN {table} ON {on_condition}")
        return self
    
    def order_by(self, field: str, direction: str = "ASC") -> 'QueryBuilder':
        """Add ORDER BY clause."""
        self._order_by.append(f"{field} {direction}")
        return self
    
    def limit(self, count: int) -> 'QueryBuilder':
        """Add LIMIT clause."""
        self._limit_count = count
        return self
    
    def offset(self, count: int) -> 'QueryBuilder':
        """Add OFFSET clause."""
        self._offset_count = count
        return self
    
    def build(self) -> Tuple[str, Dict]:
        """Build the SQL query and parameters."""
        # SELECT clause
        fields = ", ".join(self._select_fields) if self._select_fields else "*"
        query = f"SELECT {fields} FROM {self.table}"
        
        # JOIN clauses
        if self._joins:
            query += " " + " ".join(self._joins)
        
        # WHERE clause
        if self._where_conditions:
            query += " WHERE " + " AND ".join(self._where_conditions)
        
        # ORDER BY clause
        if self._order_by:
            query += " ORDER BY " + ", ".join(self._order_by)
        
        # LIMIT clause
        if self._limit_count:
            query += f" LIMIT {self._limit_count}"
        
        # OFFSET clause
        if self._offset_count:
            query += f" OFFSET {self._offset_count}"
        
        return query, self._params
    
    def execute(self) -> List[Dict]:
        """Execute the built query."""
        query, params = self.build()
        return execute_query(query, params)


def query_builder(table: str) -> QueryBuilder:
    """Create a new query builder instance."""
    return QueryBuilder(table)
