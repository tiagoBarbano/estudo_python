from typing import Any
from app import service
from fastapi import FastAPI, Request
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from app.config import get_settings, logger
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry import trace
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor, Span
from opentelemetry.instrumentation.logging import LoggingInstrumentor
#from opentelemetry.instrumentation.aio_pika import AioPikaInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.instrumentation.aiohttp_client import AioHttpClientInstrumentor
from pyctuator.pyctuator import Pyctuator
from app.database import engine
import time

settings = get_settings()


def create_app():
    app: Any = FastAPI(
        title="Estudo Python",
        description="Cache - Redis",
        version="1.0.0",
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    def server_request_hook(span: Span, scope: dict):
        if span and span.is_recording():
            span.set_attribute("Dados Scope 1", str(scope))

    def client_request_hook(span: Span, scope: dict):
        if span and span.is_recording():
            span.set_attribute("Dados Scope 2", str(scope))

    def client_response_hook(span: Span, message: dict):
        if span and span.is_recording():
            span.set_attribute("Dados Message", str(message))

    resource = Resource.create(attributes={"service.name": settings.app_name})
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)
    tracer.add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.host_jaeger,
                agent_port=settings.port_jaeger,
            )))

    LoggingInstrumentor().instrument(set_logging_format=True)
    RedisInstrumentor().instrument()
    #AioPikaInstrumentor().instrument()
    SQLAlchemyInstrumentor().instrument(engine=engine.sync_engine)
    AioHttpClientInstrumentor().instrument()
    FastAPIInstrumentor.instrument_app(
        app,
        tracer_provider=tracer,
        server_request_hook=server_request_hook,
        client_request_hook=client_request_hook,
        client_response_hook=client_response_hook)

    async def on_startup() -> None:
        redis = aioredis.from_url(settings.redis_url,
                                  encoding="utf-8",
                                  decode_responses=True)
        FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

        Instrumentator().instrument(app).expose(app)

    Pyctuator(app,
              "FastAPI Pyctuator",
              app_url=settings.app_url,
              pyctuator_endpoint_url=settings.pyctuator_endpoint_url,
              registration_url=settings.registration_url)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()

        logger.info("INICIO", 
            extra={"tags": {"start_time": str(start_time),
                            "path": str(request.url)},})

        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        
        logger.info("TÉRMINO", 
            extra={"tags": {"process_time": str(process_time),
                            "path": str(request.url)},})
        
        return response


    app.include_router(service.router, prefix="/v1/user", tags=["Users"])
    app.add_event_handler("startup", on_startup)

    return app
