from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from config.database import SessionLocal, engine
from models.todo_model import Todo
from pydantic import BaseModel
from typing import List

# Create database tables
Todo.metadata.create_all(bind=engine)

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
    description: str = None # type: ignore
    completed: bool = False

class TodoResponse(TodoCreate):
    id: int
    class Config:
        orm_mode = True

# Create a new Todo
@app.post("/todos/", response_model=TodoResponse)
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    db_todo = Todo(title=todo.title, description=todo.description, completed=todo.completed)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

# Get all Todos
@app.get("/todos/")
def get_todos(db: Session = Depends(get_db)):
    return db.query(Todo).all()

# Get a Todo by ID
@app.get("/todos/{todo_id}", response_model=TodoResponse)
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

# Update a Todo
@app.put("/todos/{todo_id}", response_model=TodoResponse)
def update_todo(todo_id: int, todo_update: TodoCreate, db: Session = Depends(get_db)):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
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
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.delete(todo)
    db.commit()
    return {"message": "Todo deleted"}


# uv run alembic revision --autogenerate -m "create todos table"

# alembic upgrade head