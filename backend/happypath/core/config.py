"""
Configuration management for the Happy Path platform.
Handles environment-based settings, secrets, and feature flags.
"""

import os
import json
from enum import Enum
from typing import Any, Dict, Optional, Union
from dataclasses import dataclass, field
from pathlib import Path

from .exceptions import ConfigurationError


class Environment(Enum):
    """Application environments."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class DatabaseConfig:
    """Database configuration settings."""
    host: str = "localhost"
    port: int = 5432
    database: str = "happy_path"
    username: str = "postgres"
    password: str = ""
    pool_size: int = 20
    max_overflow: int = 30
    pool_timeout: int = 30
    ssl_mode: str = "prefer"
    application_name: str = "happy_path"


@dataclass
class RedisConfig:
    """Redis cache configuration."""
    host: str = "localhost"
    port: int = 6379
    database: int = 0
    password: Optional[str] = None
    ssl: bool = False
    pool_size: int = 10
    timeout: int = 5


@dataclass
class SecurityConfig:
    """Security configuration settings."""
    secret_key: str = ""
    jwt_secret: str = ""
    jwt_expiry_hours: int = 24
    password_min_length: int = 8
    password_require_special: bool = True
    session_timeout_minutes: int = 60
    max_login_attempts: int = 5
    lockout_duration_minutes: int = 30
    encryption_key: str = ""
    enable_2fa: bool = True


@dataclass
class LoggingConfig:
    """Logging configuration settings."""
    level: str = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    file_path: Optional[str] = None
    max_file_size: int = 100 * 1024 * 1024  # 100MB
    backup_count: int = 5
    enable_json: bool = False
    enable_console: bool = True


@dataclass
class MonitoringConfig:
    """Monitoring and metrics configuration."""
    enable_metrics: bool = True
    metrics_port: int = 9090
    health_check_interval: int = 30
    performance_tracking: bool = True
    alert_email: Optional[str] = None
    prometheus_enabled: bool = False


@dataclass
class PaymentConfig:
    """Payment processing configuration."""
    stripe_public_key: str = ""
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    enable_test_mode: bool = True
    currency: str = "USD"
    tax_rate: float = 0.0


@dataclass
class FeatureFlags:
    """Feature flag configuration."""
    enable_ai_insights: bool = True
    enable_provider_coordination: bool = True
    enable_crisis_detection: bool = True
    enable_medication_tracking: bool = True
    enable_analytics: bool = True
    enable_premium_features: bool = True
    enable_notifications: bool = True
    enable_audit_logging: bool = True


class Config:
    """Main configuration class for the Happy Path platform."""
    
    def __init__(self, env: Optional[Environment] = None):
        self.env = env or self._detect_environment()
        self.database = DatabaseConfig()
        self.redis = RedisConfig()
        self.security = SecurityConfig()
        self.logging = LoggingConfig()
        self.monitoring = MonitoringConfig()
        self.payment = PaymentConfig()
        self.features = FeatureFlags()
        
        # Load configuration from environment
        self._load_from_environment()
        self._load_from_file()
        self._validate_config()
    
    def _detect_environment(self) -> Environment:
        """Detect current environment from environment variables."""
        env_name = os.getenv("HAPPY_PATH_ENV", "development").lower()
        try:
            return Environment(env_name)
        except ValueError:
            return Environment.DEVELOPMENT
    
    def _load_from_environment(self):
        """Load configuration from environment variables."""
        # Database configuration
        self.database.host = os.getenv("DB_HOST", self.database.host)
        self.database.port = int(os.getenv("DB_PORT", self.database.port))
        self.database.database = os.getenv("DB_NAME", self.database.database)
        self.database.username = os.getenv("DB_USER", self.database.username)
        self.database.password = os.getenv("DB_PASSWORD", self.database.password)
        self.database.pool_size = int(os.getenv("DB_POOL_SIZE", self.database.pool_size))
        
        # Redis configuration
        self.redis.host = os.getenv("REDIS_HOST", self.redis.host)
        self.redis.port = int(os.getenv("REDIS_PORT", self.redis.port))
        self.redis.database = int(os.getenv("REDIS_DB", self.redis.database))
        self.redis.password = os.getenv("REDIS_PASSWORD", self.redis.password)
        
        # Security configuration
        self.security.secret_key = os.getenv("SECRET_KEY", self.security.secret_key)
        self.security.jwt_secret = os.getenv("JWT_SECRET", self.security.jwt_secret)
        self.security.encryption_key = os.getenv("ENCRYPTION_KEY", self.security.encryption_key)
        
        # Payment configuration
        self.payment.stripe_public_key = os.getenv("STRIPE_PUBLIC_KEY", self.payment.stripe_public_key)
        self.payment.stripe_secret_key = os.getenv("STRIPE_SECRET_KEY", self.payment.stripe_secret_key)
        self.payment.stripe_webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET", self.payment.stripe_webhook_secret)
        
        # Logging configuration
        self.logging.level = os.getenv("LOG_LEVEL", self.logging.level)
        self.logging.file_path = os.getenv("LOG_FILE_PATH", self.logging.file_path)
        
        # Feature flags
        self.features.enable_ai_insights = self._get_bool_env("ENABLE_AI_INSIGHTS", self.features.enable_ai_insights)
        self.features.enable_crisis_detection = self._get_bool_env("ENABLE_CRISIS_DETECTION", self.features.enable_crisis_detection)
        self.features.enable_audit_logging = self._get_bool_env("ENABLE_AUDIT_LOGGING", self.features.enable_audit_logging)
    
    def _get_bool_env(self, key: str, default: bool) -> bool:
        """Get boolean value from environment variable."""
        value = os.getenv(key, str(default)).lower()
        return value in ("true", "1", "yes", "on")
    
    def _load_from_file(self):
        """Load configuration from JSON file if it exists."""
        config_file = Path(f"config/{self.env.value}.json")
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    file_config = json.load(f)
                self._merge_config(file_config)
            except (json.JSONDecodeError, IOError) as e:
                raise ConfigurationError(f"Failed to load config file {config_file}: {e}")
    
    def _merge_config(self, file_config: Dict[str, Any]):
        """Merge configuration from file with current config."""
        if "database" in file_config:
            for key, value in file_config["database"].items():
                if hasattr(self.database, key):
                    setattr(self.database, key, value)
        
        if "redis" in file_config:
            for key, value in file_config["redis"].items():
                if hasattr(self.redis, key):
                    setattr(self.redis, key, value)
        
        if "security" in file_config:
            for key, value in file_config["security"].items():
                if hasattr(self.security, key):
                    setattr(self.security, key, value)
        
        if "logging" in file_config:
            for key, value in file_config["logging"].items():
                if hasattr(self.logging, key):
                    setattr(self.logging, key, value)
        
        if "features" in file_config:
            for key, value in file_config["features"].items():
                if hasattr(self.features, key):
                    setattr(self.features, key, value)
    
    def _validate_config(self):
        """Validate configuration settings."""
        errors = []
        
        # Validate required security settings for production
        if self.env == Environment.PRODUCTION:
            if not self.security.secret_key:
                errors.append("SECRET_KEY is required for production")
            if not self.security.jwt_secret:
                errors.append("JWT_SECRET is required for production")
            if not self.security.encryption_key:
                errors.append("ENCRYPTION_KEY is required for production")
            if not self.database.password:
                errors.append("Database password is required for production")
        
        # Validate database configuration
        if not self.database.host:
            errors.append("Database host is required")
        if not self.database.database:
            errors.append("Database name is required")
        
        # Validate payment configuration if payment features are enabled
        if self.features.enable_premium_features:
            if not self.payment.stripe_secret_key:
                errors.append("Stripe secret key is required when premium features are enabled")
        
        if errors:
            raise ConfigurationError(f"Configuration validation failed: {'; '.join(errors)}")
    
    def get_database_url(self) -> str:
        """Get database connection URL."""
        password_part = f":{self.database.password}" if self.database.password else ""
        return (
            f"postgresql://{self.database.username}{password_part}@"
            f"{self.database.host}:{self.database.port}/{self.database.database}"
        )
    
    def get_redis_url(self) -> str:
        """Get Redis connection URL."""
        password_part = f":{self.redis.password}@" if self.redis.password else ""
        protocol = "rediss" if self.redis.ssl else "redis"
        return f"{protocol}://{password_part}{self.redis.host}:{self.redis.port}/{self.redis.database}"
    
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.env == Environment.DEVELOPMENT
    
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.env == Environment.PRODUCTION
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary (excluding sensitive data)."""
        return {
            "environment": self.env.value,
            "database": {
                "host": self.database.host,
                "port": self.database.port,
                "database": self.database.database,
                "username": self.database.username,
                "pool_size": self.database.pool_size,
            },
            "redis": {
                "host": self.redis.host,
                "port": self.redis.port,
                "database": self.redis.database,
            },
            "logging": {
                "level": self.logging.level,
                "enable_console": self.logging.enable_console,
                "enable_json": self.logging.enable_json,
            },
            "features": {
                "enable_ai_insights": self.features.enable_ai_insights,
                "enable_provider_coordination": self.features.enable_provider_coordination,
                "enable_crisis_detection": self.features.enable_crisis_detection,
                "enable_medication_tracking": self.features.enable_medication_tracking,
                "enable_analytics": self.features.enable_analytics,
            }
        }


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def initialize_config(env: Optional[Environment] = None) -> Config:
    """Initialize the global configuration."""
    global _config
    _config = Config(env)
    return _config
