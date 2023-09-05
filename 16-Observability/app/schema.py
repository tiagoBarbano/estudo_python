from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    id: None | int
    nome_item: str = Field(...)
    num_item: int = Field(...)
    
    class Config:
        orm_mode = True
        
class UserSchemaUpdate(BaseModel):
    nome_item: str = Field(...)
    num_item: int = Field(...)    

