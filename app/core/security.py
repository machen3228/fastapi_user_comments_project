from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/auth/login',
    description='Log in with your username and password',
    scheme_name='Log in'
)


def get_password_hash(password: str) -> str:
    """Hash password function"""
    return pwd_context.hash(password)


def verify_password(
        to_be_verified_password: str,
        password: str,
) -> bool:
    """Hash password function"""
    return pwd_context.verify(to_be_verified_password, password)
