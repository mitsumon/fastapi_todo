import uuid
from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities.user import User


class UserRepository(ABC):
    """ユーザーリポジトリインターフェース."""

    @abstractmethod
    async def create(self, user: User) -> User:
        """ユーザーを作成."""
        pass

    @abstractmethod
    async def get_by_id(self, user_id: uuid.UUID) -> Optional[User]:
        """IDでユーザーを取得."""
        pass

    @abstractmethod
    async def get_by_email(self, email: str) -> Optional[User]:
        """メールアドレスでユーザーを取得."""
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        """全ユーザーを取得."""
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """ユーザーを更新."""
        pass

    @abstractmethod
    async def delete(self, user_id: uuid.UUID) -> bool:
        """ユーザーを削除."""
        pass
