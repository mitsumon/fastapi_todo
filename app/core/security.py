from datetime import datetime, timedelta, timezone
from typing import Any

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# パスワードハッシュ化の設定
pwd_context = CryptContext(
    schemes=['argon2'],
    deprecated='auto',
    argon2__time_cost=3,  # 時間コスト
    argon2__memory_cost=65536,  # メモリコスト (64MB)
    argon2__parallelism=1,  # 並列度
)


# JWTの設定
def create_access_token(subject: Any) -> str:
    """アクセストークンを作成."""
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )

    to_encode = {'exp': expire, 'sub': str(subject)}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def hash_password(password: str) -> str:
    """パスワードをハッシュ化."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードを検証."""
    return pwd_context.verify(plain_password, hashed_password)
