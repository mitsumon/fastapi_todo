import uuid
from typing import AsyncGenerator

from fastapi_pagination import Page

from app.application.interfaces.user_repository import UserRepository
from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.core.security import hash_password
from app.domain.entities.user import User as UserEntity
from app.domain.entities.user import UserList as UserEntityList
from app.domain.value_objects.user_value_objects.email import Email
from app.domain.value_objects.user_value_objects.password import Password
from app.domain.value_objects.user_value_objects.username import Username
from app.domain.value_objects.uuid import UuId
from app.presentation.schemas.user_schemas import UserResponse


class UserUseCases:
    """ユーザー関連のユースケース."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def get_all_users(self) -> UserEntityList:
        """全ユーザーを取得."""
        return await self._user_repository.get_all()

    async def get_all_users_streaming(self) -> AsyncGenerator[UserEntity, None]:
        """全ユーザーをストリーミングで取得."""
        async for user in self._user_repository.get_all_streaming():
            yield user

    async def get_all_users_with_pagination(self) -> Page[UserResponse]:
        """全ユーザーを取得.

        - ページネーション対応.
        - パスワードなどの機密情報を除外.
        """
        user_list = await self._user_repository.get_all_safe()
        return user_list

    async def get_user_by_id(self, user_id: str) -> UserEntity:
        """IDでユーザーを取得."""
        user = await self._user_repository.get_by_id(UuId(user_id))
        if not user:
            raise UserNotFoundError(f'User with ID {user_id} not found')
        return user

    async def create_user(self, username: str, email: str, password: str) -> UserEntity:
        """新しいユーザーを作成."""
        # 既存ユーザーチェック
        username = Username(username)
        email = Email(email)
        password = Password(password)
        existing_user = await self._user_repository.get_by_email(email)
        if existing_user:
            raise UserAlreadyExistsError(f'User with email `{email}` already exists')

        # ドメインエンティティ作成
        user = UserEntity(
            username=username.value,
            email=email.value,
            password=hash_password(password.value),
        )

        return await self._user_repository.create(user)

    async def deactivate_user(self, user_id: uuid.UUID) -> UserEntity:
        """ユーザーを非アクティブ化."""
        user = await self.get_user_by_id(user_id)
        user.deactivate()
        return await self._user_repository.update(user)
