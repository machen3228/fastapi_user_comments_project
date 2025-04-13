from fastapi import APIRouter

from app.api.endpoints import comment_router, user_router

main_router = APIRouter()
main_router.include_router(
    comment_router, prefix='/comments', tags=['Comments']
    )
main_router.include_router(user_router)
