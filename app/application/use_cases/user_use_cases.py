import uuid

from app.core.exceptions import UserAlreadyExistsError, UserNotFoundError
from app.core.security import hash_password
from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository


class UserUseCases:
    """ユーザー関連のユースケース."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    async def get_all_users(self) -> list[User]:
        """全ユーザーを取得."""
        return await self._user_repository.get_all()

    async def get_user_by_id(self, user_id: uuid.UUID) -> User:
        """IDでユーザーを取得."""
        user = await self._user_repository.get_by_id(user_id)
        if not user:
            raise UserNotFoundError(f'User with ID {user_id} not found')
        return user

    async def create_user(self, user_data: dict) -> User:
        """新しいユーザーを作成."""
        # 既存ユーザーチェック
        existing_user = await self._user_repository.get_by_email(user_data['email'])
        if existing_user:
            raise UserAlreadyExistsError(f'User with email {user_data["email"]} already exists')

        # ドメインエンティティ作成
        user = User(
            # id=uuid.uuid4(),
            username=user_data['username'],
            email=user_data['email'],
            password=hash_password(user_data['password']),
        )

        return await self._user_repository.create(user)

    async def deactivate_user(self, user_id: uuid.UUID) -> User:
        """ユーザーを非アクティブ化."""
        user = await self.get_user_by_id(user_id)
        user.deactivate()
        return await self._user_repository.update(user)
