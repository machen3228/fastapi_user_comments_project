from datetime import datetime
from pydantic import BaseModel, Field, validator, Extra
from typing import Optional


class CommentBase(BaseModel):

    class Config:
        extra = Extra.forbid


class CommentCreate(CommentBase):
    comment_text: str = Field(
        ...,
        max_length=5000,
        description="Текст комментария"
    )
    user_id: int

    class Config:
        title = 'Класс для создания комментария'
        schema_extra = {
           'example': {
               'comment_text': 'Текст комментария',
               'user_id': 0
           }
        }


class CommentUpdate(CommentBase):
    comment_text: str = Field(
        ...,
        max_length=5000,
        description="Обновленный текст комментария"
    )

    @validator('comment_text')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Комментарий не может быть пустым!')
        return value


class CommentResponse(CommentBase):
    id: int
    user_id: int
    author_id: int
    comment_text: str
    created_at: datetime = Field(..., example='2025-04-12T11:00')
    updated_at: Optional[datetime] = Field(..., example='2025-04-12T12:00')
    is_edited: bool

    class Config:
        orm_mode = True


class CommentDB(CommentBase):
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
