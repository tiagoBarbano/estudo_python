from .schema import ItemSchema, ItemSchemaUpdate
from .config import get_settings
import asyncpg

settings = get_settings()

async def startup():
    global pool
    pool = await asyncpg.create_pool(database=settings.database_db,
                                    host=settings.host_db,
                                    password=settings.password_db,
                                    user=settings.user_db,
                                    port=settings.port_db)
    print("Conexao realizada", pool)
    
           
async def get_all_items():
    global pool
    async with pool.acquire() as conn:
        values = await conn.fetch('SELECT * FROM "items"')
        r = [dict(v) for v in values]
        return r


async def get_item_by_id(id: int) -> dict:
    global pool
    async with pool.acquire() as conn:
        values = await conn.fetchrow('SELECT * FROM "items" WHERE ID = $1', id)
        
        if values is None:
            return values    
        
        r = dict(values)            
        return r


async def add_item(user_data: ItemSchemaUpdate) -> ItemSchema:
    global pool
    async with pool.acquire() as conn:
        values = await conn.fetchrow('''INSERT INTO items(num_item, nome_item) VALUES ($1, $2) RETURNING *''', 
                                      user_data.num_item, user_data.nome_item, )
        new_user = dict(values)
        return new_user


async def update_item(id: str, data: ItemSchemaUpdate):   
    global pool
    async with pool.acquire() as conn:
        values = await conn.execute('''UPDATE items SET num_item=$1, nome_item=$2 WHERE id=$3''', 
                                            data.num_item, data.nome_item, id)
        
        if values == 'UPDATE 1':
            return True

        return False


async def delete_item(id: int):
    global pool
    async with pool.acquire() as conn:
        values = await conn.execute('''DELETE FROM items WHERE id=$1''', id)
        
        if values != 'DELETE 0':
            return True

        return False
