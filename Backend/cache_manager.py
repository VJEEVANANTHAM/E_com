import redis
import json
from typing import Optional, Any
from config import (
    REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD, CACHE_TTL
)


class CacheManager:
    """Redis-based cache manager for general purpose caching."""
    
    def __init__(self):
        """Initialize Redis connection."""
        try:
            self.redis_client = redis.Redis(
                host=REDIS_HOST,
                port=REDIS_PORT,
                db=REDIS_DB,
                password=REDIS_PASSWORD,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_keepalive=True
            )
            self.redis_client.ping()
            print("✓ Cache manager connected to Redis")
        except redis.ConnectionError as e:
            print(f"✗ Failed to connect to Redis: {e}")
            raise
    
    def get(self, key: str) -> Optional[Any]:
        """
        Retrieve a cached value.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found
        """
        cached_value = self.redis_client.get(key)
        if cached_value:
            try:
                return json.loads(cached_value)
            except json.JSONDecodeError:
                return cached_value
        return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Store a value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (defaults to CACHE_TTL)
            
        Returns:
            True if successful
        """
        ttl = ttl or CACHE_TTL
        try:
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            self.redis_client.setex(key, ttl, value)
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Delete a cached value.
        
        Args:
            key: Cache key
            
        Returns:
            True if deleted, False if not found
        """
        result = self.redis_client.delete(key)
        return result > 0
    
    def exists(self, key: str) -> bool:
        """Check if a key exists in cache."""
        return self.redis_client.exists(key) > 0
    
    def clear_pattern(self, pattern: str) -> int:
        """
        Delete all keys matching a pattern.
        
        Args:
            pattern: Redis glob pattern (e.g., "product:*")
            
        Returns:
            Number of keys deleted
        """
        deleted_count = 0
        for key in self.redis_client.scan_iter(pattern):
            self.redis_client.delete(key)
            deleted_count += 1
        return deleted_count
    
    def flush_all(self) -> bool:
        """Clear all cache. Use with caution!"""
        try:
            self.redis_client.flushdb()
            return True
        except Exception as e:
            print(f"Flush error: {e}")
            return False
    
    def get_ttl(self, key: str) -> Optional[int]:
        """Get remaining TTL for a key in seconds."""
        ttl = self.redis_client.ttl(key)
        return ttl if ttl >= 0 else None
    
    def increment(self, key: str, amount: int = 1, ttl: Optional[int] = None) -> int:
        """
        Increment a counter value.
        
        Args:
            key: Cache key
            amount: Amount to increment
            ttl: Set TTL if incrementing creates the key
            
        Returns:
            New value
        """
        value = self.redis_client.incrby(key, amount)
        if ttl and not self.redis_client.ttl(key) > 0:
            self.redis_client.expire(key, ttl)
        return value
    
    def decrement(self, key: str, amount: int = 1) -> int:
        """Decrement a counter value."""
        return self.redis_client.decrby(key, amount)


# Global cache manager instance
_cache_manager: Optional[CacheManager] = None


def get_cache_manager() -> CacheManager:
    """Get or create the global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager
