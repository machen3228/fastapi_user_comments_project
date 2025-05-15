from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Text, ForeignKey, Integer
from sqlalchemy.sql import func

from app.core.db import Base


class Comment(Base):
    comment_text = Column(
        Text,
        nullable=False,
        comment="Comment text"
    )
    created_at = Column(
        DateTime(timezone=True),
        default=func.now(),
        nullable=False,
        comment="Comment creation date and time"
    )
    updated_at = Column(
        DateTime,
        onupdate=func.now(),
        comment="Comment update date and time"
    )
    is_edited = Column(
        Boolean,
        default=False
    )
    author_id = Column(
        Integer,
        ForeignKey('user.id'),
        comment="Comment author id"
    )
    user_id = Column(
        Integer,
        nullable=False,
        comment="User id"
    )
