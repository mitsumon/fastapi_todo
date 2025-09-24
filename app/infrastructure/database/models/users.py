from sqlmodel import Field

from app.infrastructure.database.models.base import BaseModel, TimestampMixin


class User(BaseModel, TimestampMixin, table=True):
    __tablename__ = 'users'

    username: str = Field(unique=True, index=True, max_length=50)
    email: str = Field(unique=True, index=True, max_length=255)
    password: str = Field(max_length=128)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
