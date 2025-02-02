from fastapi import FastAPI

app = FastAPI()



@app.get("/")
def get_hello_world2():
    return {"Hello": "auth"}

@app.get("/login")
def get_hello_world3():
    return {"Hello": "login"}


@app.post("/login")
def get_hello_world():
    print("Function Call!")
    return {"Hello": "login post"}


@app.delete("/login")
def get_hello_world23():
    print("Function Call!")
    return {"Hello": "login delete"}

@app.put("/login")
def get_hello_world232():
    print("Function Call!")
    return {"Hello": "login put"}

@app.get("/auth/signup")
def get_hello_world1():
    return {"Hello": "signup"}

# poetry run uvicorn 03-fastapi.01_hello_world:app
