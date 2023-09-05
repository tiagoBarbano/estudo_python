from fastapi import FastAPI
from pydantic import BaseModel
from random import randint
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor, Span
import uvicorn
from opentelemetry import trace
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


class Item(BaseModel):
    item_id: int | None = None
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
items_fake = [
            {"item_id": 1,
            "name": "Tiago",
            "description": "Teste",
            "price": 10.5,
            "tax": 1.36
            },
            {"item_id": 2,
            "name": "Tiago",
            "description": "Teste",
            "price": 10.5,
            "tax": 1.36
            }
           ]

app = FastAPI()

def configure_opentelemetry():
    resource = Resource.create(attributes={"service.name": "items"})
    tracer = TracerProvider(resource=resource)
    trace.set_tracer_provider(tracer)
    tracer.add_span_processor(BatchSpanProcessor(JaegerExporter(agent_host_name="localhost",
                                                                agent_port=6831, )))   
    
    return tracer



def server_request_hook(span: Span, scope: dict):
    if span and span.is_recording():
        span.set_attribute("custom_user_attribute_from_request_hook", "some-value")

def client_request_hook(span: Span, scope: dict):
    if span and span.is_recording():
        span.set_attribute("custom_user_attribute_from_client_request_hook", "some-value")

def client_response_hook(span: Span, message: dict):
    if span and span.is_recording():
        span.set_attribute("custom_user_attribute_from_response_hook", "some-value")

instrumentator = Instrumentator().instrument(app)
tracer = configure_opentelemetry()
FastAPIInstrumentor().instrument_app(app=app,
                                     server_request_hook=server_request_hook,
                                     client_request_hook=client_request_hook,
                                     client_response_hook=client_response_hook,
                                     tracer_provider=tracer)
# FastAPIInstrumentor().instrument(server_request_hook=server_request_hook, client_request_hook=client_request_hook, client_response_hook=client_response_hook)

@app.on_event("startup")
async def _startup():
    instrumentator.expose(app)

#Busca um item através do ID
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None, y: str | None = None):
    return {"item_id": item_id, "q": q, "y": y}

#Busca todos os items
@app.get("/items")
async def read_items():
    return items_fake

#Inclui um novo item
@app.post("/item")
async def create_item(item: Item):
    item.item_id = randint(0,90) #Cria um id randomico
    items_fake.append(item)
    return items_fake


if __name__ == '__main__':
    uvicorn.run(app, port=8000, host='0.0.0.0')