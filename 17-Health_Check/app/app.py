from typing import Any
from app import service, health_check
from fastapi import FastAPI
from redis import asyncio as aioredis, Redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.config import get_settings
from pyctuator.pyctuator import Pyctuator
from pyctuator.health.redis_health_provider import RedisHealthProvider
from pyctuator.health.db_health_provider import DbHealthProvider
from app.database import sync_engine
import datetime, psutil


settings = get_settings()


def create_app():
    app: Any = FastAPI(
        title="Estudo Python",
        description="PG - REDIS - Health Check PyCtuator",
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
        

    pyctuator = Pyctuator(
        app,
        app_name=app.title,
        app_description=app.description,
        app_url="http://localhost:8000",
        pyctuator_endpoint_url="http://localhost:8000/pyctuator",
        registration_url="http://localhost:8180/instances"
    )
    
    r = Redis.from_url(settings.redis_url)
    pyctuator.register_health_provider(DbHealthProvider(sync_engine))
    pyctuator.register_health_provider(RedisHealthProvider(r))
    
    # Provide app's build info
    pyctuator.set_build_info(
        name=app.title,
        group=app.description,
        version=app.version,
        time=datetime.datetime.now(),
        artifact="" 
    )
    
    # Provide git commit info
    pyctuator.set_git_info(
        commit="7d4fef3",
        time=datetime.datetime.now(),
        branch="master",
    )

    app.add_event_handler("startup", on_startup)
   
    app.include_router(service.router, prefix="/v1/user", tags=["Users"])
    app.include_router(health_check.router, prefix="", tags=["HealthCheck"])    


    return app
