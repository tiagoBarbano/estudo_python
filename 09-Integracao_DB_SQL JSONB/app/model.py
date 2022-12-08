from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.dialects.postgresql import JSONB
from app.database import Base


class UserModel(Base):
    __tablename__ = "apolice"

    id = Column(Integer, autoincrement=True, primary_key=True, index=True)
    create_time = Column(Date)
    detalhe = Column(JSONB)
    

