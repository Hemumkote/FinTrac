from datetime import datetime, time
from enum import Enum
from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.schemas.common import StrongPassword, name_field


class DaysOfWeek(str, Enum):
    """Days of the week for week_starts_on preference."""

    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class Theme(str, Enum):
    """App theme options."""

    SYSTEM = "system"
    LIGHT = "light"
    DARK = "dark"


class TimeTrackingMode(str, Enum):
    """Default time tracking mode options."""

    TIMER = "timer"
    MANUAL = "manual"
    QUICK_LOG = "quick_log"


class DateFormat(str, Enum):
    """Supported date formats."""

    DD_MM_YYYY = "DD/MM/YYYY"
    MM_DD_YYYY = "MM/DD/YYYY"
    YYYY_MM_DD = "YYYY-MM-DD"


class TimeFormat(str, Enum):
    """Supported time formats."""

    TWELVE_HOUR = "12h"
    TWENTY_FOUR_HOUR = "24h"


class UserBase(BaseModel):
    """Base user schema with common fields."""

    email: EmailStr = Field(description="User email address")
    first_name: str = name_field(min_length=1, max_length=100, description="First name")
    last_name: str = name_field(min_length=1, max_length=100, description="Last name")


class UserProfile(BaseModel):
    """User profile information schema."""

    avatar_url: Optional[str] = Field(
        default=None, description="URL of the user's avatar image"
    )

    class Config:
        from_attributes = True


class UserSettings(BaseModel):
    """User settings schema."""

    currency: Optional[str] = Field(
        default="INR", max_length=10, description="Preferred currency (e.g., INR, USD)"
    )
    week_starts_on: Optional[DaysOfWeek] = Field(
        default=DaysOfWeek.MONDAY, description="Preferred starting day of the week"
    )
    date_format: Optional[DateFormat] = Field(
        default=DateFormat.DD_MM_YYYY, description="Preferred date format"
    )
    time_format: Optional[TimeFormat] = Field(
        default=TimeFormat.TWELVE_HOUR, description="Preferred time format (12h/24h)"
    )
    timezone: Optional[str] = Field(
        default="Asia/Kolkata", max_length=50, description="Preferred timezone"
    )
    theme: Optional[Theme] = Field(
        default=Theme.SYSTEM, description="App theme preference"
    )
    default_time_tracking_mode: Optional[TimeTrackingMode] = Field(
        default=TimeTrackingMode.TIMER, description="Default time tracking mode"
    )
    daily_remainder_enabled: Optional[bool] = Field(
        default=False, description="Enable daily tracking remainder"
    )
    daily_remainder_time: Optional[time] = Field(
        default=time(20, 0), description="Time for daily remainder (default 8:00 PM)"
    )
    app_lock_enabled: Optional[bool] = Field(
        default=False, description="Enable app lock for security"
    )

    ## This is needed to allow loading from ORM objects with nested relationships
    class Config:
        from_attributes = True


class UserCreate(UserBase):
    """Schema for creating a new user."""

    password: StrongPassword = Field(
        min_length=8, max_length=128, description="Password for the user account"
    )

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def sanitize_name(cls, value: str) -> str:
        if value is not None and isinstance(value, str):
            return " ".join(value.split()).strip()
        return value


class UserUpdate(BaseModel):
    """Schema for updating user profile."""

    id: int = Field(description="User ID")
    email: EmailStr = Field(description="User email address")
    first_name: Optional[str] = name_field(
        default=None, min_length=1, max_length=100, description="First name"
    )
    last_name: Optional[str] = name_field(
        default=None, min_length=1, max_length=100, description="Last name"
    )

    profile: Optional[UserProfile] = Field(
        default=None, description="User profile information (e.g., avatar URL)"
    )
    settings: Optional[UserSettings] = Field(
        default=None, description="User settings (e.g., preferences)"
    )

    @field_validator("first_name", "last_name", mode="before")
    @classmethod
    def sanitize_name(cls, value: str) -> str:
        if value is not None and isinstance(value, str):
            return " ".join(value.split()).strip()
        return value


class UserResponse(UserBase):
    """Schema for user response (returned from API)."""

    id: int = Field(description="User ID")
    email: EmailStr = Field(description="User email address")
    first_name: str = name_field(min_length=1, max_length=100, description="First name")
    last_name: str = name_field(min_length=1, max_length=100, description="Last name")
    is_active: bool = Field(description="User account status")
    created_at: datetime = Field(description="Creation timestamp")
    updated_at: datetime = Field(description="Last update timestamp")
    profile: Optional[UserProfile] = Field(
        default=None, description="User profile information (e.g., avatar URL)"
    )
    settings: Optional[UserSettings] = Field(
        default=None, description="User settings (e.g., preferences)"
    )

    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    """Schema for user stored in database (includes hashed password)."""

    hashed_password: str = Field(description="Hashed password")


class UserLogin(BaseModel):
    """Schema for the user to login"""

    email: EmailStr = Field(description="User email address")
    password: StrongPassword = Field(
        min_length=8, max_length=128, description="Password for the user account"
    )


class LoginResponse(UserResponse):
    access_token: str = Field(description="JWT access token")
    refresh_token: str = Field(description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
