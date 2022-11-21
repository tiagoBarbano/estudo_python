import logging, logging_loki
from pydantic import BaseSettings
from functools import lru_cache
from fastapi_cache import FastAPICache
from fastapi import Request, Response


class Settings(BaseSettings):
    asyncpg_url: str
    redis_url: str

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


def key_user_by_id(
    func,
    namespace: str | None = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    prefix = FastAPICache.get_prefix()
    cache_key = f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{request.path_params}"
    return cache_key


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


def key_add_user(
    func,
    namespace: str | None = "",
    request: Request = None,
    response: Response = None,
    *args,
    **kwargs,
):
    prefix = FastAPICache.get_prefix()
    body = kwargs.get("kwargs")
    cache_key = f"{prefix}:{namespace}:{func.__module__}:{func.__name__}:{body.get('user')}"
    return cache_key

handler = logging_loki.LokiHandler(
    url="http://localhost:3100/loki/api/v1/push", 
    tags={"application": "CRUD USERS"},
    version="1",
)


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s')


logger = logging.getLogger('python-logger')
logger.addHandler(handler)
logger.setLevel(logging.INFO)

