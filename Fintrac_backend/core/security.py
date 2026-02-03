from datetime import timedelta
import datetime
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings


# password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
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
    # Encode the JWT token
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt
