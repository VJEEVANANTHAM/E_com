"""
Example usage of Session and Cache managers in FastAPI.

This file demonstrates common patterns for implementing
session management and caching in your FastAPI application.
"""

from fastapi import FastAPI, Depends, HTTPException, Response, Cookie, status
from fastapi.responses import JSONResponse
from typing import Optional
from pydantic import BaseModel

# Import managers and dependencies
from session_manager import get_session_manager
from cache_manager import get_cache_manager
from dependencies import get_current_user, get_optional_user

app = FastAPI(title="Session & Cache Examples")


# ==================== MODELS ====================

class UserLoginRequest(BaseModel):
    user_id: str
    email: str
    username: str
    password: str  # In real app, validate against DB


class ProductData(BaseModel):
    id: str
    name: str
    price: float
    description: str


# ==================== SESSION EXAMPLES ====================

@app.post("/examples/session/login")
async def example_login(request: UserLoginRequest, response: Response):
    """
    Example: Create a session when user logs in.
    """
    session_manager = get_session_manager()
    
    # In real app, validate password here
    user_data = {
        "email": request.email,
        "username": request.username,
        "role": "user",
        "last_login": "2026-06-04"
    }
    
    session_id = session_manager.create_session(request.user_id, user_data)
    
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        secure=False,  # Change to True in production
        samesite="lax",
        max_age=3600
    )
    
    return {"message": "Login successful", "session_id": session_id}


@app.get("/examples/session/profile")
async def example_get_profile(current_user: dict = Depends(get_current_user)):
    """
    Example: Access protected route using session dependency.
    """
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "username": current_user["username"],
        "role": current_user.get("role", "user"),
        "created_at": current_user["created_at"],
        "last_accessed": current_user["last_accessed"]
    }


@app.post("/examples/session/update-profile")
async def example_update_profile(
    username: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Example: Update session data.
    """
    session_manager = get_session_manager()
    session_id = None
    
    # In real app, you'd extract session_id from cookie
    # For this example, we'll use the current_user data
    user_id = current_user["user_id"]
    
    # Update user data
    updated_data = {"username": username}
    
    return {
        "message": "Profile updated successfully",
        "user": {**current_user, **updated_data}
    }


@app.post("/examples/session/logout")
async def example_logout(response: Response, session_id: Optional[str] = Cookie(None)):
    """
    Example: Logout and invalidate session.
    """
    session_manager = get_session_manager()
    
    if session_id:
        session_manager.delete_session(session_id)
    
    response.delete_cookie(key="session_id")
    return {"message": "Logged out successfully"}


# ==================== CACHE EXAMPLES ====================

@app.post("/examples/cache/product")
async def example_cache_product(product: ProductData):
    """
    Example: Store product data in cache.
    """
    cache = get_cache_manager()
    
    cache_key = f"product:{product.id}"
    cache.set(cache_key, product.dict(), ttl=3600)
    
    return {"message": f"Product {product.id} cached", "ttl": 3600}


@app.get("/examples/cache/product/{product_id}")
async def example_get_cached_product(product_id: str):
    """
    Example: Retrieve product from cache or database.
    """
    cache = get_cache_manager()
    
    cache_key = f"product:{product_id}"
    cached_product = cache.get(cache_key)
    
    if cached_product:
        return {"source": "cache", "data": cached_product}
    
    # In real app, fetch from database here
    mock_product = {
        "id": product_id,
        "name": "Example Product",
        "price": 99.99
    }
    
    # Cache for next time
    cache.set(cache_key, mock_product, ttl=3600)
    
    return {"source": "database", "data": mock_product}


@app.post("/examples/cache/clear-product/{product_id}")
async def example_clear_product_cache(product_id: str):
    """
    Example: Clear specific product from cache.
    """
    cache = get_cache_manager()
    
    cache_key = f"product:{product_id}"
    was_deleted = cache.delete(cache_key)
    
    return {
        "message": f"Product cache cleared",
        "was_cached": was_deleted
    }


@app.post("/examples/cache/view-count/{product_id}")
async def example_increment_view_count(product_id: str):
    """
    Example: Use cache for counters (view count).
    """
    cache = get_cache_manager()
    
    counter_key = f"product:{product_id}:views"
    new_count = cache.increment(counter_key, amount=1, ttl=86400)
    
    return {
        "product_id": product_id,
        "total_views": new_count
    }


@app.get("/examples/cache/view-count/{product_id}")
async def example_get_view_count(product_id: str):
    """
    Example: Get cached counter value.
    """
    cache = get_cache_manager()
    
    counter_key = f"product:{product_id}:views"
    count = cache.get(counter_key) or 0
    
    return {
        "product_id": product_id,
        "total_views": count
    }


@app.post("/examples/cache/clear-pattern")
async def example_clear_cache_pattern(pattern: str):
    """
    Example: Clear multiple cache keys by pattern.
    
    Usage:
    - /examples/cache/clear-pattern?pattern=product:*
    - /examples/cache/clear-pattern?pattern=product:123:*
    """
    cache = get_cache_manager()
    
    deleted_count = cache.clear_pattern(pattern)
    
    return {
        "pattern": pattern,
        "deleted_keys": deleted_count
    }


# ==================== COMBINED EXAMPLES ====================

@app.post("/examples/user-activity")
async def example_track_user_activity(current_user: dict = Depends(get_current_user)):
    """
    Example: Track user activity using both sessions and cache.
    
    - Session: Stores logged-in user data
    - Cache: Stores activity metrics
    """
    cache = get_cache_manager()
    user_id = current_user["user_id"]
    
    # Increment activity counter
    activity_key = f"user:{user_id}:activity_count"
    activity_count = cache.increment(activity_key, amount=1, ttl=86400)
    
    # Store last activity timestamp
    last_activity_key = f"user:{user_id}:last_activity"
    cache.set(last_activity_key, "2026-06-04T12:30:00", ttl=86400)
    
    return {
        "user_id": user_id,
        "activity_count": activity_count,
        "message": "Activity tracked"
    }


@app.get("/examples/dashboard")
async def example_dashboard(current_user: dict = Depends(get_current_user)):
    """
    Example: Dashboard using session + cache data.
    """
    cache = get_cache_manager()
    user_id = current_user["user_id"]
    
    # Get cached metrics
    activity_count = cache.get(f"user:{user_id}:activity_count") or 0
    last_activity = cache.get(f"user:{user_id}:last_activity")
    
    return {
        "user_info": {
            "user_id": current_user["user_id"],
            "email": current_user["email"],
            "username": current_user["username"]
        },
        "metrics": {
            "activity_count": activity_count,
            "last_activity": last_activity,
            "session_created": current_user["created_at"]
        }
    }


@app.get("/examples/optional-user")
async def example_optional_user(current_user: dict = Depends(get_optional_user)):
    """
    Example: Route that works for both authenticated and anonymous users.
    """
    if current_user:
        return {
            "authenticated": True,
            "user_id": current_user["user_id"],
            "message": f"Welcome {current_user['username']}"
        }
    else:
        return {
            "authenticated": False,
            "message": "Welcome guest, please log in to see personalized content"
        }


# ==================== HEALTH CHECK ====================

@app.get("/examples/health")
async def example_health_check():
    """
    Example: Health check for Redis connections.
    """
    try:
        session_manager = get_session_manager()
        cache = get_cache_manager()
        
        # Test both managers
        cache.set("health_check", "ok", ttl=10)
        value = cache.get("health_check")
        
        return {
            "status": "healthy",
            "redis": "connected",
            "cache_test": value
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "redis": "disconnected",
            "error": str(e)
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
