from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from config.database import get_db
from models.todo_model import Users
from utils.utils_helper import create_access_token
from validations.validation import LoginUser, UserCreate



user_router = APIRouter()


@user_router.post("/register")
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
        

@user_router.post("/login")
def login_user(user:LoginUser, db: Session = Depends(get_db)):
    try:
        db_user = db.query(Users).filter(Users.email == user.email).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="User not found")
        if db_user.password != user.password:
            raise HTTPException(status_code=401, detail="Invalid password")
        token = create_access_token(data={"sub": db_user.email})
        user_data = {
            "name": db_user.name,
            "email": db_user.email,
            "token": token
        }
        return {
            "data": user_data,
            "message": "User logged in successfully",
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

