from contextlib import asynccontextmanager
from fastapi import FastAPI

from database import init_db
from routes import medspa, services, appointments


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
    lifespan=lifespan,
)

app.include_router(medspa.router)
app.include_router(services.router)
app.include_router(appointments.router)
