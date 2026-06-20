from pydantic import ConfigDict, Field
from pydantic_settings import BaseSettings
from pathlib import Path

from src.utils.logging import logger


class ModelConfig:

    model_config = ConfigDict(
        extra="ignore",
        env_file=".env",
        env_file_encoding="utf-8",
    )


class DbSettings(BaseSettings, ModelConfig):

    DB_HOST: str | None = None
    DB_PORT: int | None = None
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    DATABASE_URL: str | None = None  # якщо задано напряму

    @property
    def DB_URL(self) -> str:

        # 1. якщо є готовий URL → використовуємо його
        if self.DATABASE_URL:
            return self.DATABASE_URL

        # 2. fallback → будуємо з частин
        return (
            f"postgresql+asyncpg://{self.DB_USER}:"
            f"{self.DB_PASSWORD}@{self.DB_HOST}:"
            f"{self.DB_PORT}/{self.DB_NAME}"
        )

    # @property
    # def DB_URL(self):
    #     if self.DB_PORT:
    #         return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    #     else:
    #         return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}/{self.DB_NAME}"


class Settings(BaseSettings, ModelConfig):
    MODE: str = "DEV"

    db: DbSettings = Field(default_factory=DbSettings)

    BASE_DIR: Path = Path(__file__).parent.parent



settings = Settings()
