from datetime import datetime, UTC

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class CommentsORM(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    comment_text: Mapped[str]
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC),
        onupdate=datetime.now(UTC),
    )
    is_edited: Mapped[bool] = mapped_column(
        default=False,
        onupdate=True
    )
