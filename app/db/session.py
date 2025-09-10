from typing import AsyncGenerator, Generator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import Session, create_engine

from app.core.config import settings

# 非同期エンジン（本来の使用）
async_engine = create_async_engine(
    settings.database_url,
    pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# 同期エンジン（認証サービス用）
sync_engine = create_engine(settings.database_url_sync, pool_pre_ping=True)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


def get_session() -> Generator[Session, None, None]:
    """Get sync database session for auth service."""
    with Session(sync_engine) as session:
        yield session


ASession: AsyncSession = Depends(get_db)
