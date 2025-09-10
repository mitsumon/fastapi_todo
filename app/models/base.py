import uuid
from datetime import datetime, timezone

from sqlalchemy import func
from sqlmodel import Field, SQLModel
from ulid import new as new_ulid


class BaseModel(SQLModel):
    """The base model for all other models."""

    id: uuid.UUID = Field(
        default_factory=lambda: new_ulid().uuid,
        primary_key=True,
        index=True,
        nullable=False,
    )


class TimestampMixin(SQLModel):
    """Mixin for adding timestamp fields."""

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False,
        sa_column_kwargs={'server_default': func.now()},
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
        nullable=False,
        sa_column_kwargs={'server_default': func.now(), 'onupdate': func.now()},
    )
    deleted_at: datetime | None = Field(
        default=None,
        nullable=True,
    )

    def soft_delete(self) -> None:
        """Mark the record as deleted by setting deleted_at timestamp."""
        self.deleted_at = datetime.now(timezone.utc).replace(tzinfo=None)

    def restore(self) -> None:
        """Restore a soft-deleted record by clearing deleted_at timestamp."""
        self.deleted_at = None

    @property
    def is_deleted(self) -> bool:
        """Check if the record is soft-deleted."""
        return self.deleted_at is not None
