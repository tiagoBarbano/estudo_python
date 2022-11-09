from typing import Any
from fastapi import FastAPI
import service, consumer_rabbitmq, asyncio


def create_app():
    app: Any = FastAPI(
            title="Estudo Python",
            description="Mensageria - RabbitMQ",
            version="1.0.0",
            openapi_url="/openapi.json",
            docs_url="/docs",
            redoc_url="/redoc"
          )

    #@app.on_event("startup")
    async def rabbitmq_startup():
        await consumer_rabbitmq.install(app)
        asyncio.create_task(consumer_rabbitmq.consume(app))
        print('RabbitMQ Habilitado - Escutando Fila')

    app.include_router(service.router, prefix="/v1", tags=["teste"])
    app.add_event_handler("startup", rabbitmq_startup)

    return app
    