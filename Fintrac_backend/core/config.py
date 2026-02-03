from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the directory where this config file is located
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""

    # Database Configuration
    DATABASE_URL: str = (
        "postgresql+asyncpg://postgres:dev_password@127.0.0.1:5434/daily_tracker"
    )

    # Security Configuration
    JWT_SECRET: str = "your_secret_key_change_in_production"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_HOURS: int = 24

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
