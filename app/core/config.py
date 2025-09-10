"""アプリケーション設定管理モジュール.

環境変数を使用して設定を管理します。
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーション設定クラス."""

    # API設定
    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = 'Todo API'

    # 環境設定
    ENVIRONMENT: str = Field(default='development', description='実行環境')
    DEBUG: bool = Field(default=True, description='デバッグモード')

    # セキュリティ設定
    SECRET_KEY: str = Field(
        default='your-secret-key-change-in-production',
        description='JWT署名用のシークレットキー',
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description='アクセストークンの有効期限（分）',
    )

    # AWS Cognito設定（本番環境用）
    COGNITO_USER_POOL_ID: str = Field(default='', description='Cognito ユーザープールID')
    COGNITO_CLIENT_ID: str = Field(default='', description='Cognito クライアントID')
    COGNITO_REGION: str = Field(default='', description='Cognito リージョン')
    COGNITO_JWKS_URL: str = Field(
        default='',
        description='Cognito JWKS URL',
    )

    # # Google OAuth設定（本番環境用）
    # GOOGLE_CLIENT_ID: str = Field(default='', description='Google OAuth クライアントID')
    # GOOGLE_CLIENT_SECRET: str = Field(
    #     default='',
    #     description='Google OAuth クライアントシークレット',
    # )
    # GOOGLE_REDIRECT_URI: str = Field(
    #     default='http://localhost:8000/api/v1/auth/google/callback',
    #     description='Google OAuth リダイレクトURI',
    # )

    # CORS設定
    BACKEND_CORS_ORIGINS: list[str] = Field(
        default=['http://localhost:3000', 'http://localhost:8000'],
        description='CORS許可オリジン',
    )

    # Database
    POSTGRES_HOST: str = Field(default='localhost', description='PostgreSQLサーバー')
    POSTGRES_USER: str = Field(default='user', description='PostgreSQLユーザー')
    POSTGRES_PASSWORD: str = Field(default='password', description='PostgreSQLパスワード')
    POSTGRES_DB: str = Field(default='esop_db', description='PostgreSQLデータベース名')

    @property
    def is_production(self) -> bool:
        """本番環境かどうかを判定."""
        return self.ENVIRONMENT.lower() == 'production'

    @property
    def is_development(self) -> bool:
        """開発環境かどうかを判定."""
        return self.ENVIRONMENT.lower() == 'development'

    @property
    def database_url(self) -> str:
        """Async database URL for the application."""
        if self.SQLALCHEMY_DATABASE_URI:
            return self.SQLALCHEMY_DATABASE_URI
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}'

    @property
    def database_url_sync(self) -> str:
        """Sync database URL for Alembic migrations."""
        if self.SQLALCHEMY_DATABASE_URI:
            # If a full URI is provided, convert it for sync usage
            return self.SQLALCHEMY_DATABASE_URI.replace('postgresql+asyncpg', 'postgresql')
        return f'postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
