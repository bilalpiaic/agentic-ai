from fastapi import APIRouter
from utils.posts_utility import post_data

postsRouter = APIRouter()

@postsRouter.get("/")
async def get_posts():
    return {"message": "Get all posts"}

@postsRouter.get("/{post_id}")
async def get_post(post_id: int):
    data = post_data(post_id)
    print(data)
    return {"message": f"Get post with id {post_id}", "data": data}

@postsRouter.post("/create")
async def create_post():
    return {"message": "Create post"}

@postsRouter.put("/update/{post_id}")
async def update_post(post_id: int):
    return {"message": f"Update post with id {post_id}"}


@postsRouter.delete("/delete/{post_id}")
async def delete_post(post_id: int):
    return {"message": f"Delete post with id {post_id}"}