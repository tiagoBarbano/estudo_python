import aiohttp
from .config import get_settings
from fastapi import HTTPException, status
from cache import AsyncTTL

setting = get_settings()


@AsyncTTL(time_to_live=55, maxsize=1024)
async def proxy_token():
    print("inicio token")
    async with aiohttp.ClientSession() as session:
        async with session.post(setting.url_token, data={"username": setting.user_token, "password": setting.password_token}, ssl=False) as response:
            if response.status != 200:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
            resposta = await response.json()
            print("fim token")
            return resposta['access_token']
        

async def proxy_get_items(token: str):
    print("inicio get")
    async with aiohttp.ClientSession(headers={"token": token }) as session:
        async with session.get(setting.url_items, ssl=False) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status)
            res = await response.json()
            print("termino get")
            return res
            