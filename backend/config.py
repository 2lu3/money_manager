from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    resend_webhook_secret: str | None = None
    resend_api_key: str | None = None

    supabase_user: str | None = None
    supabase_password: str | None = None
    supabase_database: str | None = None
    supabase_host: str | None = None
    supabase_port: int | None = None

@lru_cache
def get_settings() -> Settings:
    return Settings()
