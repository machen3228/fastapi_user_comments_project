from datetime import datetime, UTC

from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base


class UsersORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )
    username: Mapped[str] = mapped_column(
        unique=True,
    )
    email: Mapped[str] = mapped_column(
        unique=True,
    )
    password: Mapped[str]
    birthday: Mapped[datetime | None]
    rating: Mapped[float] = mapped_column(
        default=0.0,
    )
    registered_at: Mapped[datetime] = mapped_column(
        default=datetime.now(UTC),
    )
    last_login: Mapped[datetime] = mapped_column(
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
    )
    is_superuser: Mapped[bool] = mapped_column(
        default=False,
    )
