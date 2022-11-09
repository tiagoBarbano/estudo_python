import logging
from fastapi import FastAPI
from aio_pika import connect as pika_connect, IncomingMessage, ExchangeType


logger = logging.getLogger('uvicorn')

async def on_message(message: IncomingMessage):
    async with message.process():
        logger.info("Mensagem lida da Fila %r" % (message.body.decode()))

async def consume(app: FastAPI):
    await app.state.rabbit_queue.consume(on_message)

async def install(app: FastAPI):
    # Perform connection
    connection = await pika_connect("amqp://guest:guest@localhost/")
    app.state.rabbit_connection = connection

    # Creating a channel
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=1)
    app.state.rabbit_channel = channel

    exchange = await channel.declare_exchange("teste", ExchangeType.TOPIC, durable=True)
    app.state.rabbit_exchange = exchange

    queue = await channel.declare_queue(name="teste", durable=True)
    app.state.rabbit_queue = queue

    # Binding the queue to the exchange
    await queue.bind(exchange, routing_key='teste')