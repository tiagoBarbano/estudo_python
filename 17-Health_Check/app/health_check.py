from fastapi import APIRouter
from app.config import logger


router = APIRouter()

@router.get('/health')
async def health():
    logger.info("OK")
    return "ok"