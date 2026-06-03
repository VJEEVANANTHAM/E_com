from fastapi import APIRouter, Response, HTTPException, status, Cookie
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel
from session_manager import get_session_manager
from config import SESSION_COOKIE_NAME, SESSION_COOKIE_SECURE, SESSION_COOKIE_HTTPONLY, SESSION_COOKIE_SAMESITE


router = APIRouter(prefix="/session", tags=["Session"])


class LoginRequest(BaseModel):
    user_id: str
    email: str
    username: str


class SessionResponse(BaseModel):
    user_id: str
    email: str
    username: str
    created_at: str
    last_accessed: str

#
@router.post("/login", response_model=SessionResponse)
async def login(request: LoginRequest, response: Response):
    """
    Create a new session for the user.
    
    Sets a secure HTTP-only cookie containing the session ID.
    """
    session_manager = get_session_manager()
    
    user_data = {
        "email": request.email,
        "username": request.username
    }
    
    session_id = session_manager.create_session(request.user_id, user_data)
    
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=SESSION_COOKIE_HTTPONLY,
        secure=SESSION_COOKIE_SECURE,
        samesite=SESSION_COOKIE_SAMESITE,
        max_age=3600  # 1 hour
    )
    
    session_data = session_manager.get_session(session_id)
    return SessionResponse(**session_data)


@router.post("/logout")
async def logout(response: Response, session_id: Optional[str] = Cookie(None)):
    """
    Logout the user by invalidating their session.
    
    Clears the session cookie.
    """
    if session_id:
        session_manager = get_session_manager()
        session_manager.delete_session(session_id)
    
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return {"message": "Logged out successfully"}


@router.get("/me", response_model=SessionResponse)
async def get_current_session(session_id: Optional[str] = Cookie(None)):
    """
    Get current user's session information.
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    session_manager = get_session_manager()
    session_data = session_manager.get_session(session_id)
    
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid"
        )
    
    return SessionResponse(**session_data)


@router.post("/refresh")
async def refresh_session(
    session_id: Optional[str] = Cookie(None)
):
    """
    Refresh/extend the current session.
    
    Updates the session's last_accessed time and resets TTL.
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    session_manager = get_session_manager()
    
    if not session_manager.update_session(session_id, {}):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid"
        )
    
    session_data = session_manager.get_session(session_id)
    return SessionResponse(**session_data)


@router.post("/logout-all")
async def logout_all_sessions(session_id: Optional[str] = Cookie(None)):
    """
    Logout from all devices by deleting all sessions for the current user.
    """
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )
    
    session_manager = get_session_manager()
    session_data = session_manager.get_session(session_id)
    
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid"
        )
    
    user_id = session_data.get("user_id")
    deleted_count = session_manager.delete_all_user_sessions(user_id)
    
    return {
        "message": f"Logged out from {deleted_count} session(s)",
        "deleted_sessions": deleted_count
    }
