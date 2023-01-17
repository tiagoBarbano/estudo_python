from typing import Any
from app.api.controllers import UserController
from fastapi import FastAPI
from app.api.repository import startup

def create_app():
    app: Any = FastAPI(
        title="Estudo Python",
        description="Integracao com DB SQL",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(UserController.router())
    app.add_event_handler("startup", startup)
    
    return app
