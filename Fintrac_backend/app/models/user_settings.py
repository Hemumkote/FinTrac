# models/user_settings.py
from datetime import datetime, time
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, String, Boolean, Integer, Time, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.schemas.user import DateFormat, DaysOfWeek, TimeFormat, TimeTrackingMode
from app.db.base import Base

if TYPE_CHECKING:
    from app.models.user import User

class UserSettings(Base):
    """User preferences and settings"""
    __tablename__ = "user_settings"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), unique=True, nullable=False)
    
    # Regional settings
    currency: Mapped[str] = mapped_column(String, nullable=True)
    week_starts_on: Mapped[DaysOfWeek] = mapped_column(Enum(DaysOfWeek), nullable=True)
    date_format: Mapped[DateFormat] = mapped_column(Enum(DateFormat), nullable=True)
    time_format: Mapped[TimeFormat] = mapped_column(Enum(TimeFormat), nullable=True)
    timezone: Mapped[str] = mapped_column(String, nullable=True)
    
    # App settings
    default_time_tracking_mode: Mapped[TimeTrackingMode] = mapped_column(Enum(TimeTrackingMode), nullable=True)
    daily_remainder_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    daily_remainder_time: Mapped[time] = mapped_column(Time, nullable=True)
    app_lock_enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    theme: Mapped[str] = mapped_column(String, nullable=True)
    
    # Backup tracking
    last_backup_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)
    
    # Relationship
    user: Mapped["User"] = relationship(back_populates="settings")