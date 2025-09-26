from dataclasses import dataclass
from datetime import datetime, timezone  # noqa: F401
from typing import Optional

from app.domain.value_objects.created_at import CreatedAt
from app.domain.value_objects.deleted_at import DeletedAt
from app.domain.value_objects.updated_at import UpdatedAt
from app.domain.value_objects.user_value_objects.email import Email
from app.domain.value_objects.user_value_objects.is_active import IsActive
from app.domain.value_objects.user_value_objects.is_superuser import IsSuperUser
from app.domain.value_objects.user_value_objects.password import Password
from app.domain.value_objects.user_value_objects.username import Username
from app.domain.value_objects.uuid import UuId


@dataclass
class User:
    """ユーザードメインエンティティ."""

    username: Username
    email: Email
    password: Password
    is_active: IsActive = IsActive(True)
    is_superuser: IsSuperUser = IsSuperUser(False)
    id: Optional[UuId] = None
    created_at: Optional[CreatedAt] = None
    updated_at: Optional[UpdatedAt] = None
    deleted_at: Optional[DeletedAt] = None

    def deactivate(self) -> None:
        """ユーザーを非アクティブ化."""
        self.is_active = IsActive(False)
        # self.updated_at = UpdatedAt(datetime.now(timezone.utc))

    def activate(self) -> None:
        """ユーザーをアクティブ化."""
        self.is_active = IsActive(True)


@dataclass
class UserList:
    """ユーザーリストドメインエンティティ."""

    users: list[User]
    total_count: int

    def add_user(self, user: User) -> None:
        """ユーザーをリストに追加."""
        self.users.append(user)
        self.total_count += 1

    def remove_user(self, user: User) -> None:
        """ユーザーをリストから削除."""
        self.users.remove(user)
        self.total_count -= 1

    def get_user_by_id(self, user_id: UuId) -> Optional[User]:
        """IDでユーザーを取得."""
        for user in self.users:
            if user.id == user_id:
                return user
        return None

    def filter_active_users(self) -> 'UserList':
        """アクティブなユーザーのみを取得."""
        return UserList([user for user in self.users if user.is_active.value], 0)

    def filter_inactive_users(self) -> 'UserList':
        """非アクティブなユーザーのみを取得."""
        return UserList([user for user in self.users if not user.is_active.value], 0)

    def filter_not_soft_deleted_users(self) -> 'UserList':
        """ソフトデリートされていないユーザーのみを取得."""
        return UserList([user for user in self.users if user.deleted_at is None], 0)

    def __len__(self) -> int:
        """ユーザーリストの長さを返す."""
        return self.total_count

    def __iter__(self):
        """ユーザーリストのイテレータを返す."""
        return iter(self.users)
