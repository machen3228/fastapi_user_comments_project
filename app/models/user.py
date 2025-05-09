from sqlalchemy import (
    Column, DateTime, String, Boolean, Float, func
)
from app.core.db import Base


class User(Base):
    '''Модель пользователя'''
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    username = Column(String, unique=True, nullable=False)
    birthdate = Column(DateTime)
    rating = Column(Float, default=0.0)
    registered_at = Column(DateTime, server_default=func.now())
    last_login = Column(DateTime)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
