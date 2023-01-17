import asyncio
from typing import Any
from fastapi import FastAPI
from . import hello, consumer_rabbitmq, service


def create_app():
    app: Any = FastAPI(
            title="Estudo Python",
            description="Mensageria - RabbitMQ",
            version="1.0.0",
            openapi_url="/openapi.json",
            docs_url="/docs",
            redoc_url="/redoc"
          )

    async def rabbitmq_startup():
        await consumer_rabbitmq.install(app)
        asyncio.create_task(consumer_rabbitmq.consume(app))
        print('RabbitMQ Habilitado - Escutando Fila')
        await hello.teste()

    app.add_event_handler("startup", rabbitmq_startup)
    app.include_router(service.router, prefix="/v1", tags=["teste"])
    app.include_router(hello.router, prefix="/v1", tags=["teste"])
    
    return app
    