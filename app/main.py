from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
import httpx
from .routes import home, github

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    app.state.client = httpx.AsyncClient(timeout=10.0)
    yield
    # Shutdown
    await app.state.client.aclose()

app = FastAPI(title="GitHub Repository Analyzer", lifespan=lifespan)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(home.router)
app.include_router(github.router)

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})