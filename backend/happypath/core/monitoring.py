"""
Monitoring and health check system for the Happy Path platform.
Provides system metrics, performance monitoring, and health checks.
"""

import asyncio
import time
import psutil
import threading
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional, Callable
from dataclasses import dataclass, asdict
from collections import defaultdict, deque
import json

from .config import get_config
from .database import get_db_manager
from .logging import get_logger
from .exceptions import MonitoringError

logger = get_logger(__name__)


@dataclass
class HealthStatus:
    """Health check status information."""
    service: str
    status: str  # 'healthy', 'unhealthy', 'degraded'
    message: str
    timestamp: datetime
    response_time_ms: Optional[float] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class MetricData:
    """Metric data point."""
    name: str
    value: float
    timestamp: datetime
    tags: Dict[str, str]
    unit: str = ""


@dataclass
class SystemMetrics:
    """System performance metrics."""
    cpu_percent: float
    memory_percent: float
    memory_used_mb: float
    memory_available_mb: float
    disk_percent: float
    disk_used_gb: float
    disk_free_gb: float
    network_sent_mb: float
    network_recv_mb: float
    uptime_seconds: float
    load_average: List[float]
    timestamp: datetime


class HealthChecker:
    """System health monitoring and checks."""
    
    def __init__(self):
        self.config = get_config()
        self.checks: Dict[str, Callable[[], HealthStatus]] = {}
        self.last_check_results: Dict[str, HealthStatus] = {}
    
    def register_check(self, name: str, check_func: Callable[[], HealthStatus]):
        """Register a health check function."""
        self.checks[name] = check_func
        logger.info(f"Health check registered: {name}")
    
    def check_database(self) -> HealthStatus:
        """Check database connectivity and performance."""
        start_time = time.time()
        
        try:
            db_manager = get_db_manager()
            health_data = db_manager.get_health_status()
            
            response_time = (time.time() - start_time) * 1000
            
            if health_data.get("status") == "healthy":
                return HealthStatus(
                    service="database",
                    status="healthy",
                    message="Database is accessible and responsive",
                    timestamp=datetime.now(timezone.utc),
                    response_time_ms=response_time,
                    details=health_data
                )
            else:
                return HealthStatus(
                    service="database",
                    status="unhealthy",
                    message=f"Database health check failed: {health_data.get('error', 'Unknown error')}",
                    timestamp=datetime.now(timezone.utc),
                    response_time_ms=response_time,
                    details=health_data
                )
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            logger.error(f"Database health check failed: {e}")
            
            return HealthStatus(
                service="database",
                status="unhealthy",
                message=f"Database connection failed: {str(e)}",
                timestamp=datetime.now(timezone.utc),
                response_time_ms=response_time,
                details={"error": str(e)}
            )
    
    def check_redis(self) -> HealthStatus:
        """Check Redis connectivity and performance."""
        start_time = time.time()
        
        try:
            from .cache import get_cache_manager
            cache_manager = get_cache_manager()
            
            # Test Redis connection with a simple ping
            test_key = "health_check_test"
            cache_manager.set(test_key, "ping", ttl=5)
            result = cache_manager.get(test_key)
            cache_manager.delete(test_key)
            
            response_time = (time.time() - start_time) * 1000
            
            if result == "ping":
                return HealthStatus(
                    service="redis",
                    status="healthy",
                    message="Redis is accessible and responsive",
                    timestamp=datetime.now(timezone.utc),
                    response_time_ms=response_time
                )
            else:
                return HealthStatus(
                    service="redis",
                    status="unhealthy",
                    message="Redis ping test failed",
                    timestamp=datetime.now(timezone.utc),
                    response_time_ms=response_time
                )
                
        except Exception as e:
            response_time = (time.time() - start_time) * 1000
            logger.error(f"Redis health check failed: {e}")
            
            return HealthStatus(
                service="redis",
                status="unhealthy",
                message=f"Redis connection failed: {str(e)}",
                timestamp=datetime.now(timezone.utc),
                response_time_ms=response_time,
                details={"error": str(e)}
            )
    
    def check_system_resources(self) -> HealthStatus:
        """Check system resource usage."""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Define thresholds
            cpu_warning = 80
            cpu_critical = 95
            memory_warning = 85
            memory_critical = 95
            disk_warning = 85
            disk_critical = 95
            
            issues = []
            status = "healthy"
            
            # Check CPU
            if cpu_percent > cpu_critical:
                issues.append(f"CPU usage critical: {cpu_percent:.1f}%")
                status = "unhealthy"
            elif cpu_percent > cpu_warning:
                issues.append(f"CPU usage high: {cpu_percent:.1f}%")
                status = "degraded" if status == "healthy" else status
            
            # Check Memory
            if memory.percent > memory_critical:
                issues.append(f"Memory usage critical: {memory.percent:.1f}%")
                status = "unhealthy"
            elif memory.percent > memory_warning:
                issues.append(f"Memory usage high: {memory.percent:.1f}%")
                status = "degraded" if status == "healthy" else status
            
            # Check Disk
            if disk.percent > disk_critical:
                issues.append(f"Disk usage critical: {disk.percent:.1f}%")
                status = "unhealthy"
            elif disk.percent > disk_warning:
                issues.append(f"Disk usage high: {disk.percent:.1f}%")
                status = "degraded" if status == "healthy" else status
            
            message = "System resources are within normal limits"
            if issues:
                message = f"System resource issues detected: {'; '.join(issues)}"
            
            return HealthStatus(
                service="system_resources",
                status=status,
                message=message,
                timestamp=datetime.now(timezone.utc),
                details={
                    "cpu_percent": cpu_percent,
                    "memory_percent": memory.percent,
                    "disk_percent": disk.percent,
                    "memory_available_gb": memory.available / (1024**3),
                    "disk_free_gb": disk.free / (1024**3)
                }
            )
            
        except Exception as e:
            logger.error(f"System resource check failed: {e}")
            return HealthStatus(
                service="system_resources",
                status="unhealthy",
                message=f"System resource check failed: {str(e)}",
                timestamp=datetime.now(timezone.utc),
                details={"error": str(e)}
            )
    
    def run_all_checks(self) -> Dict[str, HealthStatus]:
        """Run all registered health checks."""
        results = {}
        
        # Default checks
        default_checks = {
            "database": self.check_database,
            "redis": self.check_redis,
            "system_resources": self.check_system_resources
        }
        
        # Combine with registered checks
        all_checks = {**default_checks, **self.checks}
        
        for name, check_func in all_checks.items():
            try:
                result = check_func()
                results[name] = result
                self.last_check_results[name] = result
                
            except Exception as e:
                logger.error(f"Health check {name} failed: {e}")
                result = HealthStatus(
                    service=name,
                    status="unhealthy",
                    message=f"Health check failed: {str(e)}",
                    timestamp=datetime.now(timezone.utc),
                    details={"error": str(e)}
                )
                results[name] = result
                self.last_check_results[name] = result
        
        return results
    
    def get_overall_status(self) -> Dict[str, Any]:
        """Get overall system health status."""
        results = self.run_all_checks()
        
        unhealthy_services = [name for name, status in results.items() if status.status == "unhealthy"]
        degraded_services = [name for name, status in results.items() if status.status == "degraded"]
        
        if unhealthy_services:
            overall_status = "unhealthy"
            message = f"System is unhealthy. Failed services: {', '.join(unhealthy_services)}"
        elif degraded_services:
            overall_status = "degraded"
            message = f"System is degraded. Affected services: {', '.join(degraded_services)}"
        else:
            overall_status = "healthy"
            message = "All systems are healthy"
        
        return {
            "status": overall_status,
            "message": message,
            "timestamp": datetime.now(timezone.utc),
            "services": {name: asdict(status) for name, status in results.items()},
            "summary": {
                "total_services": len(results),
                "healthy_services": len([s for s in results.values() if s.status == "healthy"]),
                "degraded_services": len(degraded_services),
                "unhealthy_services": len(unhealthy_services)
            }
        }


class MetricsCollector:
    """System metrics collection and storage."""
    
    def __init__(self, max_data_points: int = 1000):
        self.max_data_points = max_data_points
        self.metrics_data: Dict[str, deque] = defaultdict(lambda: deque(maxlen=max_data_points))
        self.start_time = time.time()
        self._lock = threading.Lock()
    
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics."""
        try:
            # CPU metrics
            cpu_percent = psutil.cpu_percent(interval=0.1)
            
            # Memory metrics
            memory = psutil.virtual_memory()
            
            # Disk metrics
            disk = psutil.disk_usage('/')
            
            # Network metrics
            network = psutil.net_io_counters()
            
            # System uptime
            uptime = time.time() - self.start_time
            
            # Load average (Unix-like systems)
            try:
                load_avg = list(psutil.getloadavg())
            except AttributeError:
                load_avg = [0.0, 0.0, 0.0]  # Windows doesn't have load average
            
            return SystemMetrics(
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_used_mb=memory.used / (1024**2),
                memory_available_mb=memory.available / (1024**2),
                disk_percent=disk.percent,
                disk_used_gb=disk.used / (1024**3),
                disk_free_gb=disk.free / (1024**3),
                network_sent_mb=network.bytes_sent / (1024**2),
                network_recv_mb=network.bytes_recv / (1024**2),
                uptime_seconds=uptime,
                load_average=load_avg,
                timestamp=datetime.now(timezone.utc)
            )
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            raise MonitoringError(f"System metrics collection failed: {e}")
    
    def record_metric(self, name: str, value: float, tags: Optional[Dict[str, str]] = None, unit: str = ""):
        """Record a custom metric."""
        metric = MetricData(
            name=name,
            value=value,
            timestamp=datetime.now(timezone.utc),
            tags=tags or {},
            unit=unit
        )
        
        with self._lock:
            self.metrics_data[name].append(metric)
    
    def record_counter(self, name: str, tags: Optional[Dict[str, str]] = None):
        """Record a counter metric (increment by 1)."""
        self.record_metric(name, 1.0, tags, "count")
    
    def record_timer(self, name: str, duration_seconds: float, tags: Optional[Dict[str, str]] = None):
        """Record a timing metric."""
        self.record_metric(name, duration_seconds, tags, "seconds")
    
    def record_gauge(self, name: str, value: float, tags: Optional[Dict[str, str]] = None, unit: str = ""):
        """Record a gauge metric (current value)."""
        self.record_metric(name, value, tags, unit)
    
    def get_metrics_summary(self, hours: int = 1) -> Dict[str, Any]:
        """Get summary of metrics for the specified time period."""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        summary = {}
        
        with self._lock:
            for metric_name, data_points in self.metrics_data.items():
                recent_points = [
                    point for point in data_points 
                    if point.timestamp >= cutoff_time
                ]
                
                if recent_points:
                    values = [point.value for point in recent_points]
                    summary[metric_name] = {
                        "count": len(values),
                        "min": min(values),
                        "max": max(values),
                        "avg": sum(values) / len(values),
                        "latest": values[-1],
                        "unit": recent_points[-1].unit
                    }
        
        return summary
    
    def get_metric_history(self, metric_name: str, hours: int = 24) -> List[Dict[str, Any]]:
        """Get historical data for a specific metric."""
        cutoff_time = datetime.now(timezone.utc) - timedelta(hours=hours)
        
        with self._lock:
            if metric_name not in self.metrics_data:
                return []
            
            return [
                {
                    "timestamp": point.timestamp.isoformat(),
                    "value": point.value,
                    "tags": point.tags,
                    "unit": point.unit
                }
                for point in self.metrics_data[metric_name]
                if point.timestamp >= cutoff_time
            ]


class PerformanceMonitor:
    """Performance monitoring with context managers and decorators."""
    
    def __init__(self, metrics_collector: MetricsCollector):
        self.metrics = metrics_collector
    
    def timer(self, name: str, tags: Optional[Dict[str, str]] = None):
        """Context manager for timing operations."""
        return TimerContext(self.metrics, name, tags)
    
    def counter(self, name: str, tags: Optional[Dict[str, str]] = None):
        """Context manager for counting operations."""
        return CounterContext(self.metrics, name, tags)
    
    def monitor_function(self, name: Optional[str] = None, tags: Optional[Dict[str, str]] = None):
        """Decorator for monitoring function performance."""
        def decorator(func):
            def wrapper(*args, **kwargs):
                metric_name = name or f"{func.__module__}.{func.__name__}"
                
                with self.timer(f"{metric_name}.duration", tags):
                    try:
                        result = func(*args, **kwargs)
                        self.metrics.record_counter(f"{metric_name}.success", tags)
                        return result
                    except Exception as e:
                        self.metrics.record_counter(f"{metric_name}.error", {**(tags or {}), "error_type": type(e).__name__})
                        raise
            
            return wrapper
        return decorator


class TimerContext:
    """Context manager for timing operations."""
    
    def __init__(self, metrics_collector: MetricsCollector, name: str, tags: Optional[Dict[str, str]] = None):
        self.metrics = metrics_collector
        self.name = name
        self.tags = tags
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.start_time:
            duration = time.time() - self.start_time
            self.metrics.record_timer(self.name, duration, self.tags)


class CounterContext:
    """Context manager for counting operations."""
    
    def __init__(self, metrics_collector: MetricsCollector, name: str, tags: Optional[Dict[str, str]] = None):
        self.metrics = metrics_collector
        self.name = name
        self.tags = tags
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.metrics.record_counter(self.name, self.tags)


# Global instances
_health_checker: Optional[HealthChecker] = None
_metrics_collector: Optional[MetricsCollector] = None
_performance_monitor: Optional[PerformanceMonitor] = None


def get_health_checker() -> HealthChecker:
    """Get the global health checker instance."""
    global _health_checker
    if _health_checker is None:
        _health_checker = HealthChecker()
    return _health_checker


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance."""
    global _metrics_collector
    if _metrics_collector is None:
        _metrics_collector = MetricsCollector()
    return _metrics_collector


def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance."""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor(get_metrics_collector())
    return _performance_monitor


# Monitoring middleware for web applications
class MonitoringMiddleware:
    """ASGI middleware for request monitoring."""
    
    def __init__(self, app):
        self.app = app
        self.metrics = get_metrics_collector()
        self.performance = get_performance_monitor()
        self.logger = get_logger(__name__)
    
    async def __call__(self, scope, receive, send):
        """ASGI middleware implementation."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        
        method = scope["method"]
        path = scope["path"]
        
        # Track request metrics
        with self.performance.timer("http_request_duration", {"method": method, "path": path}):
            with self.performance.counter("http_requests_total", {"method": method, "path": path}):
                try:
                    await self.app(scope, receive, send)
                    
                except Exception as e:
                    # Track error metrics
                    self.metrics.record_counter(
                        "http_request_errors_total",
                        {"method": method, "path": path, "error_type": type(e).__name__}
                    )
                    raise
