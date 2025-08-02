"""
Simple rate limiter for the Telegram bot.

This module provides a thread-safe rate limiter to prevent spam
and ensure fair usage of the AI agent system.
"""

import time
import threading
from collections import defaultdict, deque
from typing import Dict
from src.core.config import config


class RateLimiter:
    """
    Thread-safe rate limiter using sliding window approach.
    
    Tracks requests per user ID and enforces limits based on configuration.
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        self._user_requests: Dict[int, deque] = defaultdict(deque)
    
    def is_allowed(self, user_id: int) -> bool:
        """
        Check if user is allowed to make a request.
        
        Args:
            user_id (int): Telegram user ID
            
        Returns:
            bool: True if request is allowed, False if rate limited
        """
        with self._lock:
            now = time.time()
            window_start = now - config.RATE_LIMIT_WINDOW
            
            # Get user's request history
            user_queue = self._user_requests[user_id]
            
            # Remove old requests outside the time window
            while user_queue and user_queue[0] < window_start:
                user_queue.popleft()
            
            # Check if under limit
            if len(user_queue) < config.RATE_LIMIT_PER_USER:
                user_queue.append(now)
                return True
            
            return False
    
    def get_reset_time(self, user_id: int) -> float:
        """
        Get time until rate limit resets for user.
        
        Args:
            user_id (int): Telegram user ID
            
        Returns:
            float: Seconds until oldest request expires
        """
        with self._lock:
            user_queue = self._user_requests[user_id]
            if not user_queue:
                return 0.0
            
            oldest_request = user_queue[0]
            reset_time = oldest_request + config.RATE_LIMIT_WINDOW
            return max(0.0, reset_time - time.time())


# Global rate limiter instance
rate_limiter = RateLimiter()