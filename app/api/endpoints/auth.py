from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext
from pydantic import BaseModel, ConfigDict, EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi_auth_jwt import JWTAuthBackend

from app.core.config import settings
from app.core.db import get_async_session
from app.models import User


router = APIRouter()

# move to app/core/user
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/auth/login',
    description='Войдите, используя свои имя пользователя и пароль',
    scheme_name='Войти'
    )


# move to app/schemas/auth
class PayloadSchema(BaseModel):
    """Схема для данных в JWT токене"""
    model_config = ConfigDict(strict=True)

    sub: str  # username/id пользователя
    email: Optional[EmailStr] = None
    is_active: bool = True


# move to app/schemas/auth
class AuthUser(BaseModel):
    """Схема для представления аутентифицированного пользователя"""
    username: str
    email: Optional[EmailStr] = None
    is_active: bool = True


# move to app/schemas/auth
class TokenInfo(BaseModel):
    """Схема для ответа с JWT токеном"""
    access_token: str
    token_type: str


# move to app/core/user
class AuthenticationSettings(BaseModel):
    """Настройки для JWT аутентификации"""
    secret: str = settings.secret
    jwt_algorithm: str = settings.jwt_algorithm
    expiration_seconds: int = settings.expiration_seconds


# move to app/core/user
auth_backend = JWTAuthBackend(
    authentication_config=AuthenticationSettings(),
    user_schema=PayloadSchema
)


# move to app/crud/auth
async def hash_password(password: str) -> str:
    """Хеширование пароля"""
    return pwd_context.hash(password)


# move to app/crud/auth
async def validate_auth_user(
        session: AsyncSession = Depends(get_async_session),
        username: str = Form(...),
        password: str = Form(...),
        ) -> User:
    """Проверка учетных данных пользователя"""
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password'
    )
    stmt = await session.execute(
        select(User).where(
            User.username == username
        )
    )
    db_user = stmt.scalars().first()

    if not db_user or not pwd_context.verify(password, db_user.password):
        raise auth_exception

    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User inactive'
        )

    return db_user


# move to app/crud/auth
async def get_current_payload(
    token: HTTPAuthorizationCredentials = Depends(oauth2_scheme)
) -> PayloadSchema:
    """Получение и валидация JWT токена"""
    try:
        payload = await auth_backend.get_current_user(token)
        return payload
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}"
        )


# move to app/crud/auth
async def get_current_auth_user(
    session: AsyncSession = Depends(get_async_session),
    payload: PayloadSchema = Depends(get_current_payload),
) -> AuthUser:
    """Получение текущего пользователя из БД"""
    stmt = await session.execute(
        select(User).where(User.username == payload.sub)
    )
    db_user = stmt.scalars().first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token invalid'
        )
    return AuthUser(
        username=db_user.username,
        email=db_user.email,
        is_active=db_user.is_active,
    )


# move to app/crud/auth
async def get_current_active_user(
    user: AuthUser = Depends(get_current_auth_user),
):
    """Проверка активности пользователя"""
    if user.is_active:
        return user
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail='User inactive'
    )


@router.post('/login',
             response_model=TokenInfo,
             summary='Авторизация пользователя',
             description='Войдите, используя свои имя пользователя и пароль',
             )
async def auth_user_issue_jwt(
    user: User = Depends(validate_auth_user),
):
    jwt_payload = {
        'sub': user.username,
        'email': user.email

    }
    token = await auth_backend.create_token(jwt_payload)
    return TokenInfo(
        access_token=token,
        token_type='Bearer'
    )


@router.get('/me',
            response_model=AuthUser,
            summary='Получение информации о текущем пользователе',
            )
async def read_user_me(
    current_user: AuthUser = Depends(get_current_active_user)
):
    return current_user


@router.get('/test',
            dependencies=[Depends(get_current_active_user)],
            summary='Тестовая функция',
            description='Тестовая функция для проверки внедрения звисимости',
            )
async def test():
    return {'test': 'Hello World'}
