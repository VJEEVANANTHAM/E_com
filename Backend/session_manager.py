import redis
import json
import uuid
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from config import (
    REDIS_HOST, REDIS_PORT, REDIS_DB, REDIS_PASSWORD,
    SESSION_EXPIRY_TIME, SESSION_COOKIE_NAME
)


class SessionManager:
    """Redis-based session manager for handling user sessions and cookies."""
    
    def __init__(self):
        """Initialize Redis connection pool."""
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
            # Test connection
            self.redis_client.ping()
            print("✓ Redis connection established successfully")
        except redis.ConnectionError as e:
            print(f"✗ Failed to connect to Redis: {e}")
            raise
    
    def create_session(self, user_id: str, user_data: Dict[str, Any]) -> str:
        """
        Create a new session for a user.
        
        Args:
            user_id: Unique user identifier
            user_data: Dictionary containing user information to store
            
        Returns:
            Session ID (cookie value)
        """
        session_id = str(uuid.uuid4())
        
        session_data = {
            "user_id": user_id,
            "created_at": datetime.utcnow().isoformat(),
            "last_accessed": datetime.utcnow().isoformat(),
            **user_data
        }
        
        session_key = f"session:{session_id}"
        self.redis_client.setex(
            session_key,
            SESSION_EXPIRY_TIME,
            json.dumps(session_data)
        )
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve session data by session ID.
        
        Args:
            session_id: Session identifier from cookie
            
        Returns:
            Session data dictionary or None if not found/expired
        """
        session_key = f"session:{session_id}"
        session_data = self.redis_client.get(session_key)
        
        if session_data:
            self.update_last_accessed(session_id)
            return json.loads(session_data)
        return None
    
    def update_session(self, session_id: str, user_data: Dict[str, Any]) -> bool:
        """
        Update session data.
        
        Args:
            session_id: Session identifier
            user_data: Updated user data to merge
            
        Returns:
            True if successful, False if session not found
        """
        session_key = f"session:{session_id}"
        existing_data = self.redis_client.get(session_key)
        
        if not existing_data:
            return False
        
        current_data = json.loads(existing_data)
        current_data.update(user_data)
        current_data["last_accessed"] = datetime.utcnow().isoformat()
        
        self.redis_client.setex(
            session_key,
            SESSION_EXPIRY_TIME,
            json.dumps(current_data)
        )
        return True
    
    def update_last_accessed(self, session_id: str) -> None:
        """Update the last accessed timestamp for a session."""
        session_key = f"session:{session_id}"
        session_data = self.redis_client.get(session_key)
        
        if session_data:
            data = json.loads(session_data)
            data["last_accessed"] = datetime.utcnow().isoformat()
            self.redis_client.setex(
                session_key,
                SESSION_EXPIRY_TIME,
                json.dumps(data)
            )
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete/invalidate a session.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if session was deleted, False if not found
        """
        session_key = f"session:{session_id}"
        result = self.redis_client.delete(session_key)
        return result > 0
    
    def delete_all_user_sessions(self, user_id: str) -> int:
        """
        Delete all sessions for a specific user (logout all devices).
        
        Args:
            user_id: User identifier
            
        Returns:
            Number of sessions deleted
        """
        pattern = "session:*"
        deleted_count = 0
        
        for key in self.redis_client.scan_iter(pattern):
            session_data = self.redis_client.get(key)
            if session_data:
                data = json.loads(session_data)
                if data.get("user_id") == user_id:
                    self.redis_client.delete(key)
                    deleted_count += 1
        
        return deleted_count
    
    def is_session_valid(self, session_id: str) -> bool:
        """
        Check if a session is still valid.
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if valid, False otherwise
        """
        session_key = f"session:{session_id}"
        return self.redis_client.exists(session_key) > 0
    
    def get_session_ttl(self, session_id: str) -> Optional[int]:
        """
        Get remaining TTL for a session in seconds.
        
        Args:
            session_id: Session identifier
            
        Returns:
            TTL in seconds or None if session not found
        """
        session_key = f"session:{session_id}"
        ttl = self.redis_client.ttl(session_key)
        return ttl if ttl >= 0 else None


# Global session manager instance
_session_manager: Optional[SessionManager] = None


def get_session_manager() -> SessionManager:
    """Get or create the global session manager instance."""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
