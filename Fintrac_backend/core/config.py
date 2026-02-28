from pathlib import Path
from typing import ClassVar
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the directory where this config file is located
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Database Configuration
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:dev_password@0.0.0.0:5434/daily_tracker"
    )

    # Security Configuration
    JWT_SECRET: str = "9af91824eb3385305e0f89e2c4e259991a5f900eafa8a4ab6f992383f70dd712"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: ClassVar[int] = 24
    JWT_EXPIRY_MINUTES: ClassVar[int] = 10

    # Application Configuration
    APP_NAME: str = "Fintrac API"
    ENVIRONMENT: str = "development"
    LOG_LEVEL: str = "debug"

    # Redis Configuration
    REDIS_URL: str = "redis://redis:6379/0"

    # PostgreSQL Configuration (for Docker)
    POSTGRES_DB: str = "daily_tracker"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # Ignore extra fields from .env
    )


# Global settings instance
settings = Settings()
