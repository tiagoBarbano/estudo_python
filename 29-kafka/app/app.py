from typing import Any
from app.controllers import UserController
from fastapi import FastAPI
from app.repository import startup_db_pool
from app.kafka_connector import getUserKafka

def create_app():
    app: Any = FastAPI(
        title="Estudo Python",
        description="Integracao com DB SQL",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    async def initialize():
        await startup_db_pool()
        #await getUserKafka()
    
    
    app.include_router(UserController.router())
    app.add_event_handler("startup", initialize)
    
    return app
