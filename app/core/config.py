from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

env_path = Path(__file__).parent.parent.parent / ".env"


class Settings(BaseSettings):
    app_title: str = 'Comments service application'
    description: str = 'Service description'
    database_url: str
    secret: str
    jwt_algorithm: str = "HS256"
    access_token_expiration_seconds: int = 60 * 15

    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding='utf-8'
    )

settings = Settings()
