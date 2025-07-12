from fastapi import FastAPI
from app.core.database import create_db_and_tables
from app.routers.routers import router

app = FastAPI(
    title="My FastAPI Application",
    description="A simple API for managing items and users.",
    version="1.0.0",
)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(router, prefix="/api/v1")
