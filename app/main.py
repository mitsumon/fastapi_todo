# デフォルト設定を変更
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

# from fastapi_csrf_protect import CsrfProtect
# from fastapi_csrf_protect.exceptions import CsrfProtectError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.dependencies import get_async_session
from app.core.timezone_middleware import TimezoneMiddleware
from app.presentation.api.v1 import api_router
from app.presentation.schemas.auth_schemas import CSRFSettings

app = FastAPI(
    title='FastAPI ToDo Project',
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
)

# タイムゾーンミドルウェア設定
app.add_middleware(
    TimezoneMiddleware,
)
# CORS設定
whitelist = ['http://localhost:3000']
app.add_middleware(
    CORSMiddleware,
    allow_origins=whitelist,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(api_router, prefix=settings.API_V1_STR)


# @CsrfProtect.load_config
# def get_csrf_config() -> CSRFSettings:
#     """CSRF設定の読み込み."""
#     return CSRFSettings()


@app.get('/health')
async def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {'status': 'ok', 'message': 'FastAPI is running'}


@app.get('/dbtest')
async def db_test(db: AsyncSession = Depends(get_async_session)) -> dict[str, str]:
    """Database test endpoint."""
    from sqlalchemy import text

    await db.execute(text('SELECT 1'))
    return {'status': 'ok', 'message': 'Database connection is working'}


# 以下はいろいろ実験的なコード

import asyncio
import json

from fastapi.responses import StreamingResponse


# 非同期ジェネレータ関数
async def generate_large_data() -> str:
    for i in range(1000):
        # 重たい処理を模擬
        await asyncio.sleep(0.01)
        yield json.dumps({'id': i, 'value': f'Data point {i}'}) + '\n'


# ストリーミングレスポンスを返すエンドポイント
@app.get('/stream-data/')
async def stream_data() -> StreamingResponse:
    return StreamingResponse(
        generate_large_data(),
        media_type='application/json',
    )


def generate_csv_data():
    # ヘッダーを生成
    yield 'id,name,value\n'

    # 大量のデータ行を少しずつ生成
    for i in range(1, 10001):
        yield f'{i},User {i},{(i * 10)}\n'


@app.get('/export/csv')
async def export_csv() -> StreamingResponse:
    return StreamingResponse(
        content=generate_csv_data(),
        media_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename=large_data.csv'},
    )


# FastAPIアプリケーションにページネーション機能を追加
add_pagination(app)
