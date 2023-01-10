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
    global pool
    async with pool.acquire() as conn:
        values = await conn.fetch('SELECT * FROM "users"')
        r = [dict(v) for v in values]
        return r


async def get_user_by_id(id: int) -> dict:
    global pool
    async with pool.acquire() as conn:
        values = await conn.fetchrow('SELECT * FROM "users" WHERE ID = $1', id)
        
        if values is None:
            return values    
        
        r = dict(values)            
        return r


async def add_user(user_data: UserSchemaUpdate) -> UserSchema:
    global pool
    async with pool.acquire() as conn:
        values = await conn.fetchrow('''INSERT INTO users(num_item, nome_item) VALUES ($1, $2) RETURNING *''', 
                                      user_data.num_item, user_data.nome_item, )
        new_user = dict(values)
        return new_user


async def update_user(id: str, data: UserSchemaUpdate):   
    global pool
    async with pool.acquire() as conn:
        values = await conn.execute('''UPDATE users SET num_item=$1, nome_item=$2 WHERE id=$3''', 
                                            data.num_item, data.nome_item, id)
        
        if values == 'UPDATE 1':
            return True

        return False


async def delete_user(id: int):
    global pool
    async with pool.acquire() as conn:
        values = await conn.execute('''DELETE FROM users WHERE id=$1''', id)
        
        if values != 'DELETE 0':
            return True

        return False
