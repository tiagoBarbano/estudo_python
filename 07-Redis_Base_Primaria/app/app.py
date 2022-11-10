from typing import Any
from app import service
from fastapi import FastAPI


def create_app():
    app: Any = FastAPI(
        title="Estudo Python",
        description="Cache - Redis base primaria",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(service.router, prefix="/v1/user", tags=["Users"])

    return app
