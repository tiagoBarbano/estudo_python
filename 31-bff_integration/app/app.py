from typing import Any
from app.controllers import BffController
from fastapi import FastAPI


def create_app():
    app: Any = FastAPI(
        title="Estudo Python",
        description="BFF Integracao com oAuth",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(BffController.router())
    
    return app
