# Quick Start Guide - Session & Cache System

## 🚀 5-Minute Setup

### 1. Install Redis

**Docker (Recommended):**
```bash
docker run -d -p 6379:6379 --name redis redis:7-alpine
```

**Or local installation:**
```bash
# macOS
brew install redis

# Ubuntu/Debian
sudo apt-get install redis-server

# Start the service
redis-server
```

### 2. Update Requirements

Add to `requirements.txt`:
```
redis==5.0.1
```

Install:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 4. Update main.py

The session router is already included. Start your FastAPI app:
```bash
uvicorn main:app --reload
```

### 5. Test It Out

```bash
# Login
curl -X POST "http://localhost:8000/session/login" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"123","email":"test@test.com","username":"testuser"}'

# Get current session
curl -X GET "http://localhost:8000/session/me" \
  -H "Cookie: session_id=YOUR_SESSION_ID"

# Logout
curl -X POST "http://localhost:8000/session/logout"
```

## 📚 Available Endpoints

```
POST   /session/login           - Create session & set cookie
POST   /session/logout          - Delete session & clear cookie  
GET    /session/me              - Get current session
POST   /session/refresh         - Extend session TTL
POST   /session/logout-all      - Logout from all devices
```

## 💻 Basic Usage in Code

### Protect a Route
```python
from dependencies import get_current_user
from fastapi import Depends

@app.get("/api/protected")
async def protected(current_user: dict = Depends(get_current_user)):
    return {"user_id": current_user["user_id"]}
```

### Cache Data
```python
from cache_manager import get_cache_manager

cache = get_cache_manager()
cache.set("key", {"data": "value"}, ttl=600)
data = cache.get("key")
```

## 🔍 Check Redis

```bash
# Connect to Redis
redis-cli

# View sessions
KEYS session:*

# Clear all
FLUSHDB
```

## ⚙️ Production Settings

Update `.env`:
```env
REDIS_HOST=your-redis-host
REDIS_PASSWORD=your-password
SESSION_COOKIE_SECURE=True
SESSION_COOKIE_SAMESITE=strict
ENVIRONMENT=production
```

## 📖 Full Documentation

See `SESSION_CACHE_README.md` for complete documentation and examples.

## 🎯 What You Get

✅ Secure HTTP-only session cookies  
✅ Redis-backed session storage  
✅ Automatic session expiry  
✅ Generic caching system  
✅ Built-in route protection  
✅ Multi-device logout support  

---

**Need help?** Check `examples.py` for comprehensive usage patterns!
