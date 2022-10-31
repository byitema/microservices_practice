import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    SECRET_KEY: str
    HASH_ALGORITHM: str

    class Config:
        env_file = f'{os.path.dirname(os.path.abspath(__file__))}/../.env'


settings = Settings()
