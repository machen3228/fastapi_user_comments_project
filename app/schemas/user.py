from datetime import date
from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional

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
    'title': 'Дата рождения',
    'description': 'Введите вашу дату рождения (необязательное поле)',
    "example": "1990-01-01"
}


class UserCreate(BaseModel):
    email: EmailStr = Field(**EMAIL_FIELD)
    password: str = Field(**PASSWORD_FIELD)
    username: str = Field(**USERNAME_FIELD)
    birthdate: Optional[date] = Field(**BIRTHDAY_FIELD)

    @classmethod
    def as_form(
            cls,
            email: EmailStr = Form(**EMAIL_FIELD),
            password: str = Form(**PASSWORD_FIELD),
            username: str = Form(**USERNAME_FIELD),
            birthdate: Optional[date] = Form(**BIRTHDAY_FIELD),
    ):
        return cls(
            email=email,
            password=password,
            username=username,
            birthdate=birthdate,
        )


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = Field(None)
    password: Optional[str] = Field(None)
    username: Optional[str] = Field(None)
    birthdate: Optional[date] = Field(None)

    @field_validator("email", mode="before")
    @classmethod
    def validate_email(cls, v: Optional[str]) -> Optional[str]:
        if v == "":
            return None
        return v

    @field_validator('birthdate', mode='before')
    @classmethod
    def validate_birthdate(cls, v: Optional[str]) -> Optional[date]:
        if v == "":
            return None
        if v is None:
            return None
        try:
            return date.fromisoformat(v)
        except ValueError:
            raise ValueError("Дата должна быть в формате YYYY-MM-DD")

    @classmethod
    def as_form(
            cls,
            email: str = Form("", **EMAIL_FIELD),
            password: str = Form("", **PASSWORD_FIELD_UPDATE),
            username: str = Form("", **USERNAME_FIELD_UPDATE),
            birthdate: str = Form("", **BIRTHDAY_FIELD),
    ):
        return cls(
            email=email,
            password=password,
            username=username,
            birthdate=birthdate,
        )


class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    birthdate: Optional[date]
    rating: Optional[int]

    class Config:
        from_attributes = True
