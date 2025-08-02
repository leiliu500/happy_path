"""
Structured logging system for the Happy Path platform.
Provides centralized logging with multiple outputs, levels, and formats.
"""

import logging
import logging.handlers
import json
import sys
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional, Union
from contextvars import ContextVar

from .config import get_config
from .exceptions import ConfigurationError

# Context variables for request tracking
request_id_ctx: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id_ctx: ContextVar[Optional[str]] = ContextVar('user_id', default=None)


class LogLevel(Enum):
    """Logging levels."""
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        
        # Add context information
        request_id = request_id_ctx.get()
        if request_id:
            log_data["request_id"] = request_id
        
        user_id = user_id_ctx.get()
        if user_id:
            log_data["user_id"] = user_id
        
        # Add exception information
        if record.exc_info:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info)
            }
        
        # Add extra fields
        if hasattr(record, 'extra_data'):
            log_data.update(record.extra_data)
        
        return json.dumps(log_data)


class SecurityFilter(logging.Filter):
    """Filter to remove sensitive information from logs."""
    
    SENSITIVE_KEYS = {
        'password', 'token', 'secret', 'key', 'auth', 'credential',
        'card_number', 'ssn', 'social_security', 'credit_card'
    }
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter sensitive information from log records."""
        # Sanitize the message
        if isinstance(record.msg, str):
            record.msg = self._sanitize_message(record.msg)
        
        # Sanitize arguments
        if record.args:
            record.args = tuple(self._sanitize_value(arg) for arg in record.args)
        
        return True
    
    def _sanitize_message(self, message: str) -> str:
        """Sanitize sensitive information in message string."""
        # Simple pattern matching for common sensitive patterns
        import re
        
        # Credit card numbers (basic pattern)
        message = re.sub(r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b', '[CARD_REDACTED]', message)
        
        # Social security numbers
        message = re.sub(r'\b\d{3}[\s\-]?\d{2}[\s\-]?\d{4}\b', '[SSN_REDACTED]', message)
        
        # Email addresses (partial redaction)
        message = re.sub(r'([a-zA-Z0-9._%+-]+)@([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', r'***@\2', message)
        
        return message
    
    def _sanitize_value(self, value: Any) -> Any:
        """Sanitize sensitive values."""
        if isinstance(value, dict):
            return {k: ('[REDACTED]' if any(sensitive in k.lower() for sensitive in self.SENSITIVE_KEYS) else v) 
                   for k, v in value.items()}
        elif isinstance(value, str):
            return self._sanitize_message(value)
        return value


class HappyPathLogger:
    """Enhanced logger with context and security features."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self._extra_context: Dict[str, Any] = {}
    
    def set_context(self, **context):
        """Set additional context for logging."""
        self._extra_context.update(context)
    
    def clear_context(self):
        """Clear additional context."""
        self._extra_context.clear()
    
    def _log_with_context(self, level: int, message: str, *args, **kwargs):
        """Log with additional context."""
        extra_data = self._extra_context.copy()
        extra_data.update(kwargs.pop('extra_data', {}))
        
        # Create extra dict for logging
        extra = {'extra_data': extra_data}
        
        self.logger.log(level, message, *args, extra=extra, **kwargs)
    
    def debug(self, message: str, *args, **kwargs):
        """Log debug message."""
        self._log_with_context(logging.DEBUG, message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs):
        """Log info message."""
        self._log_with_context(logging.INFO, message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs):
        """Log warning message."""
        self._log_with_context(logging.WARNING, message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs):
        """Log error message."""
        self._log_with_context(logging.ERROR, message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs):
        """Log critical message."""
        self._log_with_context(logging.CRITICAL, message, *args, **kwargs)
    
    def exception(self, message: str, *args, **kwargs):
        """Log exception with traceback."""
        kwargs['exc_info'] = True
        self._log_with_context(logging.ERROR, message, *args, **kwargs)


def setup_logging(
    level: Optional[str] = None,
    enable_console: Optional[bool] = None,
    enable_file: Optional[bool] = None,
    file_path: Optional[str] = None,
    enable_json: Optional[bool] = None
) -> None:
    """Setup logging configuration."""
    config = get_config()
    
    # Use provided values or fall back to config
    log_level = level or config.logging.level
    console_enabled = enable_console if enable_console is not None else config.logging.enable_console
    file_enabled = enable_file if enable_file is not None else bool(config.logging.file_path)
    log_file = file_path or config.logging.file_path
    json_enabled = enable_json if enable_json is not None else config.logging.enable_json
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Create formatters
    if json_enabled:
        formatter = JSONFormatter()
    else:
        formatter = logging.Formatter(config.logging.format)
    
    # Create security filter
    security_filter = SecurityFilter()
    
    # Console handler
    if console_enabled:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        console_handler.addFilter(security_filter)
        root_logger.addHandler(console_handler)
    
    # File handler
    if file_enabled and log_file:
        try:
            # Ensure log directory exists
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Rotating file handler
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=config.logging.max_file_size,
                backupCount=config.logging.backup_count,
                encoding='utf-8'
            )
            file_handler.setFormatter(formatter)
            file_handler.addFilter(security_filter)
            root_logger.addHandler(file_handler)
            
        except Exception as e:
            raise ConfigurationError(f"Failed to setup file logging: {e}")
    
    # Setup application logger
    app_logger = logging.getLogger('happy_path')
    app_logger.setLevel(getattr(logging, log_level.upper()))
    
    # Log setup completion
    logger = get_logger(__name__)
    logger.info(f"Logging setup completed - Level: {log_level}, Console: {console_enabled}, File: {file_enabled}")


def get_logger(name: str) -> HappyPathLogger:
    """Get a logger instance with Happy Path enhancements."""
    return HappyPathLogger(name)


def set_request_context(request_id: str, user_id: Optional[str] = None):
    """Set request context for logging."""
    request_id_ctx.set(request_id)
    if user_id:
        user_id_ctx.set(user_id)


def clear_request_context():
    """Clear request context."""
    request_id_ctx.set(None)
    user_id_ctx.set(None)


class LoggingMiddleware:
    """Middleware for request/response logging."""
    
    def __init__(self, app):
        self.app = app
        self.logger = get_logger(__name__)
    
    async def __call__(self, scope, receive, send):
        """ASGI middleware implementation."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        # Generate request ID
        import uuid
        request_id = str(uuid.uuid4())
        
        # Extract request information
        method = scope["method"]
        path = scope["path"]
        query_string = scope.get("query_string", b"").decode()
        
        # Set logging context
        set_request_context(request_id)
        
        # Log request
        self.logger.info(
            f"Request started: {method} {path}",
            extra_data={
                "request_id": request_id,
                "method": method,
                "path": path,
                "query_string": query_string,
                "user_agent": dict(scope.get("headers", {})).get(b"user-agent", b"").decode()
            }
        )
        
        start_time = datetime.now(timezone.utc)
        
        # Process request
        try:
            await self.app(scope, receive, send)
            
        except Exception as e:
            # Log exception
            self.logger.exception(
                f"Request failed: {method} {path}",
                extra_data={
                    "request_id": request_id,
                    "error": str(e),
                    "error_type": type(e).__name__
                }
            )
            raise
        
        finally:
            # Calculate duration
            duration = (datetime.now(timezone.utc) - start_time).total_seconds()
            
            # Log completion
            self.logger.info(
                f"Request completed: {method} {path}",
                extra_data={
                    "request_id": request_id,
                    "duration_seconds": duration
                }
            )
            
            # Clear context
            clear_request_context()


# Performance logging decorator
def log_performance(func_name: Optional[str] = None):
    """Decorator to log function performance."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            logger = get_logger(func.__module__)
            name = func_name or f"{func.__module__}.{func.__name__}"
            
            start_time = datetime.now(timezone.utc)
            logger.debug(f"Starting {name}")
            
            try:
                result = func(*args, **kwargs)
                duration = (datetime.now(timezone.utc) - start_time).total_seconds()
                logger.debug(
                    f"Completed {name}",
                    extra_data={"duration_seconds": duration}
                )
                return result
                
            except Exception as e:
                duration = (datetime.now(timezone.utc) - start_time).total_seconds()
                logger.error(
                    f"Failed {name}: {e}",
                    extra_data={
                        "duration_seconds": duration,
                        "error_type": type(e).__name__
                    }
                )
                raise
        
        return wrapper
    return decorator
