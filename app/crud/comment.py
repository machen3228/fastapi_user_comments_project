from fastapi.encoders import jsonable_encoder
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.models import Comment, User
from app.schemas.comment import CommentCreate, CommentUpdate


async def create_comment(
        new_comment: CommentCreate,
        author: User,
        session: AsyncSession,
) -> Comment:
    new_comment_data = new_comment.dict()
    new_comment_data['author_id'] = author.id
    db_comment = Comment(**new_comment_data)
    session.add(db_comment)
    await session.commit()
    await session.refresh(db_comment)
    return db_comment


async def get_comment_by_id(
        comment_id: int,
        session: AsyncSession,
) -> Comment:
    db_comment = await session.get(Comment, comment_id)
    return db_comment


async def get_comment_by_user(
        session: AsyncSession,
        author: User
) -> list[Comment]:
    comments = await session.execute(
        select(Comment).where(
            Comment.author_id == author.id
        )
    )
    return comments.scalars().all()


async def search_comments_by_keyword(
    keyword: str,
    session: AsyncSession
) -> list[Comment]:
    comments = (await session.execute(select(Comment))).scalars().all()
    result = [
        c for c in comments
        if keyword.lower() in c.comment_text.lower()
    ]
    return result


async def update_comment(
        db_comment: Comment,
        comment_in: CommentUpdate,
        session: AsyncSession,
) -> Comment:
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
        db_comment: Comment,
        session: AsyncSession,
) -> Comment:
    await session.delete(db_comment)
    await session.commit()
    return db_comment
