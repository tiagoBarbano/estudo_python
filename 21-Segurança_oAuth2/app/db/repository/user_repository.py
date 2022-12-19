import datetime
from app.schema.schema import User
from app.db.model.model import UserModel
from app.utils.database import async_session
from sqlalchemy import update, delete, text
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession

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

# Retrieve a user with a matching ID
async def get_user_by_name(username: str) -> dict:
    async with async_session() as db:
        #q = text(f"select * from user where username = '{username}'")
        q = select(UserModel).where(UserModel.username == username) 
        users = await db.execute(q)
        user = users.scalar_one_or_none()
        await db.close()
        return user

# Add a new user into to the database
async def add_user(user: User) -> User:
    data_criacao = datetime.datetime.now()
    new_user = UserModel(nome_user=user.nome_user,
                              id_usuario=user.id_usuario,
                              data_criacao=data_criacao)

    async with async_session() as session:
        session.add(new_user)
        await session.commit()
        await session.close()
        
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