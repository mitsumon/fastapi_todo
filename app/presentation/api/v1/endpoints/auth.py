from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.usecases.auth_usecases import AuthUseCases
from app.core.config import settings
from app.core.dependencies import get_async_session
from app.infrastructure.database.repositories.user_repository_impl import UserRepositoryImpl
from app.presentation.schemas.auth_schemas import TokenResponse

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/auth/login')


async def get_auth_use_cases(
    session: AsyncSession = Depends(get_async_session),
) -> AuthUseCases:
    """認証ユースケースの依存性注入."""
    user_repository = UserRepositoryImpl(session)
    return AuthUseCases(user_repository)


@router.post('/login', response_model=TokenResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    auth_use_cases: AuthUseCases = Depends(get_auth_use_cases),
) -> TokenResponse:
    """ログイン認証を行い、JWTトークンを返す."""
    # OAuth2PasswordRequestFormではemailがusernameフィールドに入る
    user = await auth_use_cases.authenticate_user(
        email=form_data.username,
        password=form_data.password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='メールアドレスまたはパスワードが正しくありません',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='アカウントが無効化されています',
        )

    return await auth_use_cases.create_access_token_for_user(user)
