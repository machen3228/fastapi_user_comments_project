from typing import Annotated, List, TYPE_CHECKING

from fastapi import (
    APIRouter, Depends, Form,
    HTTPException, Path, status, Query
)

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

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post(
    '/',
    response_model=CommentDB,
    summary="Comment creation"
)
async def create_new_comment(
        comment: Annotated[CommentCreate, Form()],
        author: Annotated[AuthUser, Depends(get_current_auth_user)],
        session: Annotated["AsyncSession", Depends(get_async_session)],
):
    """For authorised users only"""
    await check_user_exists(comment.user_id, session)
    new_comment = await create_comment(comment, author, session)
    return new_comment


@router.get(
    '/my_comments',
    response_model=List[CommentDB],
    summary="All your comments receive"
)
async def get_my_comments(
        author: Annotated[AuthUser, Depends(get_current_auth_user)],
        session: Annotated["AsyncSession", Depends(get_async_session)],
):
    """For authorised users only"""
    comments = await get_comment_by_user(
        session=session, author=author
    )
    if not comments:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Comments are not found"
        )
    return comments


@router.get(
    '/{comment_id}',
    response_model=CommentResponse,
    summary="Receive comment by id"
)
async def get_comment(
        comment_id: Annotated[
            int,
            Path(...,
                 title="Comment id",
                 description="Comment id to be returned")
        ],
        author: Annotated[AuthUser, Depends(get_current_auth_user)],
        session: Annotated["AsyncSession", Depends(get_async_session)],
):
    """For comment author only"""
    comment = await check_comment_before_edit(
        comment_id, session, author
    )
    return comment


@router.get(
    '/search/',
    response_model=List[CommentDB],
    summary="Receive comments by substring"
)
async def search_comments(
        keyword: Annotated[
            str,
            Query(...,
                  description="Keyword for searching"
                  )
        ],
        session: Annotated["AsyncSession", Depends(get_async_session)]
):
    """For all users"""
    comments = await search_comments_by_keyword(keyword, session)
    return comments


@router.patch(
    '/{comment_id}',
    response_model=CommentResponse,
    summary="Comment update"
)
async def partially_update_comment(
        comment_id: Annotated[
            int,
            Path(...,
                 title="Comment id",
                 description="Comment id, to be updated"
                 )
        ],
        obj_in: Annotated[CommentUpdate, Form()],
        author: Annotated[AuthUser, Depends(get_current_auth_user)],
        session: Annotated["AsyncSession", Depends(get_async_session)],
):
    """For comment author only"""
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
    summary='Comment removal'
)
async def remove_comment(
        comment_id: Annotated[
            int,
            Path(...,
                 title="Comment id",
                 description="Comment id, to be removed"
                 )
        ],
        author: Annotated[AuthUser, Depends(get_current_auth_user)],
        session: Annotated["AsyncSession", Depends(get_async_session)],
):
    """For comment author only"""
    comment = await check_comment_before_edit(
        comment_id, session, author
    )
    comment = await delete_comment(
        comment, session
    )
    return comment
