from fastapi import FastAPI
import asyncio


async def calculo1():
    print("Inicio Calculo1")
    await asyncio.sleep(1)
    print("Termino Calculo1")
    return 1

async def calculo2():
    print("Inicio Calculo2")
    await asyncio.sleep(1)
    print("Termino Calculo2")
    return 2

async def calculo3():
    print("Inicio Calculo3")
    await asyncio.sleep(1)
    print("Termino Calculo3")
    return 3

app = FastAPI()

#Busca de forma async sequencial
@app.get("/calc_async")
async def read_item():
    c1 = await calculo1()
    c2 = await calculo2()
    c3 = await calculo3()
    
    return c1 + c2 + c3


#Busca de forma async paralelo
@app.get("/calc_asyncio")
async def read_item():
    c1, c2, c3 = await asyncio.gather(calculo1(), 
                                      calculo2(), 
                                      calculo3())

    return c1 + c2 + c3