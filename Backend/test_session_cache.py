"""
Test suite for Session and Cache managers.

Run with: pytest tests/test_session_cache.py -v
"""

import pytest
from fastapi.testclient import TestClient
from session_manager import SessionManager, get_session_manager
from cache_manager import CacheManager, get_cache_manager
import json
import time


class TestSessionManager:
    """Test SessionManager functionality."""
    
    @pytest.fixture
    def session_manager(self):
        """Create a session manager instance."""
        return SessionManager()
    
    def test_create_session(self, session_manager):
        """Test creating a new session."""
        user_data = {"email": "test@example.com", "username": "testuser"}
        session_id = session_manager.create_session("user123", user_data)
        
        assert session_id is not None
        assert isinstance(session_id, str)
        assert len(session_id) == 36  # UUID length
    
    def test_get_session(self, session_manager):
        """Test retrieving session data."""
        user_data = {"email": "test@example.com", "username": "testuser"}
        session_id = session_manager.create_session("user123", user_data)
        
        retrieved = session_manager.get_session(session_id)
        
        assert retrieved is not None
        assert retrieved["user_id"] == "user123"
        assert retrieved["email"] == "test@example.com"
        assert retrieved["username"] == "testuser"
        assert "created_at" in retrieved
        assert "last_accessed" in retrieved
    
    def test_get_nonexistent_session(self, session_manager):
        """Test getting a non-existent session."""
        result = session_manager.get_session("nonexistent-id")
        assert result is None
    
    def test_update_session(self, session_manager):
        """Test updating session data."""
        user_data = {"email": "test@example.com", "username": "testuser"}
        session_id = session_manager.create_session("user123", user_data)
        
        success = session_manager.update_session(session_id, {"role": "admin"})
        assert success is True
        
        updated = session_manager.get_session(session_id)
        assert updated["role"] == "admin"
    
    def test_delete_session(self, session_manager):
        """Test deleting a session."""
        user_data = {"email": "test@example.com", "username": "testuser"}
        session_id = session_manager.create_session("user123", user_data)
        
        success = session_manager.delete_session(session_id)
        assert success is True
        
        retrieved = session_manager.get_session(session_id)
        assert retrieved is None
    
    def test_is_session_valid(self, session_manager):
        """Test checking session validity."""
        user_data = {"email": "test@example.com"}
        session_id = session_manager.create_session("user123", user_data)
        
        assert session_manager.is_session_valid(session_id) is True
        
        session_manager.delete_session(session_id)
        assert session_manager.is_session_valid(session_id) is False
    
    def test_get_session_ttl(self, session_manager):
        """Test getting session TTL."""
        user_data = {"email": "test@example.com"}
        session_id = session_manager.create_session("user123", user_data)
        
        ttl = session_manager.get_session_ttl(session_id)
        assert ttl is not None
        assert ttl > 0
        assert ttl <= 3600  # Should be at or close to SESSION_EXPIRY_TIME


class TestCacheManager:
    """Test CacheManager functionality."""
    
    @pytest.fixture
    def cache_manager(self):
        """Create a cache manager instance."""
        return CacheManager()
    
    def test_set_and_get(self, cache_manager):
        """Test setting and getting cache values."""
        cache_manager.set("test_key", "test_value", ttl=600)
        result = cache_manager.get("test_key")
        
        assert result == "test_value"
    
    def test_set_and_get_dict(self, cache_manager):
        """Test caching dictionary objects."""
        test_data = {"name": "John", "age": 30}
        cache_manager.set("user:123", test_data, ttl=600)
        result = cache_manager.get("user:123")
        
        assert result == test_data
        assert result["name"] == "John"
    
    def test_delete(self, cache_manager):
        """Test deleting cache entries."""
        cache_manager.set("test_key", "value", ttl=600)
        
        success = cache_manager.delete("test_key")
        assert success is True
        
        result = cache_manager.get("test_key")
        assert result is None
    
    def test_exists(self, cache_manager):
        """Test checking if key exists."""
        cache_manager.set("test_key", "value", ttl=600)
        
        assert cache_manager.exists("test_key") is True
        assert cache_manager.exists("nonexistent") is False
    
    def test_increment(self, cache_manager):
        """Test counter increment."""
        counter_key = "counter:test"
        
        value1 = cache_manager.increment(counter_key, amount=1, ttl=600)
        assert value1 == 1
        
        value2 = cache_manager.increment(counter_key, amount=5)
        assert value2 == 6
    
    def test_decrement(self, cache_manager):
        """Test counter decrement."""
        counter_key = "counter:test"
        cache_manager.set(counter_key, 10)
        
        result = cache_manager.decrement(counter_key, amount=3)
        assert result == 7
    
    def test_clear_pattern(self, cache_manager):
        """Test clearing cache by pattern."""
        cache_manager.set("product:1", "data1")
        cache_manager.set("product:2", "data2")
        cache_manager.set("user:1", "data3")
        
        deleted = cache_manager.clear_pattern("product:*")
        
        assert deleted == 2
        assert cache_manager.get("product:1") is None
        assert cache_manager.get("user:1") is not None
    
    def test_get_ttl(self, cache_manager):
        """Test getting remaining TTL."""
        cache_manager.set("test_key", "value", ttl=600)
        
        ttl = cache_manager.get_ttl("test_key")
        assert ttl is not None
        assert ttl > 0
        assert ttl <= 600


class TestSessionEndpoints:
    """Integration tests for session endpoints."""
    
    def test_health_check(self):
        """Test that Redis is accessible."""
        try:
            sm = SessionManager()
            cm = CacheManager()
            assert sm is not None
            assert cm is not None
        except Exception as e:
            pytest.skip(f"Redis not available: {e}")


# Test fixtures
@pytest.fixture(autouse=True)
def cleanup_cache():
    """Clean up cache before and after each test."""
    cache = get_cache_manager()
    cache.clear_pattern("test:*")
    cache.clear_pattern("product:*")
    cache.clear_pattern("user:*")
    cache.clear_pattern("counter:*")
    yield
    cache.clear_pattern("test:*")
    cache.clear_pattern("product:*")
    cache.clear_pattern("user:*")
    cache.clear_pattern("counter:*")


@pytest.fixture(autouse=True)
def cleanup_sessions():
    """Clean up sessions before and after each test."""
    session_manager = get_session_manager()
    # Note: In real scenarios, you'd clear specific test sessions
    yield


# Performance tests
class TestPerformance:
    """Performance tests for cache operations."""
    
    def test_bulk_set_performance(self):
        """Test setting multiple cache entries."""
        cache = get_cache_manager()
        
        start = time.time()
        for i in range(100):
            cache.set(f"perf_test:{i}", f"value_{i}")
        elapsed = time.time() - start
        
        # Should complete in reasonable time (< 5 seconds for 100 ops)
        assert elapsed < 5.0
        print(f"✓ Set 100 items in {elapsed:.3f}s")
    
    def test_bulk_get_performance(self):
        """Test getting multiple cache entries."""
        cache = get_cache_manager()
        
        # Setup
        for i in range(100):
            cache.set(f"perf_test:{i}", f"value_{i}")
        
        start = time.time()
        for i in range(100):
            cache.get(f"perf_test:{i}")
        elapsed = time.time() - start
        
        # Should complete quickly
        assert elapsed < 5.0
        print(f"✓ Get 100 items in {elapsed:.3f}s")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
