"""
Performance Optimization Utilities
Caching, lazy loading, and performance monitoring
"""

import streamlit as st
import time
import functools
from typing import Any, Callable, Dict, Optional
import hashlib
import json

class PerformanceMonitor:
    """Monitor and track performance metrics"""
    
    def __init__(self):
        self.metrics = {}
        self.start_times = {}
    
    def start_timer(self, operation: str):
        """Start timing an operation"""
        self.start_times[operation] = time.time()
    
    def end_timer(self, operation: str) -> float:
        """End timing and record duration"""
        if operation not in self.start_times:
            return 0.0
        
        duration = time.time() - self.start_times[operation]
        
        if operation not in self.metrics:
            self.metrics[operation] = []
        
        self.metrics[operation].append(duration)
        del self.start_times[operation]
        
        return duration
    
    def get_average(self, operation: str) -> float:
        """Get average duration for operation"""
        if operation not in self.metrics or not self.metrics[operation]:
            return 0.0
        
        return sum(self.metrics[operation]) / len(self.metrics[operation])
    
    def get_stats(self) -> Dict[str, Dict[str, float]]:
        """Get statistics for all operations"""
        stats = {}
        
        for operation, durations in self.metrics.items():
            if durations:
                stats[operation] = {
                    'count': len(durations),
                    'total': sum(durations),
                    'average': sum(durations) / len(durations),
                    'min': min(durations),
                    'max': max(durations)
                }
        
        return stats
    
    def clear(self):
        """Clear all metrics"""
        self.metrics.clear()
        self.start_times.clear()


def cache_result(ttl: int = 300):
    """
    Cache function results with time-to-live
    
    Args:
        ttl: Time to live in seconds (default 5 minutes)
    """
    def decorator(func: Callable) -> Callable:
        cache = {}
        cache_times = {}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key
            key_data = {
                'args': args,
                'kwargs': kwargs
            }
            cache_key = hashlib.md5(
                json.dumps(key_data, sort_keys=True, default=str).encode()
            ).hexdigest()
            
            # Check cache
            current_time = time.time()
            
            if cache_key in cache:
                cache_time = cache_times.get(cache_key, 0)
                
                # Return cached result if still valid
                if current_time - cache_time < ttl:
                    return cache[cache_key]
            
            # Compute result
            result = func(*args, **kwargs)
            
            # Store in cache
            cache[cache_key] = result
            cache_times[cache_key] = current_time
            
            # Clean old entries
            if len(cache) > 100:  # Limit cache size
                oldest_key = min(cache_times, key=cache_times.get)
                del cache[oldest_key]
                del cache_times[oldest_key]
            
            return result
        
        return wrapper
    
    return decorator


def lazy_load(func: Callable) -> Callable:
    """
    Lazy load function - only execute when needed
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Check if already loaded in session state
        cache_key = f"lazy_{func.__name__}"
        
        if cache_key not in st.session_state:
            st.session_state[cache_key] = func(*args, **kwargs)
        
        return st.session_state[cache_key]
    
    return wrapper


def debounce(wait: float = 0.5):
    """
    Debounce function calls
    
    Args:
        wait: Wait time in seconds
    """
    def decorator(func: Callable) -> Callable:
        last_call = {'time': 0}
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            current_time = time.time()
            
            if current_time - last_call['time'] >= wait:
                last_call['time'] = current_time
                return func(*args, **kwargs)
            
            return None
        
        return wrapper
    
    return decorator


def optimize_dataframe(df):
    """
    Optimize pandas DataFrame memory usage
    
    Args:
        df: Pandas DataFrame
        
    Returns:
        Optimized DataFrame
    """
    for col in df.columns:
        col_type = df[col].dtype
        
        if col_type == 'object':
            # Convert to category if few unique values
            num_unique = df[col].nunique()
            num_total = len(df[col])
            
            if num_unique / num_total < 0.5:
                df[col] = df[col].astype('category')
        
        elif col_type == 'int64':
            # Downcast integers
            df[col] = df[col].astype('int32')
        
        elif col_type == 'float64':
            # Downcast floats
            df[col] = df[col].astype('float32')
    
    return df


def batch_process(items: list, batch_size: int = 100, 
                  process_func: Callable = None):
    """
    Process items in batches for better performance
    
    Args:
        items: List of items to process
        batch_size: Size of each batch
        process_func: Function to process each batch
        
    Yields:
        Processed batches
    """
    for i in range(0, len(items), batch_size):
        batch = items[i:i + batch_size]
        
        if process_func:
            yield process_func(batch)
        else:
            yield batch


class LoadingState:
    """Manage loading states with spinners"""
    
    def __init__(self, message: str = "Loading..."):
        self.message = message
        self.spinner = None
    
    def __enter__(self):
        self.spinner = st.spinner(self.message)
        self.spinner.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.spinner:
            self.spinner.__exit__(exc_type, exc_val, exc_tb)
    
    def update(self, message: str):
        """Update loading message"""
        self.message = message


def measure_performance(func: Callable) -> Callable:
    """
    Decorator to measure function performance
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        duration = time.time() - start_time
        
        # Store in session state
        if 'performance_metrics' not in st.session_state:
            st.session_state['performance_metrics'] = {}
        
        if func.__name__ not in st.session_state['performance_metrics']:
            st.session_state['performance_metrics'][func.__name__] = []
        
        st.session_state['performance_metrics'][func.__name__].append(duration)
        
        return result
    
    return wrapper


def get_performance_report() -> Dict[str, Any]:
    """
    Get performance report for all measured functions
    
    Returns:
        Dictionary with performance statistics
    """
    if 'performance_metrics' not in st.session_state:
        return {}
    
    report = {}
    
    for func_name, durations in st.session_state['performance_metrics'].items():
        if durations:
            report[func_name] = {
                'calls': len(durations),
                'total_time': sum(durations),
                'avg_time': sum(durations) / len(durations),
                'min_time': min(durations),
                'max_time': max(durations)
            }
    
    return report


def clear_cache():
    """Clear all Streamlit caches"""
    st.cache_data.clear()
    st.cache_resource.clear()


def optimize_images(image_path: str, max_size: tuple = (800, 600)) -> str:
    """
    Optimize image for web display
    
    Args:
        image_path: Path to image
        max_size: Maximum dimensions (width, height)
        
    Returns:
        Path to optimized image
    """
    try:
        from PIL import Image
        
        img = Image.open(image_path)
        
        # Resize if needed
        if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
            img.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save optimized
        optimized_path = image_path.replace('.', '_optimized.')
        img.save(optimized_path, optimize=True, quality=85)
        
        return optimized_path
    
    except ImportError:
        return image_path


# Singleton performance monitor
_monitor = None

def get_performance_monitor() -> PerformanceMonitor:
    """Get singleton performance monitor"""
    global _monitor
    if _monitor is None:
        _monitor = PerformanceMonitor()
    return _monitor
