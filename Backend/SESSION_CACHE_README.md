# Session Cookies & Caching System

A production-ready Redis-based session management and caching system for FastAPI with secure HTTP-only cookies.

## Features

✅ **Secure Session Management**
- UUID-based session IDs
- HTTP-only cookies (prevents XSS attacks)
- Configurable expiry times
- Automatic session TTL extension on access

✅ **Redis-Backed Storage**
- Fast in-memory session storage
- Automatic cleanup of expired sessions
- Support for clustered deployments

✅ **Cache Management**
- Generic key-value caching with TTL
- Counter operations (increment/decrement)
- Pattern-based key deletion
- JSON serialization support

✅ **Multi-Device Support**
- Track sessions across multiple devices
- "Logout all devices" functionality
- Per-session activity tracking

## Installation

### 1. Install Dependencies

```bash
pip install redis==5.0.1
```

Add to `requirements.txt`:
```
redis==5.0.1
```

### 2. Setup Redis

**Using Docker (Recommended):**
```bash
docker run -d -p 6379:6379 redis:7-alpine
```

**Using Homebrew (macOS):**
```bash
brew install redis
redis-server
```

**Using apt (Linux):**
```bash
sudo apt-get install redis-server
redis-server
```

### 3. Environment Configuration

Copy `.env.example` to `.env` and configure:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=         # Leave empty if no password

SESSION_EXPIRY_TIME=3600    # Session timeout in seconds
SESSION_COOKIE_SECURE=False # Set to True for HTTPS
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=lax

CACHE_TTL=600    # Default cache TTL in seconds
ENVIRONMENT=development
```

## Usage

### Session Management

#### Login (Create Session)

```python
from fastapi import APIRouter
from session_manager import get_session_manager
from config import SESSION_COOKIE_NAME, SESSION_COOKIE_SECURE, SESSION_COOKIE_HTTPONLY, SESSION_COOKIE_SAMESITE

@app.post("/login")
async def login(request: LoginRequest, response: Response):
    session_manager = get_session_manager()
    
    user_data = {
        "email": request.email,
        "username": request.username,
        "role": "admin"
    }
    
    session_id = session_manager.create_session(request.user_id, user_data)
    
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=SESSION_COOKIE_HTTPONLY,
        secure=SESSION_COOKIE_SECURE,
        samesite=SESSION_COOKIE_SAMESITE,
        max_age=3600
    )
    
    return {"message": "Login successful"}
```

#### Get Session Data

```python
from dependencies import get_current_user

@app.get("/profile")
async def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "user_id": current_user["user_id"],
        "email": current_user["email"],
        "username": current_user["username"]
    }
```

#### Logout

```python
from session_manager import get_session_manager

@app.post("/logout")
async def logout(session_id: str = Cookie(None), response: Response = Response()):
    if session_id:
        session_manager = get_session_manager()
        session_manager.delete_session(session_id)
    
    response.delete_cookie(key=SESSION_COOKIE_NAME)
    return {"message": "Logged out"}
```

#### Logout All Devices

```python
@app.post("/logout-all")
async def logout_all(current_user: dict = Depends(get_current_user)):
    session_manager = get_session_manager()
    deleted_count = session_manager.delete_all_user_sessions(current_user["user_id"])
    
    return {"message": f"Logged out from {deleted_count} device(s)"}
```

### Cache Management

#### Basic Caching

```python
from cache_manager import get_cache_manager

cache = get_cache_manager()

# Store a value
cache.set("user:123:profile", {"name": "John", "age": 30}, ttl=600)

# Retrieve a value
user_profile = cache.get("user:123:profile")

# Check if key exists
if cache.exists("user:123:profile"):
    print("Cache hit!")

# Delete a value
cache.delete("user:123:profile")
```

#### Counter Operations

```python
cache = get_cache_manager()

# Increment view count
new_count = cache.increment("product:456:views", amount=1, ttl=86400)

# Decrement stock
new_stock = cache.decrement("product:456:stock", amount=5)
```

#### Pattern-Based Operations

```python
# Clear all products from cache
deleted = cache.clear_pattern("product:*")
print(f"Cleared {deleted} cache entries")

# Clear all user sessions
deleted = cache.clear_pattern("session:*")
```

## API Endpoints

### Session Routes (Included in main.py)

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/session/login` | Create session and set cookie |
| POST | `/session/logout` | Delete session and clear cookie |
| GET | `/session/me` | Get current session info |
| POST | `/session/refresh` | Extend session TTL |
| POST | `/session/logout-all` | Logout from all devices |

## Dependencies (Protecting Routes)

### Required Authentication

```python
from dependencies import get_current_user
from fastapi import Depends

@app.get("/protected")
async def protected_route(current_user: dict = Depends(get_current_user)):
    return {"user_id": current_user["user_id"]}
```

### Optional Authentication

```python
from dependencies import get_optional_user
from fastapi import Depends

@app.get("/optional")
async def optional_route(current_user: dict = Depends(get_optional_user)):
    if current_user:
        return {"message": f"Welcome {current_user['username']}"}
    else:
        return {"message": "Welcome guest"}
```

## Cookie Security

### Development (HTTP)
```env
SESSION_COOKIE_SECURE=False      # Allow HTTP
SESSION_COOKIE_HTTPONLY=True     # Prevent JavaScript access
SESSION_COOKIE_SAMESITE=lax      # CSRF protection
```

### Production (HTTPS)
```env
SESSION_COOKIE_SECURE=True       # HTTPS only
SESSION_COOKIE_HTTPONLY=True     # Prevent JavaScript access
SESSION_COOKIE_SAMESITE=strict   # Strict CSRF protection
```

## Redis Commands for Debugging

```bash
# Connect to Redis
redis-cli

# List all sessions
KEYS session:*

# Get session data
GET session:abc123uuid

# Check session TTL
TTL session:abc123uuid

# Clear all sessions
FLUSHDB

# Monitor Redis commands in real-time
MONITOR
```

## Error Handling

### Session Not Found
```
Status: 401 Unauthorized
Detail: "Session expired or invalid"
```

### Not Authenticated
```
Status: 401 Unauthorized
Detail: "Not authenticated"
```

### Redis Connection Error
```
✗ Failed to connect to Redis: Connection refused
```

## Performance Considerations

- **Session TTL**: Default 1 hour. Adjust based on security/UX requirements
- **Cache TTL**: Default 10 minutes. Set per-use case
- **Redis Memory**: Monitor with `INFO memory` command
- **Connection Pool**: Reuses connections, no need to manage manually

## Testing

```python
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login():
    response = client.post("/session/login", json={
        "user_id": "123",
        "email": "test@example.com",
        "username": "testuser"
    })
    assert response.status_code == 200
    assert "session_id" in response.cookies

def test_protected_route():
    # First login
    login_response = client.post("/session/login", json={
        "user_id": "123",
        "email": "test@example.com",
        "username": "testuser"
    })
    
    # Access protected route with session cookie
    response = client.get("/session/me")
    assert response.status_code == 200
```

## Troubleshooting

### Redis Connection Issues
1. Ensure Redis is running: `redis-cli ping` should return `PONG`
2. Check host/port in `.env` file
3. Verify firewall rules allow Redis port (default 6379)

### Sessions Not Persisting
1. Check Redis is running
2. Verify session cookie is being set (check browser DevTools)
3. Check `SESSION_COOKIE_HTTPONLY` setting

### Performance Issues
1. Monitor Redis memory: `redis-cli INFO memory`
2. Check network latency to Redis
3. Consider using Redis cluster for high traffic

## License

MIT
