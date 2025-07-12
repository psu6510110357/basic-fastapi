import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import httpx
from httpx import AsyncClient
from sqlmodel import SQLModel


from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import async_sessionmaker
import pytest_asyncio

# Update this import path to match where your FastAPI app instance is defined]
from app.main import app
from app.core.database import get_session


@pytest_asyncio.fixture
async def engine():
    """Create test database engine."""
    sql_url = os.getenv("DATABASE_URL_PG") or "sqlite+aiosqlite:///test_database.db"
    engine = create_async_engine(
        sql_url,
        connect_args=(
            {"check_same_thread": False} if sql_url.startswith("sqlite") else {}
        ),
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)

    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def session(engine):
    """Create test database session."""
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def client(session):
    """Create test client with dependency override."""

    async def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override

    transport = httpx.ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url="http://localhost:8000"
    ) as client:
        yield client

    app.dependency_overrides.clear()
