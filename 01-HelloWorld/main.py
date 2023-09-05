from fastapi import FastAPI
from fastapi.responses import ORJSONResponse, UJSONResponse, JSONResponse
import uvicorn

app = FastAPI()


@app.get("/")
def read_root():
    print("Hello World")
    return {"Hello": "World"}


@app.get("/hello-world")
def hello_world():
    return JSONResponse(content={"Hello": "World"}, status_code=200)

@app.get("/hello-world-orjson")
def hello_world():
    return ORJSONResponse(content={"Hello": "World"}, status_code=200)

@app.get("/hello-world-ujson")
def hello_world():
    return UJSONResponse(content={"Hello": "World"}, status_code=200)


if __name__ == "__main__":
     uvicorn.run(app)