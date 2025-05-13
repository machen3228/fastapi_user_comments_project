from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/auth/login',
    description='Войдите, используя свои имя пользователя и пароль',
    scheme_name='Войти'
)


def get_password_hash(password: str) -> str:
    """Функция хеширования пароля"""
    return pwd_context.hash(password)
