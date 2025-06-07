from typing import List, TYPE_CHECKING

from fastapi import status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from sqlalchemy import select

from app.models import CommentsORM
from app.schemas.auth import AuthUser
from app.schemas.comment import CommentCreate, CommentUpdate
if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


async def create_comment(
        new_comment: CommentCreate,
        author: AuthUser,
        session: "AsyncSession",
) -> CommentsORM:
    new_comment_data = new_comment.dict()
    new_comment_data['author_id'] = author.id
    db_comment = CommentsORM(**new_comment_data)
    session.add(db_comment)
    await session.commit()
    await session.refresh(db_comment)
    return db_comment


async def get_comment_by_id(
        comment_id: int,
        session: "AsyncSession",
) -> CommentsORM | None:
    db_comment = await session.get(CommentsORM, comment_id)
    return db_comment


async def get_comment_by_user(
        author: AuthUser,
        session: "AsyncSession",
) -> List[CommentsORM]:
    query = await session.execute(
        select(CommentsORM).where(
            CommentsORM.author_id == author.id
        )
    )
    result = query.scalars().all()
    return list(result)


async def search_comments_by_keyword(
        keyword: str,
        session: "AsyncSession"
) -> List[CommentsORM]:
    query = select(CommentsORM).where(
        CommentsORM.comment_text.like(f"%{keyword}%")
    )
    result = await session.execute(query)
    comments = result.scalars().all()
    if not comments:
        raise HTTPException(
            status_code=status.HTTP_204_NO_CONTENT,
            detail="Comments not found"
        )
    return list(comments)


async def update_comment(
        db_comment: CommentsORM,
        comment_in: CommentUpdate,
        session: "AsyncSession",
) -> CommentsORM:
    obj_data = jsonable_encoder(db_comment)
    update_data = comment_in.dict(exclude_unset=True)
    db_comment.is_edited = True

    for field in obj_data:
        if field in update_data:
            setattr(db_comment, field, update_data[field])
    session.add(db_comment)
    await session.commit()
    await session.refresh(db_comment)
    return db_comment


async def delete_comment(
        db_comment: CommentsORM,
        session: "AsyncSession",
) -> CommentsORM:
    await session.delete(db_comment)
    await session.commit()
    return db_comment
