from app.schema.schema import User
from app.db.model.model import UserModel
from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from fastapi_cache.coder import JsonCoder
from app.utils.config import key_user_by_name
from fastapi.encoders import jsonable_encoder


# Retrieve all users present in the database
async def get_all_users(db: AsyncSession):
    query = select(UserModel)
    users = await db.execute(query)
    users = users.scalars().all()
    return users

# Retrieve a user with a matching ID
async def get_user_by_id(db: AsyncSession, id: int) -> dict:
    query = select(UserModel).where(UserModel.id == id)
    users = await db.execute(query)
    user = users.scalar_one_or_none()
    return user

@cache(expire=60,
       coder=JsonCoder,
       key_builder=key_user_by_name)
async def get_user_by_name(db: AsyncSession, username: str) -> dict:
    q = select(UserModel).where(UserModel.username == username) 
    users = await db.execute(q)
    user = users.scalar_one_or_none()
    return jsonable_encoder(user)

# Add a new user into to the database
async def add_user(db: AsyncSession, new_user: User) -> User:       
    db.add(new_user)
    return new_user


# Update a user with a matching ID
async def update_user(db: AsyncSession, id: str, data: User):
    query = (update(UserModel).where(UserModel.id == id).values(data).execution_options(synchronize_session="fetch"))
    await db.execute(query)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise

# Delete a user from the database
async def delete_user(db: AsyncSession, id: int):
    query = delete(UserModel).where(UserModel.id == id)
    await db.execute(query)
    try:
        await db.commit()
    except Exception:
        await db.rollback()
        raise
    return True