from datetime import date
from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional, Annotated, Union

from fastapi import Form

EMAIL_FIELD = {
    'title': 'E-mail',
    'description': 'Введите существующий e-mail адрес',
    "example": "user@example.com"
}
PASSWORD_FIELD = {
    'title': 'Пароль',
    'description': 'Введите безопасный пароль не менее 6 символов',
    'min_length': 5,
    'max_length': 20
}
PASSWORD_FIELD_UPDATE = {
    'title': 'Пароль',
    'description': 'Введите безопасный пароль не менее 6 символов',
}
USERNAME_FIELD = {
    'title': 'Имя пользователя',
    'description': 'Придумайте имя пользователя (от 4 до 12 символов)',
    'min_length': 4,
    'max_length': 12
}
USERNAME_FIELD_UPDATE = {
    'title': 'Имя пользователя',
    'description': 'Введите имя пользователя (от 4 до 12 символов)',
}
BIRTHDAY_FIELD = {
    "title": 'Дата рождения',
    "description": 'Введите вашу дату рождения (необязательное поле)',
    "example": "1990-01-01",
    "default": None
}


class UserCreate(BaseModel):
    email: Annotated[EmailStr, Field(**EMAIL_FIELD)]
    password: Annotated[str, Field(**PASSWORD_FIELD)]
    username: Annotated[str, Field(**USERNAME_FIELD)]
    birthdate: Annotated[Optional[date], Field(**BIRTHDAY_FIELD)] = None


class UserUpdate(BaseModel):
    email: Annotated[Optional[EmailStr], Field(**EMAIL_FIELD)] = None
    password: Annotated[Optional[str], Field(**PASSWORD_FIELD)] = None
    username: Annotated[Optional[str], Field(**USERNAME_FIELD)] = None
    birthdate: Annotated[Optional[date], Field(BIRTHDAY_FIELD)] = None


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    birthdate: Optional[date]
    rating: Optional[int]

    class Config:
        from_attributes = True
