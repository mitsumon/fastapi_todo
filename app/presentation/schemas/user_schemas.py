import uuid
from datetime import datetime

from pydantic import BaseModel

from app.core.timezone import convert_utc_to_client_timezone
from app.domain.entities.user import User as UserEntity


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

    class Config:
        from_attributes = True  # Pydantic v2 style for ORM mode


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(
        cls,
        user: UserEntity,
        timezone_converter: callable = convert_utc_to_client_timezone,
    ) -> 'UserResponse':
        """ドメインエンティティから変換(タイムゾーン変換含む)."""
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_superuser=user.is_superuser,
            created_at=timezone_converter(user.created_at),
            updated_at=timezone_converter(user.updated_at),
        )

    class Config:
        from_attributes = True  # Pydantic v2 style for ORM mode
