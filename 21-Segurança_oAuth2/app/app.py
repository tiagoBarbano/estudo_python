from typing import Any
from fastapi import FastAPI
from app.service import user_service
from app.utils import secutiry


def create_app():
    app: Any = FastAPI(
            title="CONTEUDO MINISTRADO",
            description="BACKEND - CONTEUDO MINISTRADO",
            version="1.0.0",
            openapi_url="/openapi.json",
            docs_url="/docs",
            redoc_url="/redoc"
          )
    
    app.include_router(user_service.router, prefix="/v1/user", tags=["User"])
    app.include_router(secutiry.router, prefix="/v1/security", tags=["Security"])
    
    return app
