import uuid
from typing import Callable

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.use_cases.user_use_cases import UserUseCases
from app.core.dependencies import get_async_session, get_timezone_converter
from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from app.presentation.schemas.user_schemas import UserCreate, UserResponse

router = APIRouter()


async def get_user_use_cases(
    session: AsyncSession = Depends(get_async_session),
) -> UserUseCases:
    """ユーザーユースケースの依存性注入."""
    user_repository = UserRepositoryImpl(session)
    return UserUseCases(user_repository)


@router.get('', response_model=list[UserResponse])
async def get_users(
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    timezone_converter: Callable = Depends(get_timezone_converter),
) -> list[UserResponse]:
    """全ユーザーを取得."""
    try:
        users = await user_use_cases.get_all_users()
        return [UserResponse.from_entity(user, timezone_converter) for user in users]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from None


@router.get('/{user_id}', response_model=UserResponse)
async def get_user(
    user_id: uuid.UUID,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
) -> UserResponse:
    """特定のユーザーを取得."""
    try:
        user = await user_use_cases.get_user_by_id(user_id)
        return UserResponse.from_entity(user)
    except UserNotFoundError:
        raise HTTPException(status_code=404, detail='User not found') from None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from None


@router.post('', response_model=UserResponse)
async def create_user(
    user_data: UserCreate,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
) -> UserResponse:
    """ユーザーを作成."""
    try:
        user = await user_use_cases.create_user(user_data.model_dump())
        return UserResponse.from_entity(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=409, detail=str(e)) from None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from None


@router.post('/debug', response_model=dict)
async def debug_create_user(
    user_data: UserCreate,
) -> dict:
    """デバッグ用エンドポイント."""
    try:
        data = user_data.model_dump()
        return {'received_data': data, 'status': 'ok'}
    except Exception as e:
        return {'error': str(e), 'type': type(e).__name__}
