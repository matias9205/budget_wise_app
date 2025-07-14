import os
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

if os.getenv("USE_ENV_FILE", "true").lower() == "true":
    load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = Field(default="")
    TEST_DATABASE_URL: str = Field(default="")
    SQLITE_TEST_URL: str = Field(default="")
    SECRET_KEY: str = Field(default="supersecretkey")
    debug: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()