from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.config import settings

# The async engine — note asyncpg:// not postgresql://
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,   # Logs all SQL — turn off in production
    pool_size=10,
    max_overflow=20,
)

# Session factory — creates new DB sessions on demand
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Don't expire objects after commit (avoids lazy load errors)
)

# Base class all ORM models inherit from
class Base(DeclarativeBase):
    pass

# Dependency injected into route handlers
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise