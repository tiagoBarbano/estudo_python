from pydantic import BaseSettings
from functools import lru_cache
from fastapi_cache import FastAPICache
from fastapi import Request, Response


class Settings(BaseSettings):
    asyncpg_url: str
    redis_url: str
    pass_redis: str
    port_redis: int
    host_redis: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()
