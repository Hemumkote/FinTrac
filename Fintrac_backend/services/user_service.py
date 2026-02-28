from datetime import timedelta
import token
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.config import settings
from app.models.user_profile import UserProfile
from app.models.user_settings import UserSettings
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserUpdate
from core.security import create_access_token, hash_password, verify_password
from app.repositories.user_repository import UserRepository


class UserService:
    """Service class for user-related operations."""

    def __init__(self, session: AsyncSession):
        self.repository = UserRepository(session)
        self.session = session

    async def create_user(self, user_data: UserCreate) -> dict:
        """Create a new user"""
        existing_user = await self.repository.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=409, detail="User with this email already exists"
            )

        # hash password

        password_hash = hash_password(user_data.password)

        user = User(
            email=user_data.email,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            hashed_password=password_hash,
            is_active=True,
        )

        user = await self.repository.create_user(user)

        # commit transaction

        await self.session.commit()
        await self.session.refresh(user)  # ensures latest DB values

        # # generate token
        # access_token = create_access_token(data={"sub": user.email, "user_id": user.id})

        return {
            # "access_token": access_token,
            "token_type": "bearer",
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    async def login_user(self, user_login: UserLogin) -> dict:
        """Login a user"""
        user = await self.repository.get_user_by_email(user_login.email)
        if not user or not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Incorrect email or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        # generate token
        access_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=timedelta(minutes=settings.JWT_EXPIRY_MINUTES),
        )

        refresh_token = create_access_token(
            data={"sub": user.email, "user_id": user.id},
            expires_delta=timedelta(days=settings.JWT_EXPIRY_HOURS),
            is_refresh=True,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    async def get_user_by_email(self, user: User) -> dict:
        """Get a user by email"""

        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return {
            "id": user.id,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
        }

    async def update_user_profile(self, user_update: UserUpdate) -> UserUpdate:
        """Update user profile information and preferences"""

        existing_user = await self.repository.get_user_with_relations(user_update.id)

        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")

        # Update user fields (names live on User model)
        if user_update.first_name is not None:
            existing_user.first_name = user_update.first_name
        if user_update.last_name is not None:
            existing_user.last_name = user_update.last_name

        # Update profile (create if doesn't exist)
        if existing_user.profile is None:
            existing_user.profile = UserProfile(user_id=existing_user.id)
        if user_update.profile and user_update.profile.avatar_url is not None:
            existing_user.profile.avatar_url = user_update.profile.avatar_url

        # Update settings (create if doesn't exist)
        if existing_user.settings is None:
            existing_user.settings = UserSettings(user_id=existing_user.id)
        if user_update.settings and user_update.settings.currency is not None:
            existing_user.settings.currency = user_update.settings.currency

        if user_update.settings and user_update.settings.week_starts_on is not None:
            existing_user.settings.week_starts_on = user_update.settings.week_starts_on
        if user_update.settings and user_update.settings.date_format is not None:
            existing_user.settings.date_format = user_update.settings.date_format
        if user_update.settings and user_update.settings.time_format is not None:
            existing_user.settings.time_format = user_update.settings.time_format
        if user_update.settings and user_update.settings.timezone is not None:
            existing_user.settings.timezone = user_update.settings.timezone
        if user_update.settings and user_update.settings.theme is not None:
            existing_user.settings.theme = user_update.settings.theme
        if (
            user_update.settings
            and user_update.settings.default_time_tracking_mode is not None
        ):
            existing_user.settings.default_time_tracking_mode = (
                user_update.settings.default_time_tracking_mode
            )
        if (
            user_update.settings
            and user_update.settings.daily_remainder_enabled is not None
        ):
            existing_user.settings.daily_remainder_enabled = (
                user_update.settings.daily_remainder_enabled
            )
        if (
            user_update.settings
            and user_update.settings.daily_remainder_time is not None
        ):
            existing_user.settings.daily_remainder_time = (
                user_update.settings.daily_remainder_time
            )
        if user_update.settings and user_update.settings.app_lock_enabled is not None:
            existing_user.settings.app_lock_enabled = (
                user_update.settings.app_lock_enabled
            )

        # Commit transactions

        await self.session.commit()
        await self.session.refresh(existing_user)

        return user_update
