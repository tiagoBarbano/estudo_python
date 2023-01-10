from .schema import UserSchema, UserSchemaUpdate
from .model import UserModel
from sqlalchemy import update, delete
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
import asyncpg


async def startup():
    global pool
    pool = await asyncpg.create_pool(user='postgres',
                                    database='postgres',
                                    host='127.0.0.1',
                                    password='changeme',
                                    port=5432)
    print("Conexao realizada", pool)
    
    
        
async def get_all_users():
    async with pool.acquire() as conn:
        values = await conn.fetch(
            'SELECT * FROM "users" LIMIT 100'
        )
        r = [dict(v) for v in values]
        return r


async def get_user_by_id(db: AsyncSession, id: int) -> dict:
    query = select(UserModel).where(UserModel.id == id)
    users = await db.execute(query)
    user = users.scalar_one_or_none()
    return user


async def add_user(db: AsyncSession, user_data: UserSchemaUpdate) -> UserSchema:
    new_user = UserModel(nome_item = user_data.nome_item,
                         num_item = user_data.num_item)
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


async def delete_user(id: int, db: AsyncSession):
    query = delete(UserModel).where(UserModel.id == id)
    res = await db.execute(query)

    if res.rowcount == 1:
        await db.commit()
        return True

    return False
