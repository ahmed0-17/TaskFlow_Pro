from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

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

    # Environment Configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )


# Central Settings Instance
settings = Settings()
