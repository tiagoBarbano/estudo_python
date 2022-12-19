import datetime
from pydantic import BaseModel

       
class User(BaseModel):
    id: int | None
    username: str
    password: str | None = None
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None
    id_cadastro: int | None
    data_criacao: datetime.date | None
    
    class Config:
        orm_mode = True    
        

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None
    scopes: list[str] = []


class UserInDB(User):
    hashed_password: str