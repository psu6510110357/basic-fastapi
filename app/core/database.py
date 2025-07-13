import os
from dotenv import load_dotenv
from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from typing import AsyncIterator
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from typing import Optional

load_dotenv()

connect_args = {"ssl": True}


engine: Optional[AsyncEngine] = None


database_url = os.getenv("DATABASE_URL_PG") or "sqlite+aiosqlite:///database.db"


async def init_db():
    print(f"Initializing database with URL: {database_url}")
    """Initialize the database engine and create tables."""
    global engine

    engine = create_async_engine(
        database_url,
        echo=True,
        future=True,
        connect_args=connect_args,
    )

    await drop_db_and_tables()
    await create_db_and_tables()


async def create_db_and_tables():
    """Create database tables."""
    if engine is None:
        raise Exception("Database engine is not initialized. Call init_db() first.")
    async with engine.begin() as conn:
        print(conn.engine.url.drivername)
        # await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def drop_db_and_tables():
    """Drop database tables."""
    if engine is None:
        raise Exception("Database engine is not initialized. Call init_db() first.")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


async def get_session() -> AsyncIterator[AsyncSession]:
    """Get async database session."""
    if engine is None:
        raise Exception("Database engine is not initialized. Call init_db() first.")

    async_session = async_sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )
    async with async_session() as session:
        yield session


async def close_db():
    """Close database connection."""
    global engine
    if engine is not None:
        await engine.dispose()
        engine = None
