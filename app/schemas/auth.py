from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr


class PayloadSchema(BaseModel):
    model_config = ConfigDict(strict=True)

    type: str
    sub: str
    iat: int
    jti: str
    username: Optional[str] = None
    email: Optional[str] = None


class AuthUser(BaseModel):
    id: int
    username: str
    email: Optional[EmailStr] = None
    rating: Optional[int] = None
    is_active: Optional[bool] = None

    class Config:
        from_attributes = True


class TokenInfo(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = 'Bearer'
