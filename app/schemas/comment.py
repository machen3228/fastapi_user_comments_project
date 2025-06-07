from datetime import datetime
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from fastapi import Form

COMMENT_TEXT_META = {
    "description": "CommentsORM text",
    "max_length": 5000
}
USER_ID_META = {
    "description": "The ID of the user who will receive the comment"
}


class CommentCreate(BaseModel):
    comment_text: str = Field(..., **COMMENT_TEXT_META)
    user_id: int = Field(..., **USER_ID_META)


class CommentUpdate(BaseModel):
    comment_text: str = Field(
        ...,
        max_length=5000,
        description="Updated comment text",
        title="Updated comment text",
    )

    @field_validator('comment_text')
    def text_cannot_be_null(cls, value):
        if value is None or value.strip() == '':
            raise ValueError('CommentsORM shall not be empty!')
        return value


class CommentResponse(BaseModel):
    id: int
    user_id: int
    author_id: int
    comment_text: str
    created_at: datetime = Field(..., example='2025-04-12T11:00')
    updated_at: Optional[datetime] = Field(..., example='2025-04-12T12:00')
    is_edited: bool

    class Config:
        from_attributes = True


class CommentDB(BaseModel):
    id: int
    user_id: int
    author_id: int
    comment_text: str = Field(
        ...,
        max_length=5000,
        description="Returned comment text"
    )

    class Config:
        from_attributes = True
