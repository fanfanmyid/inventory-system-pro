from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    PROJECT_NAME: str = "Inventory & Sales API"
    SECRET_KEY: str

    # Pydantic v2 modern configuration
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra="ignore"
    )

settings = Settings()