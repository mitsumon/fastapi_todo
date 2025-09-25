import re
import uuid
from datetime import datetime

from pydantic import (  # , model_validator
    BaseModel,
    EmailStr,
    Field,
    ValidationError,
    field_validator,
)

from app.core.timezone import convert_utc_to_client_timezone
from app.domain.entities.user import User as UserEntity


class UserCreate(BaseModel):
    """ユーザー作成スキーマ（バリデーション付き）."""

    username: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description='ユーザー名(3-50文字)',
    )
    email: EmailStr = Field(
        ...,
        description='有効なメールアドレス',
    )
    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description='パスワード(8-128文字)',
    )

    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        """ユーザー名のカスタムバリデーション."""
        if not v:
            raise ValidationError('ユーザー名は必須です')

        # # 英数字とアンダースコアのみ許可
        # if not re.match(r'^[a-zA-Z0-9_]+$', v):
        #     raise ValidationError('ユーザー名は英数字とアンダースコアのみ使用できます')

        # # 予約語チェック
        # reserved_words = ['admin', 'root', 'system', 'null', 'undefined']
        # if v.lower() in reserved_words:
        #     raise ValidationError(f'ユーザー名 "{v}" は予約語のため使用できません')

        return v.strip()

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """パスワードの強度チェック."""
        check = True
        if not v:
            check = False
            raise ValidationError('パスワードは必須です')

        # 大文字、小文字、数字、特殊文字を含むかチェック
        if not re.search(r'[A-Z]', v):
            check = False

        if not re.search(r'[a-z]', v):
            check = False

        if not re.search(r'\d', v):
            check = False

        if not check:
            raise ValidationError('パスワードには英字大文字、小文字、数字を含める必要があります')
        # if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
        #     raise ValidationError('パスワードには特殊文字を含める必要があります')

        # 一般的な脆弱なパスワードをチェック
        weak_passwords = ['password', '12345678', 'qwerty', 'letmein']
        if v.lower() in weak_passwords:
            raise ValidationError('より強力なパスワードを設定してください')

        return v

    class Config:
        from_attributes = True  # Pydantic v2 style for ORM mode


class UserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: str
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
