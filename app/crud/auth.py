from datetime import UTC
from typing import Annotated, TYPE_CHECKING

from fastapi import Depends, Form, HTTPException, status
from sqlalchemy import select, func

from app.core.db import get_async_session
from app.core.security import verify_password
from app.models import UsersORM
from app.schemas.auth import AuthUser
if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def validate_auth_user(
        username: Annotated[str, Form(...)],
        password: Annotated[str, Form(...)],
        session: Annotated["AsyncSession", Depends(get_async_session)],
) -> AuthUser:
    auth_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid username or password'
    )
    query = await session.execute(
        select(UsersORM).where(
            UsersORM.username == username
        )
    )
    db_user = query.scalars().first()

    if not db_user or not verify_password(password, db_user.password):
        raise auth_exception

    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User inactive'
        )

    return AuthUser(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
    )


async def last_login(
        user: AuthUser,
        session: "AsyncSession",
) -> UsersORM:
    query = await session.execute(
        select(UsersORM).where(
            UsersORM.username == user.username
        )
    )
    user_db = query.scalars().first()

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user_db.last_login = func.datetime.now(UTC)
    session.add(user_db)
    await session.commit()
    await session.refresh(user_db)
    return user_db
