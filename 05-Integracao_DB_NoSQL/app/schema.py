from enum import Enum
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, Json


class PyObjectId(ObjectId):

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

class Tipo_Endereco(str, Enum):
    RESIDENCIAL = 'RESIDENCIAL'
    COMERCIAL = 'COMERCIAL'
    OUTROS = 'OUTROS'
    PESSOAL = 'PESSOAL'

class Tipo_Email(str, Enum):
    COMERCIAL = 'COMERCIAL'
    PESSOAL = 'PESSOAL'
    OUTROS = 'OUTROS'

class Tipo_Telefone(str, Enum):
    CELULAR = 'CELULAR'
    FIXO = 'FIXO'
    RADIO = 'RADIO'

class Endereco(BaseModel):
    id_endereco: int = Field(...)
    logradouro: str = Field(...)
    bairro: str = Field(...)
    numero: int = Field(...)
    complemento: str = Field(...)
    tipo_endereco: Tipo_Endereco = Field(...)
    
class Telefone(BaseModel):
    id_telefone: int = Field(...) 
    numero: str = Field(...)
    tipo_telefone: Tipo_Telefone = Field(...)
    
class Email(BaseModel):
    id_email: int = Field(...)
    email: EmailStr = Field(...)
    tipo_telefone: Tipo_Email = Field(...)    
    
class Detalhe(BaseModel):
    id_produto: int = Field(...)
    nome_produto: str = Field(...)
    price: float = Field(...)
    
class UserSchema(BaseModel):
    id: PyObjectId | None = Field(default_factory=PyObjectId, alias="_id")
    nome: str = Field(...)
    idade: int = Field(...)
    telefone: Json[list[Telefone]]
    email: Json[list[Email]]
    endereco: Json[list[Endereco]]
    detalhe: Json[list[Detalhe]] | None
    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class UpdateUserModel(BaseModel):
    nome: str | None
    idade: int | None
    telefone: Json[list[Telefone]] | None
    email: Json[list[Email]] | None
    endereco: Json[list[Endereco]] | None
    detalhe: Json[list[Detalhe]] | None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
