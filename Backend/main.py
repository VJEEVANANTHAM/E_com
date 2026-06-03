from fastapi import FastAPI,Request,WebSocket,WebSocketDisconnect
from fastapi.templating import Jinja2Templates
from pathlib import Path
from database import engine, Base
from routes.auth import router as auth
from fastapi.middleware.cors import CORSMiddleware
from routes.products import router as products
from routes.session import router as session
from routes.cart import router as cart
from routes.orders import router as orders
# from routes.Login import router as Login_router
from routes.Profile import router as Profile_router
import os,requests,httpx
from fastapi.responses import StreamingResponse,HTMLResponse
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
from fastapi.security import OAuth2AuthorizationCodeBearer,OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(
    auth,
    tags=["auth"]
)
app.include_router(
    session
)
app.include_router(
    products,
    prefix="/products",
    tags=["Products"]
)
app.include_router(
    cart
)
app.include_router(
    orders
)
app.include_router(
    Profile_router,
    tags=["Profile_router"]
)

load_dotenv() # Loads GEMINI_API_KEY from .env
client = genai.Client() # Uses environment variable by default

class PromptRequest(BaseModel):
    prompt: str

# templates=Jinja2Templates(directory="templates")

# @app.get("/",include_in_schema=False)
# def home(request:Request):
#     return templates.TemplateResponse(request,"home.hml")
# @app.post("/api/generate")
# async def generate_response(request: PromptRequest):
#     try:
#        
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#             contents=request.prompt
#         )
        
#         return {"response": response.text}
#     except Exception as e:
#         raise HTTPException(status_code=500,detail=str(e))

@app.post("/api/generate")
async def generate_response(request: PromptRequest):
    try:
        def stream_generator():
            response = client.models.generate_content_stream(
                model="gemini-2.5-flash",
                contents=request.prompt
            )

            for chunk in response:
                if chunk.text:
                    print(chunk.text)
                    yield chunk.text
                    

        return StreamingResponse(
            stream_generator(),
            media_type="text/plain"
        )
        

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    



@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {"name": "John"}
    )


@app.get("/routes", response_class=HTMLResponse, include_in_schema=False)
async def routes_page(request: Request):
    routes = []

    for route in request.app.routes:
        methods = getattr(route, "methods", None)
        path = getattr(route, "path", None)

        if not methods or not path:
            continue

        routes.append({
            "path": path,
            "methods": sorted(method for method in methods if method not in {"HEAD", "OPTIONS"}),
            "name": getattr(route, "name", ""),
        })

    routes.sort(key=lambda item: item["path"])

    return templates.TemplateResponse(
        request,
        "routes.html",
        {"routes": routes}
    )


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(data)
    except WebSocketDisconnect:
        print("Client disconnected")


@app.get("/products-sync")
def get_products():

    response = requests.get(
        "https://dummyjson.com/roducts"
    )
    print("hello")
    for e in response:
        print(e)
    return response.json()


@app.get("/products-async")
async def get_products():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://dummyjson.com/products"
            )
        response.raise_for_status()
        
        return response.json()
    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="Third party API timeout"
        )
    # for e in response:
    #     print(e)
    
