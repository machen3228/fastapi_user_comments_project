from fastapi import Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.db import get_async_session
from app.core.security import pwd_context
from app.models import User
from app.schemas.auth import AuthUser


async def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def validate_auth_user(
    session: AsyncSession = Depends(get_async_session),
    username: str = Form(...),
    password: str = Form(...),
) -> AuthUser:
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

    return AuthUser(
        id=db_user.id,
        username=db_user.username,
        email=db_user.email,
    )
