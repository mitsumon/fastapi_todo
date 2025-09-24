import uuid
from datetime import datetime, timezone

from sqlmodel import Field

from app.infrastructure.database.models.base import BaseModel, TimestampMixin


class Todo(BaseModel, TimestampMixin, table=True):
    __tablename__ = 'todos'

    title: str = Field(max_length=255, nullable=False)
    description: str | None = Field(default=None, max_length=1024)
    is_completed: bool = Field(default=False, nullable=False)
    due_date: datetime | None = Field(default=None, nullable=True)
    user_id: uuid.UUID = Field(foreign_key='users.id', nullable=False)
