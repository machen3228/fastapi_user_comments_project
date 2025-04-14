from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.comment import get_comment_by_id
from app.models import Comment, User


async def check_comment_before_edit(
        comment_id: int,
        session: AsyncSession,
        author: User
) -> Comment:
    comment = await get_comment_by_id(
        comment_id, session
    )
    if comment is None:
        raise HTTPException(
            status_code=404,
            detail='Комментарий не найден!'
        )
    if comment.author_id != author.id and not author.is_superuser:
        raise HTTPException(
            status_code=403,
            detail='Невозможно редактировать или удалить чужуй комментарий!'
        )
    return comment


async def check_user_exists(
        user_id: int,
        session: AsyncSession,
):
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(
            status_code=403,
            detail='Пользователь не найден!'
        )
    return db_user
