from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.middleware("http")
async def add_process_time_header(request, call_next):
    print("request",request)
    print("call_next",call_next)
    response = await call_next(request)
    response.headers["X-Process-Time"] = "10 sec"
    return response

@app.get("/")
def read_root():
    return {"message": "server is running"}


@app.get("/posts")
async def read_posts():
    # db request
    # pdf create
    # email
    return {
        "status": "success",
        "data": {
            "posts": [
                {"id": 1, "title": "Post 1"},
                {"id": 2, "title": "Post 2"},
                {"id": 3, "title": "Post 3"},
            ]
        },
    }
    
    
@app.get("/abc")
def abc_root():
    return {"message": "abc"}
