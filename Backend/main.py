from fastapi import FastAPI

from database import engine, Base
from routes.Signup import router as signup_router
from fastapi.middleware.cors import CORSMiddleware
from routes.products import router as products

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Include signup router
app.include_router(
    signup_router,
    prefix="/signup",
    tags=["Signup"]
)
app.include_router(
    products,
    prefix="/products",
    tags=["Products"]
)






# from fastapi import FastAPI
# from routes.practices import router as practices
# from database import engine,Base


# app=FastAPI()

# Base.metadata.create_all(bind=engine)

# app.include_router(practices,prefix="/router")

# @app.get("/")
# def home():
#     return "this home page"



