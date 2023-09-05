from .repository import *



async def get_users_default():
    return await get_all_users()


async def new_user(user: UserSchema):
    return await add_user(user)


async def get_user_data(id: int):
    return  await get_user_by_id(id) 


# async def update_user_data(id: int, req: UserSchemaUpdate, db: AsyncSession):
#     return await update_user(db, id, req)


# async def delete_user_data(id: int, db: AsyncSession):
#     return await delete_user(db, id)