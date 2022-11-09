import logging
from fastapi import APIRouter
from publish_rabbitmq import publish_message


router = APIRouter()
logger = logging.getLogger('uvicorn')

@router.get("/teste", status_code=200)
async def teste():
    message = "{'TESTE':'TESTE3'}"
    logger.info("Mensagem Postada %r" % (message))
    await publish_message(message)
    