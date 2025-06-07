from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from sqlalchemy import select

from app.core.security import get_password_hash
from app.models import UsersORM
from app.schemas.auth import AuthUser
from app.schemas.user import UserCreate, UserUpdate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(
        user_in: UserCreate,
        session: "AsyncSession",
) -> UsersORM:
    hashed_password = get_password_hash(user_in.password)
    new_user = UsersORM(
        email=user_in.email,
        password=hashed_password,
        username=user_in.username,
        birthday=user_in.birthday
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def update_user(
        user_id: int,
        user_update: UserUpdate,
        current_user: AuthUser,
        session: "AsyncSession",
) -> UsersORM:
    query = await session.execute(select(UsersORM).where(UsersORM.id == user_id))
    user = query.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough authority to commit this action"
        )

    if user_update.email and user_update.email != user.email:
        existing = await session.execute(
            select(UsersORM).where(UsersORM.email == user_update.email))
        if existing.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email already exists"
            )
        user.email = user_update.email

    if user_update.username and user_update.username != user.username:
        existing = await session.execute(
            select(UsersORM).where(UsersORM.username == user_update.username))
        if existing.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This username already exists"
            )
        user.username = user_update.username

    if user_update.password:
        user.password = get_password_hash(user_update.password)

    if user_update.birthday:
        user.birthday = user_update.birthday

    await session.commit()
    await session.refresh(user)

    return user
