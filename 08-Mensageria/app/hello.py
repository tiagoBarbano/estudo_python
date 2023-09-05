from fastapi import APIRouter
import requests, asyncio
from requests.auth import HTTPBasicAuth
from fastapi_restful.tasks import repeat_every
from app import consumer_rabbitmq


router = APIRouter()


# @repeat_every(seconds=60)  # 1 hour
@router.get("/hello", status_code=200)
async def teste():
    print("Inicio check")
    
    uri='http://localhost:15672/api/queues/teste/teste'
    resp = requests.get(uri, auth=HTTPBasicAuth('guest','guest'))
    
    print(resp.json())

    queues = resp.json()    
    if resp.status_code != 200 or resp.json() == [] or int(queues["consumers"]) == 0:
        queue = await consumer_rabbitmq.install()
        asyncio.create_task(consumer_rabbitmq.consume(queue))
        print('RabbitMQ Habilitado - Escutando Fila')
    
    return resp.json()

