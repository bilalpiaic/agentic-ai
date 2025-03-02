from config.database import get_db
from fastapi import APIRouter,Depends,HTTPException
from models.todo_model import Todos
from sqlalchemy.orm import Session
from validations.validation import TodoCreate

todo_router = APIRouter()



@todo_router.post("/create")
def create_todo(user_id, todo: TodoCreate, db: Session  = Depends(get_db)):
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



@todo_router.get("/")
def get_todos(db: Session = Depends(get_db)):
    try:
        todos = db.query(Todos).all()
        return {
            "data": todos,
            "message": "Todos fetched successfully",
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

# Get a Todo by ID


@todo_router.get("/{todo_id}")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        return {
            "data": todo,
            "message": "Todo fetched successfully",
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

# Update a Todo


@todo_router.put("/{todo_id}")
def update_todo(todo_id: int, todo_update: TodoCreate, db: Session = Depends(get_db)):
    try: 
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        todo.title = todo_update.title
        todo.description = todo_update.description
        todo.completed = todo_update.completed
        db.commit()
        db.refresh(todo)
        return {
            "data": todo,
            "message": "Todo updated successfully",
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

# Delete a Todo


@todo_router.delete("/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    try:
        todo = db.query(Todos).filter(Todos.id == todo_id).first()
        if not todo:
            raise HTTPException(status_code=404, detail="Todo not found")

        db.delete(todo)
        db.commit()
        return {
            "message": "Todo deleted",
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
