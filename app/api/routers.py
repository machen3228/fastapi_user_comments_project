from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from app.api.endpoints import auth_router, comment_router, user_router

http_bearer = HTTPBearer(auto_error=False)

main_router = APIRouter()

main_router.include_router(
    comment_router, prefix='/comments', tags=['Comments']
)

main_router.include_router(
    user_router,
    prefix='/users',
    tags=['Users']
)

main_router.include_router(
    auth_router,
    prefix='/auth',
    tags=['Auth'],
    dependencies=[Depends(http_bearer)]
)
