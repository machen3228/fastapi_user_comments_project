from pydantic import BaseModel

from fastapi_auth_jwt import JWTAuthBackend

from app.core.config import settings
from app.schemas.auth import PayloadSchema


class AuthenticationSettings(BaseModel):
    """JWT authentification settings"""
    secret: str = settings.secret
    jwt_algorithm: str = settings.jwt_algorithm
    expiration_seconds: int = settings.access_token_expiration_seconds


auth_backend = JWTAuthBackend(
    authentication_config=AuthenticationSettings(),
    user_schema=PayloadSchema
)
