from typing import Any
from app import service
from fastapi import FastAPI
from fastapi_pagination import add_pagination

def create_app():
    app: Any = FastAPI(
        title="Estudo Python",
        description="Integracao com DB SQL",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.include_router(service.router, prefix="/v1/user", tags=["Users"])
    
    add_pagination(app)
    
    return app
