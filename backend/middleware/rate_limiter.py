from flask import request, jsonify
from functools import wraps
import time
from collections import defaultdict
from threading import Lock

# In-memory store for rate limiting
request_counts = defaultdict(list)
lock = Lock()

def rate_limit(max_requests=100, window_seconds=60):
    """
    Rate limiting decorator
    Args:
        max_requests: Maximum number of requests allowed
        window_seconds: Time window in seconds
    """
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            # Get client identifier (IP + endpoint)
            client_ip = request.remote_addr
            endpoint = request.endpoint or 'unknown'
            client_key = f"{client_ip}:{endpoint}"
            
            # Get current time
            now = time.time()
            
            with lock:
                # Initialize or get request history
                if client_key not in request_counts:
                    request_counts[client_key] = []
                
                # Remove old requests outside the window
                request_counts[client_key] = [
                    req_time for req_time in request_counts[client_key]
                    if now - req_time < window_seconds
                ]
                
                # Check if limit exceeded
                if len(request_counts[client_key]) >= max_requests:
                    retry_after = int(window_seconds - (now - request_counts[client_key][0]))
                    return jsonify({
                        'error': 'Rate limit exceeded',
                        'message': f'Too many requests. Please try again in {retry_after} seconds.',
                        'retry_after': retry_after
                    }), 429
                
                # Add current request
                request_counts[client_key].append(now)
            
            return f(*args, **kwargs)
        
        return decorated
    return decorator

def cleanup_old_entries():
    """Cleanup old entries from rate limiter (call periodically)"""
    now = time.time()
    with lock:
        for key in list(request_counts.keys()):
            request_counts[key] = [
                req_time for req_time in request_counts[key]
                if now - req_time < 3600  # Keep last hour
            ]
            if not request_counts[key]:
                del request_counts[key]