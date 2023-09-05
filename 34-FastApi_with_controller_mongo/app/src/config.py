
from pydantic import BaseSettings, RedisDsn, MongoDsn
from functools import lru_cache
from fastapi_cache import FastAPICache
from fastapi import Request, Response



class Settings(BaseSettings):
    mongo_uri: MongoDsn
    redis_url: RedisDsn
   
    class Config:
        env_file = ".env"
       
@lru_cache()        
def get_settings():
    return Settings()


def key_all_users(
    func,
    namespace: str | None = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    prefix = FastAPICache.get_prefix()
    cache_key = f"{prefix}:{namespace}:{func.__module__}:{func.__name__}"
    return cache_key

def key_user_by_id(
    func,
    namespace: str | None = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    prefix = FastAPICache.get_prefix()
    var = kwargs.get('kwargs')
    cache_key = f"{prefix}:{namespace}:{var.get('id')}"
    return cache_key