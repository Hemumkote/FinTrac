from contextlib import asynccontextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from typing import AsyncGenerator

from app.db.base import Base
from core.config import settings

# this creates a connection pool
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.ENVIRONMENT == "development",
    ## pool_size=10,
    ## max_overflow=20,
    ## pool_timeout=30,
    ## pool_timeout=30,
)

# creates database sessions Session Factory
async_session_factory = async_sessionmaker(  ## each call produces an automated session
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> (
    AsyncGenerator[AsyncSession, None]
):  ## it is returning the object of type AsyncGenerator which yields AsyncSession objects and it sends None
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()  ## commit if no exceptions
        except Exception:
            await session.rollback()  ## rollback if any exceptions
            raise
        finally:
            await session.close()  ## close the session


@asynccontextmanager  ## decorator to make context manager for async functions espically used for background tasks cron jobs, seeding and migrations
async def get_async_context() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()  ## commit if no exceptions
        except Exception:
            await session.rollback()  ## rollback if any exceptions
            raise
        finally:
            await session.close()  ## close the session


async def init_db() -> None:
    """Initialize the database by creating all tables."""

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """Dispose of the database engine."""
    await engine.dispose()
