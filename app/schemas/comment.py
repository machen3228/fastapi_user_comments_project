from datetime import datetime
from pydantic import BaseModel, Field, validator
from typing import Optional
from fastapi import Form


COMMENT_TEXT_META = {
    "description": "Основной текст, который пользователь отправляет",
    "max_length": 5000
}
USER_ID_META = {
    "description": "Идентификатор пользователя, которому адресован комментарий"
}


class CommentCreate(BaseModel):
    comment_text: str = Field(..., **COMMENT_TEXT_META)
    user_id: int = Field(..., **USER_ID_META)

    @classmethod
    def as_form(
        cls,
        comment_text: str = Form(..., **COMMENT_TEXT_META),
        user_id: int = Form(..., **USER_ID_META)
    ) -> "CommentCreate":
        return cls(comment_text=comment_text, user_id=user_id)


class CommentUpdate(BaseModel):
    comment_text: str = Field(
        ...,
        max_length=5000,
        description="Обновленный текст комментария"
    )

    @validator('comment_text')
    def text_cannot_be_null(cls, value):
        if value is None or value.strip() == '':
            raise ValueError('Комментарий не может быть пустым!')
        return value

    @classmethod
    def as_form(
        cls,
        comment_text: str = Form(
            ...,
            max_length=5000,
            title="Обновленный текст комментария",
            description="Комментарий, который пользователь хочет обновить"
        )
    ) -> "CommentUpdate":
        return cls(comment_text=comment_text)


class CommentResponse(BaseModel):
    id: int
    user_id: int
    author_id: int
    comment_text: str
    created_at: datetime = Field(..., example='2025-04-12T11:00')
    updated_at: Optional[datetime] = Field(..., example='2025-04-12T12:00')
    is_edited: bool

    class Config:
        orm_mode = True


class CommentDB(BaseModel):
    id: int
    user_id: int
    author_id: int
    comment_text: str = Field(
        ...,
        max_length=5000,
        description="Возвращаемый текст комментария"
    )

    class Config:
        orm_mode = True
