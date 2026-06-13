from os import getenv
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    ROOMS_CSV_PATH: str

    model_config = SettingsConfigDict(
        env_file=getenv("ENV_FILE", ".env"),
        # env_file=".env",
        extra="ignore",
    )

settings = Settings()

# from pydantic_settings import BaseSettings
#
#
# class Settings(BaseSettings):
#     DATABASE_URL: str
#
#     JWT_SECRET_KEY: str
#     JWT_ALGORITHM: str
#     ACCESS_TOKEN_EXPIRE_MINUTES: int
#
#     ROOMS_CSV_PATH: str
#
#     class Config:
#         env_file = ".env"
#
#
# settings = Settings()
