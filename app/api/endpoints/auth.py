from typing import Annotated, TYPE_CHECKING

from fastapi import APIRouter, Depends

from app.core.auth.dependencies import get_current_auth_user_for_refresh
from app.crud.auth import validate_auth_user, last_login
from app.core.db import get_async_session
from app.schemas.auth import AuthUser, TokenInfo
from app.services.auth import (
    create_access_token,
    create_refresh_token
)

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post("/login",
             response_model=TokenInfo,
             summary="Authorization",
             description="Log in using your username and password",
             )
async def auth_user_issue_jwt(
        user: Annotated[AuthUser, Depends(validate_auth_user)],
        session: Annotated["AsyncSession", Depends(get_async_session)]
):
    access_token = await create_access_token(user)
    refresh_token = await create_refresh_token(user)
    await last_login(user, session)
    return TokenInfo(
        access_token=access_token,
        refresh_token=refresh_token,
    )


@router.post("/refresh",
             response_model=TokenInfo,
             response_model_exclude_none=True,
             summary='Refresh jwt issuance',
             )
async def auth_user_issue_refresh_jwt(
        user: Annotated[AuthUser, Depends(get_current_auth_user_for_refresh)],
):
    access_token = await create_access_token(user)
    return TokenInfo(access_token=access_token)
