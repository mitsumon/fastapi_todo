from fastapi import APIRouter

from app.presentation.api.v1.endpoints import auth, users

api_router = APIRouter()
# 認証関連のルーターを登録
api_router.include_router(auth.router, prefix='/auth', tags=['Auth'])
# ユーザー関連のルーターを登録
api_router.include_router(users.router, prefix='/users', tags=['Users'])


@api_router.get('/health')
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {'status': 'ok', 'message': 'FastAPI is running - api v1'}
