from typing import Any

from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.src.controllers import UserController
from fastapi import FastAPI
from .src.config import get_settings

settings = get_settings()

def create_app():
    app: Any = FastAPI(
        title="Estudo Python",
        description="Integracao com DB SQL",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    async def on_startup() -> None:
        redis = aioredis.from_url(settings.redis_url,
                                  encoding="utf-8",
                                  decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    app.include_router(UserController.router())
    app.add_event_handler("startup", on_startup)
    
    return app
