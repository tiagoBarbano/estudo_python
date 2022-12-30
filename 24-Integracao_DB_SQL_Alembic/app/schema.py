from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    id: None | int
    nome: str = Field(...)
    sobrenome: str = Field(...)
    idade: int = Field(...)
    email: EmailStr = Field(...)
    ativo: bool = Field(...)
    
    
    class Config:
        orm_mode = True
        
class UserSchemaUpdate(BaseModel):
    nome: str = Field(...)
    idade: int = Field(...)
    email: EmailStr = Field(...)        

