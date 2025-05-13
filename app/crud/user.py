from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import get_password_hash
from app.models import User
from app.schemas.auth import AuthUser
from app.schemas.user import UserCreate, UserUpdate


async def create_user(
        user_in: UserCreate,
        session: AsyncSession,
) -> User:
    """Фунция создания пользователя"""
    hashed_password = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        password=hashed_password,
        username=user_in.username,
        birthdate=user_in.birthdate
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    return new_user


async def update_user(
        user_id: int,
        user_update: UserUpdate,
        session: AsyncSession,
        current_user: AuthUser,
) -> User:
    """Фунция обновления пользователя"""
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )

    if user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав для редактирования этого пользователя"
        )

    if user_update.email and user_update.email != user.email:
        existing = await session.execute(
            select(User).where(User.email == user_update.email))
        if existing.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким email уже существует"
            )
        user.email = user_update.email

    if user_update.username and user_update.username != user.username:
        existing = await session.execute(
            select(User).where(User.username == user_update.username))
        if existing.scalars().first():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким username уже существует"
            )
        user.username = user_update.username

    if user_update.password:
        user.password = get_password_hash(user_update.password)

    if user_update.birthdate:
        user.birthdate = user_update.birthdate

    await session.commit()
    await session.refresh(user)

    return user
