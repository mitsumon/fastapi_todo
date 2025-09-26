import uuid
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import delete, select

from app.application.interfaces.user_repository import UserRepository
from app.domain.entities.user import User as UserEntity
from app.domain.entities.user import UserList as UserEntityList
from app.domain.value_objects.created_at import CreatedAt
from app.domain.value_objects.updated_at import UpdatedAt
from app.domain.value_objects.user_value_objects.email import Email
from app.domain.value_objects.user_value_objects.is_active import IsActive
from app.domain.value_objects.user_value_objects.is_superuser import IsSuperUser
from app.domain.value_objects.user_value_objects.password import Password
from app.domain.value_objects.user_value_objects.username import Username
from app.domain.value_objects.uuid import UuId
from app.infrastructure.database.models.users import User as UserModel


class UserRepositoryImpl(UserRepository):
    """ユーザーリポジトリ実装."""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, user: UserEntity) -> UserEntity:
        """ユーザーを作成."""
        user_model = self._entity_to_model(user)
        self._session.add(user_model)
        await self._session.commit()
        await self._session.refresh(user_model)
        return self._model_to_entity(user_model)

    async def get_by_id(self, user_id: UuId) -> Optional[UserEntity]:
        """IDでユーザーを取得."""
        statement = select(UserModel).where(UserModel.id == str(user_id))
        result = await self._session.execute(statement)
        user_model = result.scalar_one_or_none()
        return self._model_to_entity(user_model) if user_model else None

    async def get_by_email(self, email: Email) -> Optional[UserEntity]:
        """メールアドレスでユーザーを取得."""
        statement = select(UserModel).where(UserModel.email == email.value)
        result = await self._session.execute(statement)
        user_model = result.scalar_one_or_none()
        return self._model_to_entity(user_model) if user_model else None

    async def get_all(self) -> UserEntityList:
        """全ユーザーを取得."""
        statement = select(UserModel)
        result = await self._session.execute(statement)
        user_models = result.scalars().all()
        user_list = UserEntityList(
            [self._model_to_entity(model) for model in user_models],
            len(user_models),
        )
        return user_list

    async def update(self, user: UserEntity) -> UserEntity:
        """ユーザーを更新."""
        # 既存のユーザーを取得
        statement = select(UserModel).where(UserModel.id == user.id)
        result = await self._session.execute(statement)
        user_model = result.scalar_one_or_none()

        if not user_model:
            raise ValueError(f'User with ID {user.id} not found')

        # フィールドを更新
        user_model.username = user.username
        user_model.email = user.email
        # user_model.password = user.password
        user_model.is_active = user.is_active
        user_model.is_superuser = user.is_superuser
        user_model.updated_at = user.updated_at

        await self._session.commit()
        await self._session.refresh(user_model)
        return self._model_to_entity(user_model)

    async def delete(self, user_id: UuId) -> bool:
        """ユーザーを削除."""
        statement = delete(UserModel).where(UserModel.id == str(user_id))
        result = await self._session.execute(statement)
        await self._session.commit()
        return result.rowcount > 0

    def _model_to_entity(self, model: UserModel) -> UserEntity:
        """DBモデル → ドメインエンティティ変換."""
        return UserEntity(
            id=UuId(model.id),
            username=Username(model.username),
            email=Email(model.email),
            password=Password(model.password),
            is_active=IsActive(model.is_active),
            is_superuser=IsSuperUser(model.is_superuser),
            created_at=CreatedAt(model.created_at),
            updated_at=UpdatedAt(model.updated_at),
        )

    def _entity_to_model(self, entity: UserEntity) -> UserModel:
        """ドメインエンティティ → DBモデル変換."""
        return UserModel(
            # id=entity.id,
            username=entity.username,
            email=entity.email,
            password=entity.password,
            # is_active=entity.is_active,
            # is_superuser=entity.is_superuser,
            # created_at=entity.created_at,
            # updated_at=entity.updated_at,
        )
