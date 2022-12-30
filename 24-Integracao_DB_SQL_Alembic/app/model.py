from sqlalchemy import Column, String, Integer, Boolean

from app.database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    nome = Column(String)
    sobrenome = Column(String)
    idade = Column(Integer)
    email = Column(String)
    ativo = Column(Boolean)
    cpf = Column(Integer)
    sexo = Column(String)
