from fastapi import FastAPI 
from routes.auth_routes import authRouter
from routes.posts_routes import postsRouter


app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "server is running"}

app.include_router(authRouter, prefix="/auth", tags=["auth"])
app.include_router(postsRouter, prefix="/posts", tags=["posts"])