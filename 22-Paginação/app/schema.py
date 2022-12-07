from pydantic import BaseModel, EmailStr, Field
    
class UserSchema(BaseModel):
    id: None | int
    nome: str = Field(...)
    idade: int = Field(...)
    email: EmailStr = Field(...)
   
    class Config:
        orm_mode = True

class ResponseSchema(BaseModel):
    user = []
    limit: int
    skip: int
    total: int
        
class UserSchemaUpdate(BaseModel):
    nome: str = Field(...)
    idade: int = Field(...)
    email: EmailStr = Field(...)        

