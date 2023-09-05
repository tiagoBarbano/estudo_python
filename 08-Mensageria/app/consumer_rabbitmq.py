import logging
from fastapi import FastAPI
from aio_pika import connect_robust as pika_connect, IncomingMessage, ExchangeType
import aio_pika

logger = logging.getLogger('uvicorn')

async def on_message(message: IncomingMessage):
    async with message.process():
        logger.info("Mensagem lida da Fila %r" % (message.body.decode()))

async def consume(queue):
    await queue.consume(on_message)   

async def install():
    # Perform connection
    connection = await pika_connect("amqp://guest:guest@localhost:5672/teste")

    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)

    exchange = await channel.declare_exchange("teste", ExchangeType.TOPIC, durable=True)

    queue = await channel.declare_queue(name="teste", durable=True)

    # Binding the queue to the exchange
    await queue.bind(exchange, routing_key='teste')
    
    return queue
    