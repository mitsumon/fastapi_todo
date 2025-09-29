from pydantic import BaseModel, EmailStr

from app.core.config import settings


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class CSRFSettings(BaseModel):
    secret_key: str = settings.CSRF_KEY
