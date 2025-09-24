from passlib.context import CryptContext

# パスワードハッシュ化の設定
pwd_context = CryptContext(
    schemes=['argon2'],
    deprecated='auto',
    argon2__time_cost=3,  # 時間コスト
    argon2__memory_cost=65536,  # メモリコスト (64MB)
    argon2__parallelism=1,  # 並列度
)


def hash_password(password: str) -> str:
    """パスワードをハッシュ化."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードを検証."""
    return pwd_context.verify(plain_password, hashed_password)
