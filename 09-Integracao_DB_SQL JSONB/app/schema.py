from pydantic import BaseModel, Field
from typing import Dict
from datetime import date


class ApoliceSchema(BaseModel):
    id: None | int
    create_time: date = Field(...)
    detalhe: list[Dict]
    
    class Config:
        orm_mode = True
        
class ApoliceSchemaUpdate(BaseModel):
    create_time: date = Field(...)
    detalhe: Dict = Field(...)

