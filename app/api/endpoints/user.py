from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends, Form, Path

from app.api.endpoints.validators import validate_user_before_create
from app.core.auth.dependencies import get_current_auth_user
from app.core.db import get_async_session
from app.crud.user import create_user, update_user
from app.schemas.auth import AuthUser
from app.schemas.user import UserCreate, UserOut, UserUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    "/sign-up",
    response_model=UserOut,
    summary="User creation"
)
async def create_new_user(
        session: Annotated["AsyncSession", Depends(get_async_session)],
        user_in: Annotated[UserCreate, Form()],
):
    await validate_user_before_create(user_in, session)
    new_user = await create_user(user_in, session)
    return new_user


@router.get("/me",
            response_model=AuthUser,
            response_model_exclude_none=True,
            summary="Current user information receive",
            )
async def read_user_me(
        current_user: Annotated[AuthUser, Depends(get_current_auth_user)]
):
    return current_user


@router.patch(
    "/{user_id}/update",
    response_model=UserOut,
    summary="User update",
)
async def update_existed_user(
        user_id: Annotated[int, Path(description="user id")],
        user_update: Annotated[UserUpdate, Form()],
        session: Annotated["AsyncSession", Depends(get_async_session)],
        current_user: Annotated[AuthUser, Depends(get_current_auth_user)],
):
    result = await update_user(
        user_id,
        user_update,
        session,
        current_user,
    )
    return result
