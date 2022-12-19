from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    asyncpg_url: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:     
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings():
    return Settings()

