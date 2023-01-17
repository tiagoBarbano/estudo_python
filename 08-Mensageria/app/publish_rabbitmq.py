import logging
from aio_pika import IncomingMessage, Message, connect as pika_connect
from fastapi import Body, HTTPException


exchange_name = 'teste'
routing_key = 'teste'
logger = logging.getLogger('uvicorn')

async def publish_message(msg: IncomingMessage = Body(...)):
    try:
        connection = await pika_connect("amqps://gjnvdcak:vmtBLN9uBEWxT2DZmexo6CxTiz8pnc-L@jackal.rmq.cloudamqp.com/gjnvdcak")
        async with connection:
            channel = await connection.channel()
            queue = await channel.declare_queue("teste", durable=True)
            await channel.declare_exchange(name=exchange_name, type='topic', durable=True)
            await channel.default_exchange.publish(Message(bytes(msg,'UTF-8')),routing_key=queue.name,)
            logger.info("%r sent to exchange %r with data: %r" % (routing_key, exchange_name, msg))
    except Exception as ex:
        logger.error("Problema para postar a mensagem %r" % (ex))
        raise HTTPException(
            status_code=400,
            detail="Problema para postar a mensagem: " + ex,)        