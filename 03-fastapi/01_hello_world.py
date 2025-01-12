from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def get_hello_world():
    return {"Hello": "World"}

# poetry run uvicorn 03-fastapi.01_hello_world:app
