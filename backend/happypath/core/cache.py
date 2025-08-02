"""
Cache management for the Happy Path platform.
Provides Redis-based caching with automatic serialization and TTL management.
"""

import json
import pickle
import time
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Union, Callable
from functools import wraps
import hashlib

import redis
from redis.connection import ConnectionPool

from .config import get_config
from .logging import get_logger
from .exceptions import CacheError

logger = get_logger(__name__)


class CacheManager:
    """Redis-based cache manager with serialization and TTL support."""
    
    def __init__(self):
        self.config = get_config()
        self._pool: Optional[ConnectionPool] = None
        self._redis: Optional[redis.Redis] = None
        self._initialized = False
    
    def initialize(self):
        """Initialize Redis connection pool."""
        if self._initialized:
            return
        
        try:
            # Create connection pool
            self._pool = redis.ConnectionPool(
                host=self.config.redis.host,
                port=self.config.redis.port,
                db=self.config.redis.database,
                password=self.config.redis.password,
                max_connections=self.config.redis.pool_size,
                socket_timeout=self.config.redis.timeout,
                socket_connect_timeout=self.config.redis.timeout,
                decode_responses=False  # We handle encoding/decoding ourselves
            )
            
            # Create Redis client
            self._redis = redis.Redis(connection_pool=self._pool)
            
            # Test connection
            self._redis.ping()
            
            self._initialized = True
            logger.info("Redis cache initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Redis cache: {e}")
            raise CacheError(f"Cache initialization failed: {e}")
    
    def _ensure_initialized(self):
        """Ensure cache is initialized."""
        if not self._initialized:
            self.initialize()
    
    def _serialize_value(self, value: Any) -> bytes:
        """Serialize value for storage."""
        if isinstance(value, (str, int, float, bool)):
            # Store simple types as JSON
            return json.dumps(value).encode('utf-8')
        else:
            # Use pickle for complex types
            return pickle.dumps(value)
    
    def _deserialize_value(self, data: bytes) -> Any:
        """Deserialize value from storage."""
        try:
            # Try JSON first (for simple types)
            return json.loads(data.decode('utf-8'))
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Fall back to pickle
            return pickle.loads(data)
    
    def set(
        self,
        key: str,
        value: Any,
        ttl: Optional[int] = None,
        namespace: str = "default"
    ) -> bool:
        """Set a value in cache with optional TTL."""
        self._ensure_initialized()
        
        try:
            cache_key = self._build_key(key, namespace)
            serialized_value = self._serialize_value(value)
            
            if ttl:
                return bool(self._redis.setex(cache_key, ttl, serialized_value))
            else:
                return bool(self._redis.set(cache_key, serialized_value))
                
        except Exception as e:
            logger.error(f"Cache set failed for key {key}: {e}")
            raise CacheError(f"Failed to set cache value: {e}")
    
    def get(self, key: str, namespace: str = "default", default: Any = None) -> Any:
        """Get a value from cache."""
        self._ensure_initialized()
        
        try:
            cache_key = self._build_key(key, namespace)
            data = self._redis.get(cache_key)
            
            if data is None:
                return default
            
            return self._deserialize_value(data)
            
        except Exception as e:
            logger.error(f"Cache get failed for key {key}: {e}")
            return default
    
    def delete(self, key: str, namespace: str = "default") -> bool:
        """Delete a value from cache."""
        self._ensure_initialized()
        
        try:
            cache_key = self._build_key(key, namespace)
            return bool(self._redis.delete(cache_key))
            
        except Exception as e:
            logger.error(f"Cache delete failed for key {key}: {e}")
            raise CacheError(f"Failed to delete cache value: {e}")
    
    def exists(self, key: str, namespace: str = "default") -> bool:
        """Check if a key exists in cache."""
        self._ensure_initialized()
        
        try:
            cache_key = self._build_key(key, namespace)
            return bool(self._redis.exists(cache_key))
            
        except Exception as e:
            logger.error(f"Cache exists check failed for key {key}: {e}")
            return False
    
    def expire(self, key: str, ttl: int, namespace: str = "default") -> bool:
        """Set TTL for an existing key."""
        self._ensure_initialized()
        
        try:
            cache_key = self._build_key(key, namespace)
            return bool(self._redis.expire(cache_key, ttl))
            
        except Exception as e:
            logger.error(f"Cache expire failed for key {key}: {e}")
            raise CacheError(f"Failed to set cache expiration: {e}")
    
    def ttl(self, key: str, namespace: str = "default") -> int:
        """Get TTL for a key."""
        self._ensure_initialized()
        
        try:
            cache_key = self._build_key(key, namespace)
            return self._redis.ttl(cache_key)
            
        except Exception as e:
            logger.error(f"Cache TTL check failed for key {key}: {e}")
            return -1
    
    def clear_namespace(self, namespace: str) -> int:
        """Clear all keys in a namespace."""
        self._ensure_initialized()
        
        try:
            pattern = f"happy_path:{namespace}:*"
            keys = self._redis.keys(pattern)
            
            if keys:
                return self._redis.delete(*keys)
            return 0
            
        except Exception as e:
            logger.error(f"Cache namespace clear failed for {namespace}: {e}")
            raise CacheError(f"Failed to clear cache namespace: {e}")
    
    def clear_all(self) -> bool:
        """Clear all cache data (use with caution)."""
        self._ensure_initialized()
        
        try:
            pattern = "happy_path:*"
            keys = self._redis.keys(pattern)
            
            if keys:
                self._redis.delete(*keys)
            
            return True
            
        except Exception as e:
            logger.error(f"Cache clear all failed: {e}")
            raise CacheError(f"Failed to clear all cache data: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        self._ensure_initialized()
        
        try:
            info = self._redis.info()
            
            return {
                "connected_clients": info.get("connected_clients", 0),
                "used_memory": info.get("used_memory", 0),
                "used_memory_human": info.get("used_memory_human", "0B"),
                "keyspace_hits": info.get("keyspace_hits", 0),
                "keyspace_misses": info.get("keyspace_misses", 0),
                "total_commands_processed": info.get("total_commands_processed", 0),
                "instantaneous_ops_per_sec": info.get("instantaneous_ops_per_sec", 0),
                "uptime_in_seconds": info.get("uptime_in_seconds", 0)
            }
            
        except Exception as e:
            logger.error(f"Failed to get cache stats: {e}")
            return {}
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get cache health status."""
        try:
            self._ensure_initialized()
            
            # Test basic operations
            test_key = "health_check_test"
            test_value = "ping"
            
            start_time = time.time()
            self.set(test_key, test_value, ttl=5, namespace="health")
            result = self.get(test_key, namespace="health")
            self.delete(test_key, namespace="health")
            response_time = (time.time() - start_time) * 1000
            
            if result == test_value:
                return {
                    "status": "healthy",
                    "message": "Cache is responsive",
                    "response_time_ms": response_time,
                    "timestamp": datetime.now(timezone.utc)
                }
            else:
                return {
                    "status": "unhealthy",
                    "message": "Cache test failed",
                    "response_time_ms": response_time,
                    "timestamp": datetime.now(timezone.utc)
                }
                
        except Exception as e:
            return {
                "status": "unhealthy",
                "message": f"Cache health check failed: {e}",
                "timestamp": datetime.now(timezone.utc)
            }
    
    def _build_key(self, key: str, namespace: str) -> str:
        """Build cache key with namespace."""
        return f"happy_path:{namespace}:{key}"
    
    def close(self):
        """Close Redis connection."""
        if self._redis:
            self._redis.close()
        if self._pool:
            self._pool.disconnect()
        self._initialized = False
        logger.info("Redis cache connection closed")


class CacheDecorator:
    """Decorator for caching function results."""
    
    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
    
    def cached(
        self,
        ttl: int = 300,
        namespace: str = "functions",
        key_func: Optional[Callable] = None,
        ignore_args: Optional[List[str]] = None
    ):
        """Decorator to cache function results."""
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Generate cache key
                cache_key = self._generate_cache_key(
                    func, args, kwargs, key_func, ignore_args
                )
                
                # Try to get from cache
                cached_result = self.cache.get(cache_key, namespace)
                if cached_result is not None:
                    logger.debug(f"Cache hit for {func.__name__}")
                    return cached_result
                
                # Execute function and cache result
                logger.debug(f"Cache miss for {func.__name__}")
                result = func(*args, **kwargs)
                
                # Cache the result
                self.cache.set(cache_key, result, ttl, namespace)
                
                return result
            
            # Add cache control methods to the wrapper
            wrapper.cache_invalidate = lambda *args, **kwargs: self._invalidate_cache(
                func, args, kwargs, key_func, ignore_args, namespace
            )
            wrapper.cache_refresh = lambda *args, **kwargs: self._refresh_cache(
                func, args, kwargs, key_func, ignore_args, namespace, ttl
            )
            
            return wrapper
        return decorator
    
    def _generate_cache_key(
        self,
        func: Callable,
        args: tuple,
        kwargs: dict,
        key_func: Optional[Callable],
        ignore_args: Optional[List[str]]
    ) -> str:
        """Generate cache key for function call."""
        if key_func:
            return key_func(*args, **kwargs)
        
        # Build key from function name and arguments
        func_name = f"{func.__module__}.{func.__name__}"
        
        # Filter out ignored arguments
        if ignore_args:
            kwargs = {k: v for k, v in kwargs.items() if k not in ignore_args}
        
        # Create hashable representation of arguments
        args_str = str(args)
        kwargs_str = str(sorted(kwargs.items()))
        
        # Hash the arguments to create a consistent key
        args_hash = hashlib.md5(f"{args_str}{kwargs_str}".encode()).hexdigest()
        
        return f"{func_name}:{args_hash}"
    
    def _invalidate_cache(
        self,
        func: Callable,
        args: tuple,
        kwargs: dict,
        key_func: Optional[Callable],
        ignore_args: Optional[List[str]],
        namespace: str
    ):
        """Invalidate cached result for function call."""
        cache_key = self._generate_cache_key(func, args, kwargs, key_func, ignore_args)
        self.cache.delete(cache_key, namespace)
    
    def _refresh_cache(
        self,
        func: Callable,
        args: tuple,
        kwargs: dict,
        key_func: Optional[Callable],
        ignore_args: Optional[List[str]],
        namespace: str,
        ttl: int
    ):
        """Refresh cached result for function call."""
        cache_key = self._generate_cache_key(func, args, kwargs, key_func, ignore_args)
        result = func(*args, **kwargs)
        self.cache.set(cache_key, result, ttl, namespace)
        return result


class SessionCache:
    """User session caching."""
    
    def __init__(self, cache_manager: CacheManager):
        self.cache = cache_manager
        self.namespace = "sessions"
        self.default_ttl = 3600  # 1 hour
    
    def set_session(self, session_id: str, session_data: Dict[str, Any], ttl: Optional[int] = None):
        """Store session data."""
        session_ttl = ttl or self.default_ttl
        self.cache.set(session_id, session_data, session_ttl, self.namespace)
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve session data."""
        return self.cache.get(session_id, self.namespace)
    
    def update_session(self, session_id: str, updates: Dict[str, Any]):
        """Update session data."""
        session_data = self.get_session(session_id)
        if session_data:
            session_data.update(updates)
            # Get remaining TTL
            remaining_ttl = self.cache.ttl(session_id, self.namespace)
            if remaining_ttl > 0:
                self.cache.set(session_id, session_data, remaining_ttl, self.namespace)
    
    def delete_session(self, session_id: str):
        """Delete session data."""
        self.cache.delete(session_id, self.namespace)
    
    def extend_session(self, session_id: str, ttl: Optional[int] = None):
        """Extend session TTL."""
        session_ttl = ttl or self.default_ttl
        self.cache.expire(session_id, session_ttl, self.namespace)


# Global instances
_cache_manager: Optional[CacheManager] = None
_cache_decorator: Optional[CacheDecorator] = None
_session_cache: Optional[SessionCache] = None


def get_cache_manager() -> CacheManager:
    """Get the global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
        _cache_manager.initialize()
    return _cache_manager


def get_cache_decorator() -> CacheDecorator:
    """Get the global cache decorator instance."""
    global _cache_decorator
    if _cache_decorator is None:
        _cache_decorator = CacheDecorator(get_cache_manager())
    return _cache_decorator


def get_session_cache() -> SessionCache:
    """Get the global session cache instance."""
    global _session_cache
    if _session_cache is None:
        _session_cache = SessionCache(get_cache_manager())
    return _session_cache


# Convenience functions
def cache_key(namespace: str, *parts: str) -> str:
    """Generate a cache key from parts."""
    return f"{namespace}:{'_'.join(str(part) for part in parts)}"


def cached(ttl: int = 300, namespace: str = "functions", key_func: Optional[Callable] = None):
    """Decorator for caching function results."""
    return get_cache_decorator().cached(ttl, namespace, key_func)


def invalidate_cache(namespace: str, pattern: str = "*"):
    """Invalidate cache entries matching pattern."""
    cache = get_cache_manager()
    if pattern == "*":
        cache.clear_namespace(namespace)
    else:
        # For pattern matching, we'd need to implement a more sophisticated solution
        logger.warning(f"Pattern cache invalidation not implemented: {namespace}:{pattern}")


def set_cache(key: str, value: Any, ttl: Optional[int] = None, namespace: str = "default"):
    """Set a cache value."""
    return get_cache_manager().set(key, value, ttl, namespace)


def get_cache(key: str, namespace: str = "default", default: Any = None):
    """Get a cache value."""
    return get_cache_manager().get(key, namespace, default)


def delete_cache(key: str, namespace: str = "default"):
    """Delete a cache value."""
    return get_cache_manager().delete(key, namespace)
