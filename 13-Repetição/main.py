from fastapi import FastAPI
from fastapi_utils.tasks import repeat_every

app = FastAPI()

items = {}

@app.get("/")
@repeat_every(seconds=10)
def read_root():
    print("Hello World")
    return {"Hello": "World"}


@app.on_event("startup")
@repeat_every(seconds=10)
async def startup_event():
    print("Start Aplicacao")
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]

@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]