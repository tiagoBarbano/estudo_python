from app.schema import UserSchema, UserSchemaUpdate
from app.model import UserModel
from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.config import logger
import uuid


async def get_all_users(db: AsyncSession, my_uuid: uuid):
    async with db as session:
        logger.info("Inicio da Query", 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_all_users"},})
        query = select(UserModel)
        users = await session.execute(query)
        users = users.scalars().all()
        await session.close()
        logger.info("Término da Query", 
                    extra={"tags": {"uuid": str(my_uuid),
                                    "service": "get_all_users"},})        
        return users


async def get_user_by_id(db: AsyncSession, id: int) -> dict:
    query = select(UserModel).where(UserModel.id == id)
    users = await db.execute(query)
    user = users.scalar_one_or_none()
    await db.close()
    return user


async def add_user(db: AsyncSession,
                   user_data: UserSchemaUpdate) -> UserSchema:
    new_user = UserModel(nome=user_data.nome,
                         idade=user_data.idade,
                         email=user_data.email)
    db.add(new_user)
    await db.commit()
    return new_user


async def update_user(db: AsyncSession, id: str, data: UserSchemaUpdate):
    query = (update(UserModel).where(UserModel.id == id).values(
        data.dict()).execution_options(synchronize_session="fetch"))
    updated_user = await db.execute(query)

    if updated_user:
        await db.commit()
        return True

    return False


async def delete_user(db: AsyncSession, id: int):
    query = delete(UserModel).where(UserModel.id == id)
    res = await db.execute(query)

    if res.rowcount == 1:
        await db.commit()
        return True

    return False
