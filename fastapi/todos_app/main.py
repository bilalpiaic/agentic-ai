from fastapi import FastAPI, HTTPException
import uvicorn
from sqlmodel import Session, select
from dotenv import load_dotenv
load_dotenv()

from .models.todos import Todos, UpdateTodo, Users
from .config.db import create_tables, engine

app = FastAPI()


@app.get("/get_todos")
def get_todos():
    with Session(engine) as session:
        statement = select(Todos)
        results = session.exec(statement)
        data = results.all()
        print(data)
        return data

@app.get("/get_todos{todo_id}")
def get_todos_single(todo_id:int):
    with Session(engine) as session:
        statement = select(Todos).where(Todos.id == todo_id)
        results = session.exec(statement)
        data = results.all()
        print(data)
        return data


@app.put("/update_todo/{id}")
def update_todo(id:int, todo: UpdateTodo):
    with Session(engine) as session:
        db_todo = session.get(Todos, id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        todo_data = todo.model_dump(exclude_unset=True)
        db_todo.sqlmodel_update(todo_data)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return {"status": 200, "message": "todo updated successfully"}


@app.post("/create_todo")
def create_todo(todo: Todos):
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return {"status": 200, "message": "todo created successfully"}


@app.delete("/delete_todo/{todo_id}")
def delete_todo(todo_id:int):
    with Session(engine) as session:
        print(todo_id)
        db_todo = session.get(Todos, todo_id)
        print(db_todo)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(db_todo)
        return  {"status": 200, "message": "todo deleted successfully"}


@app.post("/create_user")
def create_todo(user: Users):
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"status": 200, "message": "user created successfully"}
# @app.get("/download_csv")
# def download_csv():
    # session
    # get db
    # csv(data)
    # return csv

def start():
    create_tables()
    uvicorn.run("todos.main:app", host="127.0.0.1", port=8080, reload=True)
