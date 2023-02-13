from pydantic import BaseModel, EmailStr, Field


class ItemSchema(BaseModel):
    id: None | int
    nome_item: str = Field(...)
    num_item: int = Field(...)
    
    class Config:
        orm_mode = True
        
class ItemSchemaUpdate(BaseModel):
    nome_item: str = Field(...)
    num_item: int = Field(...)

