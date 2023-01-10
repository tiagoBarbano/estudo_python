from fastapi import FastAPI
import asyncpg
import ujson
from fastapi.responses import UJSONResponse, ORJSONResponse

app = FastAPI()

@app.on_event("startup")
async def startup():
    global pool
    pool = await asyncpg.create_pool(user='postgres',
                                    database='postgres',
                                    host='127.0.0.1',
                                    password='changeme',
                                    port=5432)
    app.state.pool = pool
    print("Conexao realizada", app.state.pool)

@app.get("/")
async def read_root():
    global pool
    async with pool.acquire() as conn:
        values = await conn.fetch(
            'SELECT * FROM "users" LIMIT 100'
        )
        return values

@app.get("/orjson")
async def orjson():
    global pool
    async with pool.acquire() as conn:
        values = await conn.fetch(
            'SELECT * FROM "users" LIMIT 100'
        )
        r = [dict(v) for v in values]
        return ORJSONResponse(content=r)

@app.get("/ujson")
async def ujson():
    global pool
    async with pool.acquire() as conn:
        values = await conn.fetch(
            'SELECT * FROM "users" LIMIT 100'
        )
        r = [dict(v) for v in values]
        return UJSONResponse(content=r)