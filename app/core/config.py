from os import getenv
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    ROOMS_CSV_PATH: str

    ADMIN_EMAIL: str
    ADMIN_PASSWORD: str


    model_config = SettingsConfigDict(
        env_file=getenv("ENV_FILE", ".env"),
        extra="ignore",
    )

settings = Settings()
