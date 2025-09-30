from typing import Optional

from app.application.interfaces.user_repository import UserRepository
from app.core.security import create_access_token, verify_password
from app.domain.entities.user import User as UserEntity
from app.domain.value_objects.user_value_objects.email import Email


class AuthUseCases:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def authenticate_user(self, email: str, password: str) -> Optional[UserEntity]:
        """ユーザーを認証する."""
        user = await self.user_repository.get_by_email(Email(email))
        if not user:
            return None
        if not verify_password(password, user.password.value):
            return None
        return user

    async def create_access_token_for_user(self, user: UserEntity) -> dict:
        """ユーザー用のアクセストークンを生成."""
        access_token = create_access_token(
            subject=user.email,
        )
        return {
            'access_token': access_token,
            'token_type': 'bearer',
        }
