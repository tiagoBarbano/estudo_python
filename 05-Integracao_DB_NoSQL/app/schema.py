from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field


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


class UserSchema(BaseModel):
    id: PyObjectId | None = Field(default_factory=PyObjectId, alias="_id")
    nome: str = Field(...)
    idade: int = Field(...)
    email: EmailStr = Field(...)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UpdateUserModel(BaseModel):
    nome: str | None
    idade: int | None
    email: EmailStr | None

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
