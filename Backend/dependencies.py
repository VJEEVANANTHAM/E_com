from fastapi import Cookie, HTTPException, status
from typing import Optional
from session_manager import get_session_manager
from config import SESSION_COOKIE_NAME


async def get_current_user(session_id: Optional[str] = Cookie(None)):
    """
    Dependency to extract and validate session from cookies.
    
    Args:
        session_id: Session cookie value
        
    Returns:
        User data if session is valid
        
    Raises:
        HTTPException: If session is invalid or expired
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    session_manager = get_session_manager()
    session_data = session_manager.get_session(session_id)
    
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return session_data


async def get_optional_user(session_id: Optional[str] = Cookie(None)):
    """
    Optional dependency - returns user data if valid session exists, else None.
    
    Args:
        session_id: Session cookie value
        
    Returns:
        User data if valid session, None otherwise
    """
    if not session_id:
        return None
    
    session_manager = get_session_manager()
    return session_manager.get_session(session_id)
