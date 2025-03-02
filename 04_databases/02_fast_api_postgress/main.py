from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine
from models.todo_model import Todos, Users
from pydantic import BaseModel,Field,AfterValidator
from typing_extensions import Annotated
from typing import List

# Create database tables
Todos.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency for DB session


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for validation


class TodoCreate(BaseModel):
    title: str
    description: str = None  # type: ignore
    completed: bool = False


def is_even(value: int) -> int:
    if value % 2 == 1:
        raise ValueError(f'{value} is not an even number')
    return value
class UserCreate(BaseModel):
    name: Annotated[str, Field(min_length=3,max_length=50)]
    email: Annotated[str, Field(pattern=r'^\S+@\S+$')]
    password: Annotated[str, Field(min_length=6)]
    number: Annotated[int, AfterValidator(is_even)]


class TodoResponse(TodoCreate):
    id: int

    class Config:
        orm_mode = True

# Create a new Todo


@app.post("/todos/{user_id}")
def create_todo(user_id, todo: TodoCreate, db: Session = Depends(get_db)):
    try:
        db_todo = Todos(title=todo.title, description=todo.description,
                        completed=todo.completed, user_id=user_id)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return {
            "data": db_todo,
            "message": "Todo created successfully",
            "status": "success"
        }
    except Exception as e:
        print('An exception occurred')
        print(e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }


@app.post("/create_user/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        valid_user = Users(name=user.name, email=user.email,
                           password=user.password)
        db.add(valid_user)
        db.commit()
        db.refresh(valid_user)
        return {
            "data": valid_user,
            "message": "Todo created successfully",
            "status": "success"
        }
    except Exception as e:
        print('An exception occurred')
        print(e)
        return {
            "message": str(e),
            "status": "error",
            "data": None
        }


# Get all Todos


@app.get("/todos/{user_id}", response_model=List[TodoResponse])
def get_todos(user_id:str,db: Session = Depends(get_db)):
    return db.query(Todos).all()

# Get a Todo by ID


@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Update a Todo


@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoCreate, db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    todo.title = todo_update.title
    todo.description = todo_update.description
    todo.completed = todo_update.completed
    db.commit()
    db.refresh(todo)
    return todo

# Delete a Todo


@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todos).filter(Todos.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}


# uv run alembic revision --autogenerate -m "create todos table"

# uv run alembic upgrade head
