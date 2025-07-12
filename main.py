from fastapi import FastAPI
from app.core.database import (
    create_db_and_tables,
    drop_db_and_tables,
    init_db,
    close_db,
)
from app.routers.routers import router
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    await init_db()  # Initialize the database engine
    await drop_db_and_tables()
    await create_db_and_tables()
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title="My FastAPI Application",
    description="A simple API for managing items and users.",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(router, prefix="/api/v1")
