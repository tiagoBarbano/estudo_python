
from pydantic import BaseSettings, PostgresDsn
from functools import lru_cache


class Settings(BaseSettings):
    asyncpg_url: PostgresDsn

    class Config:
        env_file = ".env"
       
@lru_cache()        
def get_settings():
    return Settings()
