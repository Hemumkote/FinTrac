from typing import Optional
from click import Option
from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy import Boolean
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.transaction import TransactionCreate
from app.repositories.category_repository import CategoryRepository
from app.schemas.category import CategoryResponse
from app.db.session import get_async_session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from core.config import settings
from core.security import oauth2_scheme


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """
    Dependency to get the current user from a JWT token.

    Decodes the JWT token from the Authorization header, validates it,
    and fetches the corresponding user from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        email = payload.get("sub")
        userId = payload.get("user_id")
        if email is None or userId is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await UserRepository(session).get_user_by_email(email=email)
    if user is None or user.id != userId:
        raise credentials_exception
    return user
