from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from sqlalchemy import select, or_

from app.crud.comment import get_comment_by_id
from app.models import Comment, User
from app.schemas.auth import AuthUser
from app.schemas.user import UserCreate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def check_comment_before_edit(
        comment_id: int,
        session: "AsyncSession",
        author: AuthUser
) -> Comment:
    comment = await get_comment_by_id(
        comment_id, session
    )
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Comment not found'
        )
    if comment.author_id != author.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not enough authority. You can edit your comments only'
        )
    return comment


async def check_user_exists(
        user_id: int,
        session: "AsyncSession",
):
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User not found'
        )
    return db_user


async def validate_user_before_create(
        user_in: UserCreate,
        session: "AsyncSession"
):
    db_user = await session.execute(
        select(User).where(
            or_(User.email == user_in.email, User.username == user_in.username)
        )
    )
    result = db_user.scalars().first()
    if result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='User with these username or email already exists'
        )
    return result
