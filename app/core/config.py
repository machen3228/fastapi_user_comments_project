from typing import Optional

from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    app_title: str = 'Сервис с комментариями'
    description: str = 'Содоржательное описание сервиса'
    database_url: str = 'sqlite+aiosqlite:///./fastapi.db'
    secret: str = 'SECRET'
    first_superuser_email: Optional[EmailStr] = 'admin@admin.com'
    first_superuser_password: Optional[str] = 'admin'

    class Config:
        env_file = '.env'


settings = Settings()
