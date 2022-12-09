from pydantic import BaseModel, Field
from typing import Dict
from datetime import date



class ApoliceSchema(BaseModel):
    id: None | int
    create_time: date = Field(...)
    detalhe: list[dict]
    class Config:
        orm_mode = True
        
class ApoliceSchemaUpdate(BaseModel):
    create_time: date = Field(...)
    detalhe: Dict = Field(...)

class Detalhe(BaseModel):
    name: str
    price: float
    productid: int

class ApoliceRequest(BaseModel):
    id: None | int
    create_time: date = Field(...)
    detalhe: list[Detalhe]    