from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    print("Hello World")
    return {"Hello": "World"}


items = {}


@app.on_event("startup")
async def startup_event():
    print("Start Aplicacao")
    items["foo"] = {"name": "Fighters"}
    items["bar"] = {"name": "Tenders"}

@app.on_event("shutdown")
def shutdown_event():
    with open("log.txt", mode="a") as log:
        log.write("Application shutdown")


@app.get("/items/")
async def read_items():
    return [{"name": "Foo"}]

@app.get("/items/{item_id}")
async def read_items(item_id: str):
    return items[item_id]