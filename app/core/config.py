
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[2] / ".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )

    # Application Configuration
    APP_NAME: str = "TaskFlow Pro"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # API Configuration
    API_V1_PREFIX: str = "/api/v1"

    # Database Configuration
    DATABASE_URL: str

    # Authentication Configuration
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


# Central Settings Instance
settings = Settings()
