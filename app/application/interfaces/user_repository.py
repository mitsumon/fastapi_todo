import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.user import User as UserEntity
from app.domain.entities.user import UserList as UserEntityList
from app.domain.value_objects.user_value_objects.email import Email
from app.domain.value_objects.uuid import UuId


class UserRepository(ABC):
    """ユーザーリポジトリインターフェース."""

    @abstractmethod
    async def create(self, user: UserEntity) -> UserEntity:
        """ユーザーを作成."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: UuId) -> Optional[UserEntity]:
        """IDでユーザーを取得."""
        pass

    @abstractmethod
    async def get_by_email(self, email: Email) -> Optional[UserEntity]:
        """メールアドレスでユーザーを取得."""
        pass

    @abstractmethod
    async def get_all(self) -> UserEntityList:
        """全ユーザーを取得."""
        pass

    @abstractmethod
    async def update(self, user: UserEntity) -> UserEntity:
        """ユーザーを更新."""
        pass

    @abstractmethod
    async def delete(self, user_id: uuid.UUID) -> bool:
        """ユーザーを削除."""
        pass
