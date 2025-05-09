from datetime import datetime, timezone
from uuid import uuid4

from app.core.auth.backend import auth_backend
from app.core.auth.dependencies import (
    TOKEN_TYPE_FIELD,
    ACCESS_TOKEN_TYPE,
    REFRESH_TOKEN_TYPE,
)
from app.schemas.auth import AuthUser


async def create_jwt(token_type: str, jwt_payload: dict) -> str:
    payload = {TOKEN_TYPE_FIELD: token_type}
    payload.update(jwt_payload)
    if token_type == REFRESH_TOKEN_TYPE:
        refresh_exp_time = 60 * 60 * 24 * 30  # 30 days
        return await auth_backend.create_token(
            payload,
            expiration=refresh_exp_time
        )
    return await auth_backend.create_token(payload)


async def create_access_token(user: AuthUser) -> str:
    payload = {
        'sub': str(user.id),
        'username': user.username,
        'email': user.email if user.email else None,
        'iat': int(datetime.now(timezone.utc).timestamp()),
        "jti": str(uuid4())
    }
    return await create_jwt(
        token_type=ACCESS_TOKEN_TYPE,
        jwt_payload=payload
    )


async def create_refresh_token(user: AuthUser) -> str:
    payload = {
        'sub': str(user.id),
        'iat': int(datetime.now(timezone.utc).timestamp()),
        "jti": str(uuid4())
    }
    return await create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        jwt_payload=payload
    )
