from typing import Any
from fastapi import FastAPI
from app.service import user_service
from app.utils import secutiry
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.utils.config import get_settings

settings = get_settings()


def create_app():
    app: Any = FastAPI(
            title="CONTEUDO MINISTRADO",
            description="BACKEND - CONTEUDO MINISTRADO",
            version="1.0.0",
            openapi_url="/openapi.json",
            docs_url="/docs",
            redoc_url="/redoc"
          )
    
    async def on_startup() -> None:
        redis = aioredis.from_url(settings.redis_url,
                                  encoding="utf-8",
                                  decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix="oauth")
    
    
    app.add_event_handler("startup", on_startup)
    app.include_router(user_service.router, prefix="/v1/user", tags=["User"])
    app.include_router(secutiry.router, prefix="/v1/security", tags=["Security"])
    
    return app
