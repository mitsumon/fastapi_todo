from collections.abc import AsyncGenerator
from typing import Callable

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi_pagination import Page
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.usecases.user_usecases import UserUseCases
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


@router.get('', response_model=Page[UserResponse])
async def get_users_with_pagination(
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
) -> Page[UserResponse]:
    """全ユーザーを取得.

    - ページネーション対応.
    - パスワードなどの機密情報を除外.
    """
    try:
        return await user_use_cases.get_all_users_with_pagination()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from None


@router.get('/download')
async def download_users(
    user_use_cases: UserUseCases = Depends(get_user_use_cases),
    timezone_converter: Callable = Depends(get_timezone_converter),
) -> StreamingResponse:
    """全ユーザーを取得."""
    try:

        async def generate_csv_data() -> AsyncGenerator[str, None]:
            """CSVデータを生成するジェネレーター関数."""
            yield 'id,username,email,is_active,is_superuser,created_at,updated_at\n'
            async for user in user_use_cases.get_all_users_streaming():
                user_response = UserResponse.from_entity(user, timezone_converter)
                yield (
                    f'{user_response.id},'
                    f'{user_response.username},'
                    f'{user_response.email},'
                    f'{user_response.is_active},'
                    f'{user_response.is_superuser},'
                    f'{user_response.created_at},'
                    f'{user_response.updated_at}\n'
                )

        return StreamingResponse(
            content=generate_csv_data(),
            media_type='text/csv',
            headers={'Content-Disposition': 'attachment; filename=users.csv'},
        )
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
