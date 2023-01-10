from .schema import UserSchema, UserSchemaUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import *



async def get_users_default():
    return await get_all_users()


async def get_user_data(id: int):
    return  await get_user_by_id(id)
  

async def new_user(user: UserSchema):
    return await add_user(user)


async def update_user_data(id: int, req: UserSchemaUpdate):
    return await update_user(id, req)


async def delete_user_data(id: int):
    return await delete_user(id)