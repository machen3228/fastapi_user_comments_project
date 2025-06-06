from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials

from jwt import InvalidTokenError

from sqlalchemy import select

from app.core.auth.backend import auth_backend
from app.core.db import get_async_session
from app.core.security import oauth2_scheme
from app.schemas.auth import PayloadSchema
from app.models import UsersORM
if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

TOKEN_TYPE_FIELD = 'type'
ACCESS_TOKEN_TYPE = 'access'
REFRESH_TOKEN_TYPE = 'refresh'


async def get_current_payload(
        token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]
) -> PayloadSchema:
    try:
        payload = await auth_backend.get_current_user(token)
        return payload
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {e}"
        )


async def validate_token_type(
        payload: PayloadSchema,
        token_type: str
) -> bool:
    current_token_type = payload.type
    if current_token_type == token_type:
        return True
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=(f'Invalid token type {current_token_type!r} '
                f'expected {token_type!r}'),
    )


async def get_user_by_sub(
        payload: PayloadSchema,
        session: Annotated["AsyncSession", Depends(get_async_session)],
) -> UsersORM:
    query = await session.execute(
        select(UsersORM).where(UsersORM.id == payload.sub)
    )
    db_user = query.scalars().first()
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Token invalid'
        )
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='UsersORM inactive'
        )
    return db_user


def get_auth_user_from_token_by_type(token_type: str):
    async def get_auth_user_from_token(
            payload: Annotated[PayloadSchema, Depends(get_current_payload)],
            session: Annotated["AsyncSession", Depends(get_async_session)],
    ) -> UsersORM:
        await validate_token_type(payload, token_type)
        return await get_user_by_sub(payload, session)

    return get_auth_user_from_token


get_current_auth_user = get_auth_user_from_token_by_type(ACCESS_TOKEN_TYPE)
get_current_auth_user_for_refresh = get_auth_user_from_token_by_type(REFRESH_TOKEN_TYPE)
