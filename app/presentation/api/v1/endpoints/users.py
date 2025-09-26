import uuid
from typing import Callable

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.usecases.user_usecases import UserUseCases
from app.core.dependencies import get_async_session, get_timezone_converter
from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.domain.value_objects.user_value_objects.email import Email
from app.domain.value_objects.user_value_objects.password import Password
from app.domain.value_objects.user_value_objects.username import Username
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
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from None


@router.get('/{user_id}', response_model=UserResponse)
async def get_user(
    user_id: str,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
) -> UserResponse:
    """特定のユーザーを取得."""
    try:
        user = await user_use_cases.get_user_by_id(user_id)
        return UserResponse.from_entity(user)
    except UserNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        ) from None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from None


@router.post('', response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
) -> UserResponse:
    """ユーザーを作成."""
    try:
        user = await user_use_cases.create_user(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
        )
        return UserResponse.from_entity(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e),
        ) from None
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors,
        ) from None
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from None
