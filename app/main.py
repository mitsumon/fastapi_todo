from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1 import api_router
from app.core.config import settings
from app.db.session import ASession

app = FastAPI(
    title='FastAPI Project',
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
)

# CORS設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get('/health')
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {'status': 'ok', 'message': 'FastAPI is running'}


@app.get('/dbtest')
async def db_test(db: AsyncSession = ASession) -> dict[str, str]:
    """Database test endpoint."""
    from sqlalchemy import text

    await db.execute(text('SELECT 1'))
    return {'status': 'ok', 'message': 'Database connection is working'}
