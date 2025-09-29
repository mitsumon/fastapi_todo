from datetime import datetime
from typing import AsyncGenerator, Callable, Generator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import Session, create_engine

from app.core.config import settings
from app.core.timezone import convert_utc_to_client_timezone
from app.core.timezone_middleware import get_client_timezone

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


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Get async database session."""
    async with AsyncSessionLocal() as session:
        yield session


def get_session() -> Generator[Session, None, None]:
    """Get sync database session for auth service."""
    with Session(sync_engine) as session:
        yield session


async def get_timezone_converter(request: Request) -> Callable:
    """タイムゾーン変換関数を取得."""
    client_tz = get_client_timezone(request)

    def converter(utc_datetime: datetime) -> str:
        return convert_utc_to_client_timezone(utc_datetime, client_tz)

    return converter
