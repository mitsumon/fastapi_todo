import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class User:
    """ユーザードメインエンティティ."""

    username: str
    email: str
    password: str
    is_active: bool = True
    is_superuser: bool = False
    id: Optional[uuid.UUID] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    def deactivate(self) -> None:
        """ユーザーを非アクティブ化."""
        self.is_active = False

    def activate(self) -> None:
        """ユーザーをアクティブ化."""
        self.is_active = True
