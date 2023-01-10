from .schema import UserSchema, UserSchemaUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import *



async def get_users_default():
    return await get_all_users()


async def get_user_data(id: int, db: AsyncSession):
    return  await get_user_by_id(db, id)
  

async def new_user(user: UserSchema, db: AsyncSession):
    return await add_user(db, user)


async def update_user_data(id: int, req: UserSchemaUpdate, db: AsyncSession):
    return await update_user(db, id, req)


async def delete_user_data(id: int, db: AsyncSession):
    return await delete_user(db, id)