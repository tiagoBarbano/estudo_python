from aredis_om import get_redis_connection, JsonModel, Field
from fastapi import APIRouter
from app.config import get_settings

settings = get_settings()

router = APIRouter()

redis = get_redis_connection(host=settings.host_redis,
                             port=settings.port_redis,
                             password=settings.pass_redis,
                             decode_responses=True)


class Orquestrador(JsonModel):
    nome: str = Field(...)
    idade: int = Field(...)
    email: str = Field(...)

    class Meta:
        database = redis