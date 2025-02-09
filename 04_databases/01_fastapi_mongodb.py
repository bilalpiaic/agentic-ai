from fastapi import FastAPI
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
from pydantic import BaseModel

from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
print(os.getenv("DB_URI"))

class Todo(BaseModel):
    title: str
    description: str
    status: str

def get_db_client():
    try:
        client = MongoClient(os.getenv("DB_URI"))
        print("Connected to the database")
        return client
    except Exception as e:
        print(f"Error connecting to the database: {e}")
        return None

client = get_db_client()
db = client["fastapidb"] # type: ignore

@app.get("/")
def read_root():
    return {"status": "Server is running"}


@app.get("/todos")
def read_todos():
    try:
        todos = db.todos.find()
        listTodos = []
        for todo in todos:
            listTodos.append({
                "id": str(todo["_id"]),
                "title": todo["title"],
                "description": todo["description"],
                "status": todo["status"],
                "created_at": todo["created_at"],
            })
        return {
            "data": listTodos,
            "error": None,
            "message": "Todos read successfully",
            "status": "success"
            }
    except Exception as e:
        print(f"Error reading todos: {e}")
        return {
            "data": [],
            "error": "Error reading todos",
            "message": str(e),
            "status": "failed"
            }
        
@app.get("/todos/{id}")
def read_todo_by_id(id: str):
    print(id)
    try:
        todo = db.todos.find_one({"_id": ObjectId(id)})
        if todo is None:
            return {
                "data": {},
                "error": "Todo not found",
                "message": "Todo not found",
                "status": "failed"
                }
        return {
            "data": {
                "id": str(todo["_id"]),
                "title": todo["title"],
                "description": todo["description"],
                "status": todo["status"],
                "created_at": todo["created_at"],
            },
            "error": None,
            "message": "Todo read successfully",
            "status": "success"
            }
    except Exception as e:
        print(f"Error reading todo: {e}")
        return {
            "data": {},
            "error": "Error reading todo",
            "message": str(e),
            "status": "failed"
            }
        

@app.get("/fetch_todo_by_title")
def read_todo_by_title(title:str):
    try:
        todo = db.todos.find_one({"title": title})
        if todo is None:
            return {
                "data": {},
                "error": "Todo not found",
                "message": "Todo not found",
                "status": "failed"
                }
        return {
            "data": {
                "id": str(todo["_id"]),
                "title": todo["title"],
                "description": todo["description"],
                "status": todo["status"],
                "created_at": todo["created_at"],
            },
            "error": None,
            "message": "Todo read successfully",
            "status": "success"
            }
    except Exception as e:
        print(f"Error reading todo: {e}")
        return {
            "data": {},
            "error": "Error reading todo",
            "message": str(e),
            "status": "failed"
            }
        

@app.post("/create_todo")
def create_todo(todo: Todo):
    try:
        result = db.todos.insert_one({
            "title": todo.title,
            "description": todo.description,
            "status": todo.status,
            "created_at": str(datetime.now())
        })
        return {
            "data": {"id": str(result.inserted_id)},
            "error": None,
            "message": "Todo created successfully",
            "status": "success"
            }
    except Exception as e:
        print(f"Error creating todo: {e}")
        return {
            "data": {},
            "error": "Error creating todo",
            "message": str(e),
            "status": "failed"
            }
        
@app.delete("/delete_todo/{id}")
def delete_todo(id: str):
    try:
        result = db.todos.delete_one({"_id": ObjectId(id)})
        if result.deleted_count == 0:
            return {
                "data": {},
                "error": "Todo not found",
                "message": "Todo not found",
                "status": "failed"
                }
        return {
            "data": {},
            "error": None,
            "message": "Todo deleted successfully",
            "status": "success"
            }
    except Exception as e:
        print(f"Error deleting todo: {e}")
        return {
            "data": {},
            "error": "Error deleting todo",
            "message": str(e),
            "status": "failed"
            }

@app.put("/update_todo/{id}")
def update_todo(id: str, todo: Todo):
    try:
        result = db.todos.update_one(
            {"_id": ObjectId(id)},
            {
                "$set": {
                    "title": todo.title,
                    "description": todo.description,
                    "status": todo.status
                }
            }
        )
        if result.modified_count == 0:
            return {
                "data": {},
                "error": "Todo not found",
                "message": "Todo not found",
                "status": "failed"
                }
        return {
            "data": {},
            "error": None,
            "message": "Todo updated successfully",
            "status": "success"
            }
    except Exception as e:
        print(f"Error updating todo: {e}")
        return {
            "data": {},
            "error": "Error updating todo",
            "message": str(e),
            "status": "failed"
            }