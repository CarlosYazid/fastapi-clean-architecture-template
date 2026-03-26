from functools import lru_cache
from typing import List, Optional
from pathlib import Path

from pydantic import Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict
from passlib.context import CryptContext


class Settings(BaseSettings):
    # Base
    API: str = "/api"
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "fca-api"
    ENV: str = Field(default="dev")

    ENV_DATABASE_MAPPER: dict = {
        "prod": "fca",
        "stage": "stage-fca",
        "dev": "dev-fca",
        "test": "test-fca",
    }

    DB_ENGINE_MAPPER: dict = {
        "postgresql": "postgresql+asyncpg",
        "mysql": "mysql+aiomysql",
    }

    PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent

    model_config = SettingsConfigDict(
        env_file=(str(PROJECT_ROOT / ".env")),
        env_file_encoding="utf-8",
        extra="allow",
    )

    # date
    DATETIME_FORMAT: str = "%Y-%m-%dT%H:%M:%S"
    DATE_FORMAT: str = "%Y-%m-%d"

    # auth
    SECRET_KEY: SecretStr = Field(default=SecretStr("change-me"))
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=(60 * 24 * 30))
    PWD_CONTEXT: CryptContext = CryptContext(schemes=["argon2"], deprecated="auto")
    ALGORITHM: str = "HS256"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = []

    # database
    DB: str = Field(default="postgresql")
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str = Field(default="3306")
    DB_URI_MIGRATIONS: str
    DB_ENGINE: str = DB_ENGINE_MAPPER.get(DB, "postgresql+asyncpg")
    DATABASE_URI: Optional[str] = Field(default=None)

    def model_post_init(self, __context) -> None:

        self.DATABASE_URI = (
            f"{self.DB_ENGINE}://"
            f"{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.ENV_DATABASE_MAPPER[self.ENV]}"
        )

        if "prod" not in self.ENV:
            self.BACKEND_CORS_ORIGINS.append("*")


@lru_cache
def get_settings() -> Settings:
    return Settings()
