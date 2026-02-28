from datetime import timedelta
import datetime
from typing import Optional
import bcrypt
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer

from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/user/login")


# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    pwd_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(pwd_bytes, salt).decode("utf-8")
    return password_hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(
    data: dict, expires_delta: Optional[timedelta] = None, is_refresh: bool = False
) -> str:
    """Create JWT access token"""
    to_encode = data.copy()  # to avoid mutating the original dict
    if expires_delta:
        # Calculate the expiration time
        expire = datetime.datetime.now() + expires_delta
    else:
        # Default expiration time
        expire = datetime.datetime.now() + timedelta(hours=settings.JWT_EXPIRY_HOURS)

    # Add expiration time to the payload
    to_encode.update({"exp": expire})
    if is_refresh:
        to_encode.update({"refresh": True})
    # Encode the JWT token
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
