from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Optional

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra="ignore",
        env_ignore_empty = True,
    )
    ENVIRONMENT: Literal["local", "production"] = "local"
    JWT_SECRET_KEY: str
    DATABASE_URL: str
    DATABASE_URL_RW: str
    DATABASE_URL_AUTH_RO: str
    DATABASE_URL_MIGRATIONS: str
    OPENAI_API_KEY: str
    SCHEMA_PATH: str

    @property
    def server_host(self) -> str:
        if self.ENVIRONMENT == "local":
            return f"http://{self.DOMAIN}"
        return f"https://{self.DOMAIN}"

settings = Settings()