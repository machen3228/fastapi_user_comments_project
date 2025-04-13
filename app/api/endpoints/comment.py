from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_user
from app.crud.comment import (
    create_comment, get_comment_by_user,
    update_comment, delete_comment
)
from app.schemas.comment import (
    CommentCreate, CommentDB, CommentUpdate, CommentResponse
)
from app.models import User
from app.api.endpoints.validators import check_comment_before_edit


router = APIRouter()


@router.post(
        '/',
        response_model=CommentDB,
        summary='Создание нового комментария'
)
async def create_new_comment(
        comment: CommentCreate,
        author: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    '''Только для авторизованных пользователей'''
    new_comment = await create_comment(comment, author, session)
    return new_comment


@router.get(
        '/my_comments',
        response_model=list[CommentDB],
        summary='Получение всех комментариев автора'
)
async def get_my_comments(
    author: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Получает список всех комментариев для текущего пользователя."""
    comments = await get_comment_by_user(
        session=session, author=author
    )
    if not comments:
        raise HTTPException(
            status_code=404,
            detail="Комментарии не найдены"
        )
    return comments


@router.get(
        '/{comment_id}',
        response_model=CommentResponse,
        dependencies=[Depends(current_user)],
        summary='Получение комментария по id'
)
async def get_comment(
    comment_id: int,
    author: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    '''Только для для авторов комментариев и суперпользователей'''
    comment = await check_comment_before_edit(
        comment_id, session, author
    )
    return comment


@router.patch(
    '/{comment_id}',
    response_model=CommentResponse,
    summary='Редактирование комментария'
)
async def partially_update_comment(
        comment_id: int,
        obj_in: CommentUpdate,
        author: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    '''Только для для авторов комментариев и суперпользователей'''
    comment = await check_comment_before_edit(
        comment_id, session, author
    )
    comment = await update_comment(
        comment, obj_in, session
    )
    return comment


@router.delete(
    '/{comment_id}',
    response_model=CommentDB,
    summary='Удаление комментария'
)
async def remove_comment(
        comment_id: int,
        author: User = Depends(current_user),
        session: AsyncSession = Depends(get_async_session),
):
    '''Только для для авторов комментариев и суперпользователей'''
    comment = await check_comment_before_edit(
        comment_id, session, author
    )
    comment = await delete_comment(
        comment, session
    )
    return comment
