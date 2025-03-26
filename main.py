from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Medspa API",
    description="API for the Medspa app",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)


@app.get("/")
def read_root():
    return {
        "message": "Welcome to the Medspa API",
        "docs": "/docs",
        "redoc": "/redoc"
    } 