from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Text, ForeignKey, Integer
from sqlalchemy.sql import func

from app.core.db import Base


class Comment(Base):
    comment_text = Column(
        Text,
        nullable=False,
        comment="Текст комментария"
    )
    created_at = Column(
        DateTime(timezone=True),
        default=datetime.utcnow,
        nullable=False,
        comment="Дата и время создания комментария"
    )
    updated_at = Column(
        DateTime,
        onupdate=func.now(),
        comment="Дата и время редактирования комментария"
    )
    is_edited = Column(
        Boolean,
        default=False
    )
    author_id = Column(
        Integer,
        ForeignKey('user.id'),
        comment="ID автора комментария"
    )
    user_id = Column(
        Integer,
        nullable=False,
        comment="ID пользователя"
    )
