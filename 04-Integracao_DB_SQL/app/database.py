from typing import AsyncGenerator

from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import get_settings


settings = get_settings()

engine = create_async_engine(settings.asyncpg_url, future=True, echo=False, )
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()

# Dependency
async def get_db() -> AsyncGenerator:
    async with async_session() as session:
        try:
            yield session
        except SQLAlchemyError as sql_ex:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(sql_ex))
        except HTTPException as http_ex:
            await session.rollback()
            raise HTTPException(status_code=http_ex.status_code, detail=str(http_ex.detail))
        finally:
            await session.close()