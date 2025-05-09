from fastapi import APIRouter, Depends

from app.core.auth.dependencies import get_current_auth_user_for_refresh
from app.crud.auth import validate_auth_user
from app.schemas.auth import AuthUser, TokenInfo
from app.services.auth import (
    create_access_token,
    create_refresh_token
)


router = APIRouter()


@router.post('/login',
             response_model=TokenInfo,
             summary='Авторизация пользователя',
             description='Войдите, используя свои имя пользователя и пароль',
             )
async def auth_user_issue_jwt(
    user: AuthUser = Depends(validate_auth_user),
):
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post('/refresh',
             response_model=TokenInfo,
             response_model_exclude_none=True,
             summary='Получение refresh-токена',
             )
async def auth_user_issue_refresh_jwt(
    user: AuthUser = Depends(get_current_auth_user_for_refresh),
):
    access_token = await create_access_token(user)
    return TokenInfo(access_token=access_token)

