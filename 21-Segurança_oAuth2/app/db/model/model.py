from sqlalchemy import Column, String, Integer, DateTime, Boolean
from app.utils.database import Base

    
class UserModel(Base):
    __tablename__ = "user"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)    
    email = Column(String)
    full_name = Column(String)
    disabled = Column(Boolean)    
    id_cadastro = Column(Integer)
    data_criacao = Column(DateTime)
    
