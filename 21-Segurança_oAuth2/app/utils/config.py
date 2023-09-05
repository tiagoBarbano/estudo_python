from functools import lru_cache
from pydantic import BaseSettings, RedisDsn, PostgresDsn
from fastapi_cache import FastAPICache
from fastapi import Request, Response


class Settings(BaseSettings):
    asyncpg_url: PostgresDsn
    access_token_expire_minutes: int
    redis_url: RedisDsn

    class Config:     
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache()
def get_settings() -> Settings: 
    return Settings()


def key_user_by_name(
    func,
    namespace: str | None = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    user_name = kwargs["args"][1]
    prefix = FastAPICache.get_prefix()
    cache_key = f"{prefix}:{func.__name__}:{user_name}"
    return cache_key

def key_get_token(
    func,
    namespace: str | None = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    _kwargs = kwargs["kwargs"]
    _form_data = _kwargs["form_data"]
    user = _form_data.username
    prefix = FastAPICache.get_prefix()
    
    cache_key = f"{prefix}:{func.__name__}:{_form_data}"
    return cache_key