from typing import Any
from app.src.controllers import UserController
from fastapi import FastAPI


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
    
    return app
