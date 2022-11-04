from fastapi import FastAPI
from pydantic import BaseModel
from random import randint


class Item(BaseModel):
    item_id: int | None = None
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    
items_fake = [
            {"item_id": 1,
            "name": "Tiago",
            "description": "Teste",
            "price": 10.5,
            "tax": 1.36
            },
            {"item_id": 2,
            "name": "Tiago",
            "description": "Teste",
            "price": 10.5,
            "tax": 1.36
            }
           ]

app = FastAPI()

#Busca um item através do ID
@app.get("/items/{item_id}")
async def read_item(item_id: int, q: str | None = None, y: str | None = None):
    return {"item_id": item_id, "q": q, "y": y}

#Busca todos os items
@app.get("/items")
async def read_items():
    return items_fake

#Inclui um novo item
@app.post("/item")
async def create_item(item: Item):
    item.item_id = randint(0,90) #Cria um id randomico
    items_fake.append(item)
    return items_fake