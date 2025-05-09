from fastapi import APIRouter, Depends, HTTPException, Path, Query

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.endpoints.validators import (
    check_comment_before_edit, check_user_exists
)
from app.core.auth.dependencies import get_current_auth_user
from app.core.db import get_async_session
from app.crud.comment import (
    create_comment, get_comment_by_user,
    update_comment, delete_comment, search_comments_by_keyword
)
from app.schemas.auth import AuthUser
from app.schemas.comment import (
    CommentCreate, CommentDB, CommentUpdate, CommentResponse
)


router = APIRouter()


@router.post(
        '/',
        response_model=CommentDB,
        summary='Создание нового комментария'
)
async def create_new_comment(
        comment: CommentCreate = Depends(CommentCreate.as_form),
        author: AuthUser = Depends(get_current_auth_user),
        session: AsyncSession = Depends(get_async_session),
):
    '''Только для авторизованных пользователей'''
    await check_user_exists(comment.user_id, session)
    new_comment = await create_comment(comment, author, session)
    return new_comment


@router.get(
        '/my_comments',
        response_model=list[CommentDB],
        summary='Получение всех комментариев автора'
)
async def get_my_comments(
    author: AuthUser = Depends(get_current_auth_user),
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
        summary='Получение комментария по id'
)
async def get_comment(
    comment_id: int = Path(
        ...,
        title="ID комментария",
        description="Идентификатор комментария, который нужно вернуть"
        ),
    author: AuthUser = Depends(get_current_auth_user),
    session: AsyncSession = Depends(get_async_session),
):
    '''Только для для авторов комментариев'''
    comment = await check_comment_before_edit(
        comment_id, session, author
    )
    return comment


@router.get(
        '/search/',
        response_model=list[CommentDB],
        summary='Поиск комментариев по ключевым словам'
)
async def search_comments(
    keyword: str = Query(..., description="Ключевое слово для поиска"),
    session: AsyncSession = Depends(get_async_session)
):
    '''Для всех пользователей'''
    comments = await search_comments_by_keyword(keyword, session)
    return comments


@router.patch(
    '/{comment_id}',
    response_model=CommentResponse,
    summary='Редактирование комментария'
)
async def partially_update_comment(
        comment_id: int = Path(
        ...,
        title="ID комментария",
        description="Идентификатор комментария, который нужно отредактировать"
        ),
        obj_in: CommentUpdate = Depends(CommentUpdate.as_form),
        author: AuthUser = Depends(get_current_auth_user),
        session: AsyncSession = Depends(get_async_session),
):
    '''Только для для авторов комментариев'''
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
        comment_id: int = Path(
        ...,
        title="ID комментария",
        description="Идентификатор комментария, который нужно удалить"
        ),
        author: AuthUser = Depends(get_current_auth_user),
        session: AsyncSession = Depends(get_async_session),
):
    '''Только для для авторов комментариев'''
    comment = await check_comment_before_edit(
        comment_id, session, author
    )
    comment = await delete_comment(
        comment, session
    )
    return comment
