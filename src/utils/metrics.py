"""
Performance metrics and monitoring utilities.
"""
import time
import functools
from typing import Dict, Any, Callable
from src.utils.logging_config import get_logger

logger = get_logger(__name__)


def measure_time(func: Callable) -> Callable:
    """Decorator to measure function execution time."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        execution_time = end_time - start_time
        logger.info(f"{func.__name__} executed in {execution_time:.2f} seconds")
        
        return result
    return wrapper


class MetricsCollector:
    """Collect and track system performance metrics."""
    
    def __init__(self):
        self.metrics = {
            "query_count": 0,
            "total_response_time": 0,
            "average_response_time": 0,
            "error_count": 0,
            "embedding_cache_hits": 0,
            "embedding_cache_misses": 0
        }
    
    def record_query(self, response_time: float, error: bool = False):
        """Record a query execution."""
        self.metrics["query_count"] += 1
        
        if error:
            self.metrics["error_count"] += 1
        else:
            self.metrics["total_response_time"] += response_time
            self.metrics["average_response_time"] = (
                self.metrics["total_response_time"] / 
                (self.metrics["query_count"] - self.metrics["error_count"])
            )
    
    def record_cache_hit(self):
        """Record an embedding cache hit."""
        self.metrics["embedding_cache_hits"] += 1
    
    def record_cache_miss(self):
        """Record an embedding cache miss."""
        self.metrics["embedding_cache_misses"] += 1
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics."""
        cache_total = self.metrics["embedding_cache_hits"] + self.metrics["embedding_cache_misses"]
        cache_hit_rate = (
            self.metrics["embedding_cache_hits"] / cache_total 
            if cache_total > 0 else 0
        )
        
        return {
            **self.metrics,
            "cache_hit_rate": cache_hit_rate,
            "error_rate": (
                self.metrics["error_count"] / self.metrics["query_count"]
                if self.metrics["query_count"] > 0 else 0
            )
        }
    
    def reset_metrics(self):
        """Reset all metrics."""
        self.metrics = {key: 0 for key in self.metrics}


# Global metrics collector instance
metrics_collector = MetricsCollector()
