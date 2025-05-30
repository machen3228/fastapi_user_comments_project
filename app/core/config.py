from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str = 'Comments service application'
    description: str = 'Service description'
    database_url: str
    secret: str
    jwt_algorithm: str = "HS256"
    access_token_expiration_seconds: int = 60 * 15

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
