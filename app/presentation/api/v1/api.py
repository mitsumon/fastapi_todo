from fastapi import APIRouter

from app.presentation.api.v1.endpoints import users

api_router = APIRouter()
api_router.include_router(users.router, prefix='/users', tags=['Users'])


@api_router.get('/health')
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {'status': 'ok', 'message': 'FastAPI is running - api v1'}
