# E-Commerce Backend Documentation

This backend is a FastAPI application for an e-commerce project. It handles user signup and login, products, cart, orders, payment flow, Redis cache, Redis-backed sessions, cookies, templates, WebSocket echo testing, and Gemini response streaming.

The main focus of this document is to explain the backend from scratch to end, especially cache, sessions, and cookies.

## Tech Stack

- Python
- FastAPI
- Uvicorn
- SQLAlchemy
- MySQL
- PyMySQL
- Pydantic
- PyJWT
- pwdlib password hashing
- Redis
- Docker Compose for Redis
- Razorpay payment integration
- Google GenAI streaming endpoint
- Jinja2 templates

## Backend Folder Structure

```text
Backend/
  main.py                    FastAPI app entry point
  database.py                MySQL connection and DB session dependency
  config.py                  Redis, session, cookie, and cache settings
  session_manager.py         Redis session CRUD logic
  cache_manager.py           Redis cache helper logic
  dependencies.py            Cookie session authentication dependencies
  requirements.txt           Python dependencies
  examples.py                Cache/session usage examples
  test_session_cache.py      Cache/session tests
  models/
    Signup.py                User table
    Products.py              Product table
    Cart.py                  Cart table
    Order.py                 Order table
  schemas/
    Signup.py                Signup/profile request schemas
    Login.py                 Login/token request schemas
  routes/
    auth.py                  Signup and JWT login
    session.py               Cookie-based session endpoints
    products.py              Product listing and product details
    cart.py                  Cart APIs protected by JWT
    orders.py                Order and payment APIs protected by JWT
    Profile.py               Profile update endpoints
    Payment.py               Small test route
    voice_api.py             Gemini voice API experiment
  templates/
    index.html               Home page
    routes.html              Route listing page
```

## What Was Built

This backend was built step by step around these main parts:

1. FastAPI app setup in `main.py`.
2. MySQL database connection in `database.py`.
3. SQLAlchemy models for users, products, cart items, and orders.
4. Signup API with password hashing.
5. Login API that creates a JWT token.
6. Product APIs to list products and fetch one product.
7. Cart APIs to add, update, remove, clear, and read cart items.
8. Order APIs to create payment, verify payment, place orders, cancel orders, and return orders.
9. Redis cache manager for generic cached data.
10. Redis session manager for server-side user sessions.
11. Cookie-based session APIs under `/session`.
12. Template pages for `/` and `/routes`.
13. WebSocket echo endpoint at `/ws`.
14. Gemini streaming endpoint at `/api/generate`.

## How The Application Starts

The app starts from `main.py`.

Important things happening there:

```python
app = FastAPI()
```

This creates the FastAPI application.

```python
app.add_middleware(CORSMiddleware, ...)
```

This allows the frontend to call the backend APIs.

```python
Base.metadata.create_all(bind=engine)
```

This creates database tables from SQLAlchemy models if they do not already exist.

```python
app.include_router(auth)
app.include_router(session)
app.include_router(products, prefix="/products")
app.include_router(cart)
app.include_router(orders)
app.include_router(Profile_router)
```

This connects all route files to the main FastAPI app.

## Setup From Scratch

### 1. Create And Activate Virtual Environment

From the project root:

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Install Backend Dependencies

```bash
pip install -r Backend/requirements.txt
```

### 3. Start Redis

Redis is configured in the root `docker-compose.yml`.

From the project root:

```bash
docker-compose up -d redis
```

This starts a Redis container named `ecom-redis` on port `6379`.

### 4. Configure Environment Variables

Create or update `.env` in the project root.

Example:

```env
JWT_SECRET_KEY=your_jwt_secret_key
ALGORITHM=HS256

REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

SESSION_EXPIRY_TIME=3600
SESSION_COOKIE_NAME=session_id
SESSION_COOKIE_SECURE=False
SESSION_COOKIE_HTTPONLY=True
SESSION_COOKIE_SAMESITE=lax

CACHE_TTL=600
ENVIRONMENT=development

RAZORPAY_KEY_ID=your_razorpay_key_id
RAZORPAY_KEY_SECRET=your_razorpay_key_secret
GEMINI_API_KEY=your_gemini_api_key
```

For local development, `SESSION_COOKIE_SECURE=False` is useful because secure cookies are only sent over HTTPS. For production, use `SESSION_COOKIE_SECURE=True`.

### 5. Configure MySQL

The database URL is currently inside `database.py`:

```python
SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:password@localhost/e_com"
```

Make sure:

- MySQL is running.
- Database `e_com` exists.
- Username and password are correct.
- The backend can connect to MySQL.

### 6. Run Backend Server

From the `Backend` folder:

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

Swagger API docs:

```text
http://127.0.0.1:8000/docs
```

Route list page:

```text
http://127.0.0.1:8000/routes
```

## Database Layer

`database.py` creates the SQLAlchemy engine and database session.

```python
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()
```

The `get_db()` function is used as a FastAPI dependency:

```python
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Every API that needs the database uses:

```python
db: Session = Depends(get_db)
```

This creates one DB session for the request and closes it after the request is complete.

## Database Models

### User

File: `models/Signup.py`

Table: `user_details`

Fields:

- `id`
- `full_name`
- `email`
- `password`

Used for signup, login, cart ownership, and order ownership.

### Product

File: `models/Products.py`

Table: `products`

Fields:

- `id`
- `mongo_id`
- `name`
- `category`
- `price`
- `rating`
- `reviews`
- `image`
- `description`
- `stock`
- `version`
- `created_at`
- `updated_at`

Used by product listing, product detail, cart, and orders.

### CartItem

File: `models/Cart.py`

Table: `cart_items`

Fields:

- `id`
- `user_id`
- `product_id`
- `quantity`
- `created_at`
- `updated_at`

There is a unique rule on `user_id` and `product_id`, so the same product is not duplicated for the same user. If the user adds the same product again, quantity is increased.

### Order

File: `models/Order.py`

Table: `orders`

Fields:

- `id`
- `user_id`
- `items`
- `shipping_address`
- `total_amount`
- `status`
- `is_paid`
- `razorpay_order_id`
- `razorpay_payment_id`
- `razorpay_signature`
- `expected_delivery`
- `created_at`
- `updated_at`

Order items and shipping address are stored as JSON snapshots so the order keeps the product data from checkout time.

## Authentication Flow

This project currently has two authentication systems:

1. JWT login from `routes/auth.py`.
2. Cookie session login from `routes/session.py`.

### JWT Login

The normal e-commerce cart and order APIs use JWT authentication.

Flow:

1. User signs up with `/signup`.
2. User logs in with `/Login`.
3. Backend verifies password.
4. Backend creates JWT token.
5. Frontend stores token.
6. Frontend sends token in API requests:

```http
Authorization: Bearer <token>
```

Cart and order APIs read the token, decode the email from the JWT payload, load the user from MySQL, and then allow access.

### Cookie Session Login

The `/session/*` APIs demonstrate server-side sessions using Redis and browser cookies.

Flow:

1. User calls `/session/login`.
2. Backend creates a random session ID.
3. Backend stores session data in Redis.
4. Backend sends the session ID to the browser as a cookie.
5. Browser automatically sends the cookie on future requests.
6. Backend reads the cookie and loads session data from Redis.
7. If the Redis session exists, the user is authenticated.
8. If the Redis session is expired or deleted, the user is not authenticated.

## Main API Endpoints

### Auth

```text
POST /signup
POST /Login
```

`/signup` creates a new user with a hashed password.

`/Login` validates email and password and returns a JWT token.

### Products

```text
GET /products/
GET /products/{product_id}
```

`GET /products/` returns all products. It also supports filtering by category:

```text
GET /products/?category=electronics
```

`GET /products/{product_id}` supports both numeric DB ID and `mongo_id`.

### Cart

All cart APIs require JWT token.

```text
GET    /cart/
POST   /cart/
PUT    /cart/
DELETE /cart/clear
DELETE /cart/{product_id}
```

Cart flow:

1. Frontend sends product ID and quantity.
2. Backend validates the JWT.
3. Backend finds the logged-in user.
4. Backend finds the product.
5. Backend creates or updates cart item.
6. Backend returns the updated cart.

### Orders And Payment

All order APIs require JWT token.

```text
GET  /orders/
POST /orders/create-payment
POST /orders/verify-payment
POST /orders/dummy-payment
PUT  /orders/{order_id}/cancel
PUT  /orders/{order_id}/return
```

Order flow:

1. User adds products to cart.
2. User starts checkout.
3. Backend calculates total from cart.
4. Backend creates Razorpay order if Razorpay keys exist.
5. Frontend completes payment.
6. Backend verifies Razorpay signature.
7. Backend creates order from cart snapshot.
8. Backend clears cart.
9. User can see, cancel, or return orders.

If Razorpay keys are missing, the backend returns a dummy order ID for local testing.

### Sessions

```text
POST /session/login
POST /session/logout
GET  /session/me
POST /session/refresh
POST /session/logout-all
```

These APIs use Redis sessions and cookies instead of JWT.

### Gemini Streaming

```text
POST /api/generate
```

This accepts a prompt and streams text from Gemini using `StreamingResponse`.

### WebSocket

```text
ws://127.0.0.1:8000/ws
```

This is a simple echo WebSocket. It receives text and sends the same text back.

## Cache, Session, And Cookie Explanation

This is the most important backend concept in this project.

### What Is Cache?

Cache is temporary storage used to make repeated operations faster.

Example:

- Product list is requested many times.
- Instead of querying MySQL every time, the backend can store the product list in Redis.
- Next request reads from Redis.
- After a fixed time, the cache expires and fresh data is loaded again.

Cache is not the main database. It is a speed layer.

In this project, cache is handled by:

```text
cache_manager.py
```

The `CacheManager` connects to Redis and provides helper methods:

```python
cache.get(key)
cache.set(key, value, ttl=600)
cache.delete(key)
cache.exists(key)
cache.clear_pattern("product:*")
cache.get_ttl(key)
cache.increment(key)
cache.decrement(key)
```

### Why Redis Is Used For Cache

Redis is fast because it stores data in memory.

Good uses for Redis cache:

- Product list cache
- Product detail cache
- Frequently used category data
- Temporary counters
- Rate limit counters
- Expensive API response cache

Example:

```python
from cache_manager import get_cache_manager

cache = get_cache_manager()

products = cache.get("products:all")
if products:
    return products

products = load_products_from_database()
cache.set("products:all", products, ttl=600)
return products
```

Here:

- First request reads from MySQL.
- Data is saved in Redis for 600 seconds.
- Next requests read from Redis.
- After 600 seconds, Redis deletes the cached value.

### What Is TTL?

TTL means "time to live".

It decides how long Redis keeps a key.

Example:

```python
cache.set("products:all", products, ttl=600)
```

This means Redis stores `products:all` for 600 seconds. After that, the key expires automatically.

The default cache TTL comes from `config.py`:

```python
CACHE_TTL = int(os.getenv("CACHE_TTL", 600))
```

### What Is Session?

A session means server-side login state.

When a user logs in, the backend creates a session record. That record says:

- Who the user is.
- When the session was created.
- When the session was last used.
- Any extra user data needed by the app.

In this project, sessions are stored in Redis, not in MySQL.

Session data example in Redis:

```json
{
  "user_id": "123",
  "email": "user@example.com",
  "username": "john",
  "created_at": "2026-06-19T10:00:00",
  "last_accessed": "2026-06-19T10:05:00"
}
```

The Redis key looks like:

```text
session:<session_id>
```

Example:

```text
session:7b7a95ec-85c6-43ce-a953-6169ac245829
```

### SessionManager

Sessions are handled by:

```text
session_manager.py
```

Important methods:

```python
create_session(user_id, user_data)
get_session(session_id)
update_session(session_id, user_data)
delete_session(session_id)
delete_all_user_sessions(user_id)
is_session_valid(session_id)
get_session_ttl(session_id)
```

### How Session Login Works

Endpoint:

```text
POST /session/login
```

Request:

```json
{
  "user_id": "123",
  "email": "user@example.com",
  "username": "john"
}
```

Backend steps:

1. Generate random UUID session ID.
2. Build session data with user ID, email, username, created time, and last accessed time.
3. Save the data in Redis using `setex`.
4. `setex` saves data with an expiry time.
5. Send the session ID to the browser as a cookie.

Code concept:

```python
session_id = session_manager.create_session(request.user_id, user_data)

response.set_cookie(
    key=SESSION_COOKIE_NAME,
    value=session_id,
    httponly=True,
    secure=False,
    samesite="lax",
    max_age=3600
)
```

### What Is Cookie?

A cookie is small data saved by the browser for a website.

In this project, the cookie stores only the session ID, not the full user data.

Example cookie:

```text
session_id=7b7a95ec-85c6-43ce-a953-6169ac245829
```

The browser automatically sends this cookie to the backend on future requests.

The backend uses the session ID from the cookie to find the real session data in Redis.

### Why Store Only Session ID In Cookie?

This is safer and cleaner.

Do not store full user data in a cookie because cookies live in the browser.

Better approach:

- Cookie stores random session ID.
- Redis stores actual user data.
- Backend controls session expiry and logout.
- If user logs out, backend deletes the Redis session.
- The old cookie becomes useless.

### Cookie Security Options

Cookie settings are configured in `config.py`.

```python
SESSION_COOKIE_NAME = "session_id"
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "lax"
```

#### HttpOnly

```text
SESSION_COOKIE_HTTPONLY=True
```

This means JavaScript cannot read the cookie.

Why it matters:

- Protects session cookie from many XSS attacks.
- Frontend code cannot accidentally expose the session ID.

#### Secure

```text
SESSION_COOKIE_SECURE=True
```

This means browser sends the cookie only over HTTPS.

Use:

- `False` for local HTTP development.
- `True` for production HTTPS.

#### SameSite

```text
SESSION_COOKIE_SAMESITE=lax
```

This controls cross-site cookie behavior.

Common values:

- `lax`: good default for many apps.
- `strict`: stronger CSRF protection, but can block some cross-site navigation flows.
- `none`: allows cross-site cookies, but requires `Secure=True`.

### Session Expiry

Session expiry comes from:

```python
SESSION_EXPIRY_TIME = 3600
```

That means one session lives for one hour.

When a session is read or refreshed, `last_accessed` is updated and TTL is reset.

So the active session can continue while the user keeps using the app.

### Logout

Endpoint:

```text
POST /session/logout
```

Backend steps:

1. Read `session_id` from cookie.
2. Delete `session:<session_id>` from Redis.
3. Delete cookie from browser response.

After this, the session is invalid.

### Logout All Devices

Endpoint:

```text
POST /session/logout-all
```

Backend steps:

1. Read current session.
2. Get `user_id`.
3. Scan all Redis keys matching `session:*`.
4. Delete every session belonging to the same user.

This is useful when a user wants to log out from all browsers or devices.

### Session vs JWT

This project uses JWT for cart and orders, and Redis sessions for `/session` routes.

Main difference:

| Topic | JWT | Redis Session |
| --- | --- | --- |
| Stored in | Browser/local storage or memory | Redis on server |
| Client has | Full token | Only session ID |
| Logout | Harder before token expiry | Easy, delete Redis key |
| Server lookup | Usually no DB/session lookup needed | Needs Redis lookup |
| Best for | Stateless APIs | Server-controlled login state |

For this e-commerce backend, either approach can work. If you want stronger logout control and cookie-based browser auth, Redis sessions are better. If you want simple token auth between frontend and backend, JWT is easier.

## Redis Commands For Debugging

Open Redis CLI:

```bash
redis-cli
```

Check Redis:

```bash
PING
```

List session keys:

```bash
KEYS session:*
```

Get one session:

```bash
GET session:<session_id>
```

Check TTL:

```bash
TTL session:<session_id>
```

Delete one session:

```bash
DEL session:<session_id>
```

Watch Redis commands live:

```bash
MONITOR
```

For production, prefer `SCAN` instead of `KEYS` because `KEYS` can block Redis when there are many keys.

## Example Requests

### Signup

```bash
curl -X POST http://127.0.0.1:8000/signup \
  -H "Content-Type: application/json" \
  -d "{\"full_name\":\"John\",\"Email_Address\":\"john@example.com\",\"Password\":\"password123\"}"
```

### JWT Login

```bash
curl -X POST http://127.0.0.1:8000/Login \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"john@example.com\",\"password\":\"password123\"}"
```

Use the returned token:

```bash
curl http://127.0.0.1:8000/cart/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Cookie Session Login

```bash
curl -i -X POST http://127.0.0.1:8000/session/login \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"1\",\"email\":\"john@example.com\",\"username\":\"John\"}"
```

The response includes a `Set-Cookie` header.

Use cookie with next request:

```bash
curl http://127.0.0.1:8000/session/me \
  --cookie "session_id=YOUR_SESSION_ID"
```

### Product List

```bash
curl http://127.0.0.1:8000/products/
```

### Product By ID

```bash
curl http://127.0.0.1:8000/products/1
```

### Add To Cart

```bash
curl -X POST http://127.0.0.1:8000/cart/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d "{\"productId\":\"1\",\"quantity\":2}"
```

### Dummy Payment

```bash
curl -X POST http://127.0.0.1:8000/orders/dummy-payment \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d "{\"shippingAddress\":{\"street\":\"Main Road\",\"city\":\"Chennai\",\"state\":\"TN\",\"pincode\":\"600001\"}}"
```

## Testing

Session and cache tests are available in:

```text
Backend/test_session_cache.py
```

Run from the `Backend` folder:

```bash
pytest test_session_cache.py -v
```

Redis must be running before cache/session tests.

## Current Notes And Improvements

- `database.py` currently keeps the MySQL URL directly in code. A better production setup is to move it into `.env`.
- Cart and order routes use JWT auth, while `/session/*` routes use Redis cookie sessions. For a final production backend, choose one main authentication style or intentionally support both.
- Local cookie testing usually needs `SESSION_COOKIE_SECURE=False`.
- Production cookie testing needs HTTPS and `SESSION_COOKIE_SECURE=True`.
- Redis cache is implemented as a reusable manager. Product routes can be extended to use it for product list/detail caching.
- Session cookie extraction currently works with the default cookie name `session_id`.

## End-To-End Backend Flow

Complete user flow:

1. User signs up using `/signup`.
2. Password is hashed and saved in MySQL.
3. User logs in using `/Login`.
4. Backend returns JWT token.
5. Frontend sends JWT token for cart and order APIs.
6. User views products from `/products/`.
7. User adds products to `/cart/`.
8. Cart data is stored in MySQL.
9. User checks out.
10. Backend creates Razorpay payment or dummy payment.
11. Backend verifies payment.
12. Backend creates order snapshot in MySQL.
13. Backend clears cart.
14. User views orders from `/orders/`.
15. User can cancel or return an order.

Session and cookie flow:

1. User logs in using `/session/login`.
2. Backend creates session ID.
3. Session data is stored in Redis.
4. Session ID is sent as HTTP-only cookie.
5. Browser sends cookie automatically.
6. Backend validates cookie by checking Redis.
7. User can refresh, view, logout, or logout from all sessions.

Cache flow:

1. Backend checks Redis for cached data.
2. If found, return cached data quickly.
3. If not found, load from MySQL or external API.
4. Save result in Redis with TTL.
5. Future requests use Redis until TTL expires.

## Summary

This backend includes the core parts needed for an e-commerce API:

- FastAPI application setup
- MySQL database connection
- SQLAlchemy models
- Signup and JWT login
- Product APIs
- Cart APIs
- Order and payment APIs
- Redis cache manager
- Redis session manager
- Cookie-based session APIs
- WebSocket and streaming examples

The most important backend concepts added are Redis cache, server-side sessions, and browser cookies. Cache is for speed, sessions are for server-side login state, and cookies are how the browser carries the session ID back to the backend.
