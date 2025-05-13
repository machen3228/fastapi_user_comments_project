from fastapi import APIRouter, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import validate_user_before_create
from app.core.auth.dependencies import get_current_auth_user
from app.core.db import get_async_session
from app.crud.user import create_user, update_user
from app.schemas.auth import AuthUser
from app.schemas.user import UserCreate, UserOut, UserUpdate


router = APIRouter()


@router.post(
    '/sign-up',
    response_model=UserOut,
    summary='Регистрация пользователя'
)
async def create_new_user(
        session: AsyncSession = Depends(get_async_session),
        user_in: UserCreate = Depends(UserCreate.as_form)
):
    await validate_user_before_create(user_in, session)
    new_user = await create_user(user_in, session)
    return new_user


@router.get('/me',
            response_model=AuthUser,
            response_model_exclude_none=True,
            summary='Получение информации о текущем пользователе',
            )
async def read_user_me(
        current_user: AuthUser = Depends(get_current_auth_user)
):
    return current_user


@router.patch(
    '/{user_id}/update',
    response_model=UserOut,
    summary='Редактирование пользователя',
)
async def update_existed_user(
        user_id: int = Path(description='id пользователя'),
        user_update: UserUpdate = Depends(UserUpdate.as_form),
        session: AsyncSession = Depends(get_async_session),
        current_user: AuthUser = Depends(get_current_auth_user)
):
    result = await update_user(
        user_id,
        user_update,
        session,
        current_user,
    )
    return result
