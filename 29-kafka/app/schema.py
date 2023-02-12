import uuid
from pydantic import BaseModel, EmailStr, Field
from pydantic.dataclasses import dataclass


class UserSchema(BaseModel):
    id: None | int
    nome_item: str = Field(...)
    num_item: int = Field(...)
    myuuid: None | uuid.UUID
    
    class Config:
        orm_mode = True
        
class UserSchemaUpdate(BaseModel):
    nome_item: str = Field(...)
    num_item: int = Field(...)

@dataclass
class UserSchemaKafka:
    id: uuid.UUID = Field(...)
    nome_item: str = Field(...)
    num_item: int = Field(...)