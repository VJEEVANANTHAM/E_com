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

# from fastapi import FastAPI, APIRouter


# @
# # Create FastAPI app
# app = FastAPI()

# # Create router
# router = APIRouter(
#     prefix="/employees",
#     tags=["Employees"]
# )

# # Employee routes
# @router.get("/")
# async def home():
#     return {"message": "Hello Employees"}
# @router.get("/{employee_id}")
# async def get_employee(employee_id: int):
#     return {
#         "employee_id": employee_id,
#         "name": "Jeevan"
#     }

# # Include router in app
# app.include_router(router)

# # Root route
# @app.get("/")
# async def root():
#     return {"message": "Welcome to FastAPI"}