from sqlalchemy import Column, String, Integer

from .database import Base


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    nome_item = Column(String)
    num_item = Column(Integer)
