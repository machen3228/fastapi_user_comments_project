from datetime import date
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Annotated

EMAIL_FIELD = {
    'title': 'E-mail',
    'description': 'Input existing email address',
    "example": "user@example.com"
}
PASSWORD_FIELD = {
    'title': 'Password',
    'description': 'Input safety password not shorter than 6 symbols',
    'min_length': 5,
    'max_length': 20
}
USERNAME_FIELD = {
    'title': 'Username',
    'description': 'Input unique username (4-12 symbols length)',
    'min_length': 4,
    'max_length': 12
}
BIRTHDAY_FIELD = {
    "title": 'Birghtday',
    "description": 'Input birghtday (optional field)',
    "example": "1990-01-01",
}


class UserCreate(BaseModel):
    email: Annotated[EmailStr, Field(**EMAIL_FIELD)]
    password: Annotated[str, Field(**PASSWORD_FIELD)]
    username: Annotated[str, Field(**USERNAME_FIELD)]
    birthday: Annotated[Optional[date], Field(default=None, **BIRTHDAY_FIELD)]


class UserUpdate(BaseModel):
    email: Annotated[Optional[EmailStr], Field(default=None, **EMAIL_FIELD)]
    password: Annotated[Optional[str], Field(default=None, **PASSWORD_FIELD)]
    username: Annotated[Optional[str], Field(default=None, **USERNAME_FIELD)]
    birthday: Annotated[Optional[date], Field(default=None, **BIRTHDAY_FIELD)]


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    birthday: Optional[date]
    rating: Optional[int]

    class Config:
        from_attributes = True
