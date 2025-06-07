from typing import TYPE_CHECKING

from fastapi import HTTPException, status

from sqlalchemy import select, or_

from app.crud.comment import get_comment_by_id
from app.models import CommentsORM, UsersORM
from app.schemas.auth import AuthUser
from app.schemas.user import UserCreate

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def check_comment_before_edit(
        comment_id: int,
        author: AuthUser,
        session: "AsyncSession",
) -> CommentsORM:
    comment = await get_comment_by_id(
        comment_id, session
    )
    if comment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='CommentsORM not found'
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
    db_user = await session.get(UsersORM, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='UsersORM not found'
        )
    return db_user


async def validate_user_before_create(
        user_in: UserCreate,
        session: "AsyncSession"
):
    db_user = await session.execute(
        select(UsersORM).where(
            or_(UsersORM.email == user_in.email, UsersORM.username == user_in.username)
        )
    )
    result = db_user.scalars().first()
    if result:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='UsersORM with these username or email already exists'
        )
    return result
