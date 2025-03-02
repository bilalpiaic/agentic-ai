from fastapi import FastAPI
from dotenv import load_dotenv
from routes import todo_routes, user_routes

load_dotenv()


app = FastAPI()

app.include_router(todo_routes.todo_router, prefix="/todos", tags=["Todo"])
app.include_router(user_routes.user_router, prefix="/users", tags=["User"])



# uv run alembic revision --autogenerate -m "create todos table"
# uv run alembic upgrade head
