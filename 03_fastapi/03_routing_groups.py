from xmlrpc.client import boolean
from fastapi import FastAPI,Depends,APIRouter
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class Person():
    id: int
    name: str
    age: int
    email: Optional[str] = None
    address: Optional[str] = None
    
def common_dependency():
    return {"key": "value"}
  
# @app.post("/user/{id}")
# def create_user(person:):
#     try:
#       if id < 100:
#         raise ValueError("ID should be greater than 100")
#         # delete code?
#       return {
#                 "status": "success",
#                 "data": {
#                     "query": query,
#                     "id": id,
#                     "person":person
#                     }
#       }
#     except Exception as e:
#       return {
#               "message": str(e),
#                 "status": "error",
#                 "data": None
#       }

@app.get("/user/")
def read_root2(id: str,name:str,age:int):
    try:
        # Your code goes here
        return {
            "status": "success",
            "data": {
                "id": id,
                "profile_url":"https://plus.unsplash.com/premium_photo-1734543932716-431337d9c3c4?q=80&w=2133&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D",
                "email": "abc@gmail.com",
                "name": name,
                "age": age,
                "address":["123 Main Street", "Apt 4", "New York, NY 10001"],
            }
        }
      
    except Exception as e:
      return {
           "message": str(e),
           "status": "error",
           "data": None
          }


@app.get("/students/{student_id}")
def read_student(student_id: int, include_grades:bool, semester:Optional[str]):
  try:
    if student_id > 1000 and student_id < 90000:
     return {"student_id": student_id}
    else:
     raise ValueError("Student ID is not valid")
  except Exception as e:
    print('An exception occurred')
    return {"message": str(e)}
  

class Student(BaseModel):
  name: str
  email: str
  age: int 
  courses: Optional[list] = None 
  

@app.post("/test")
def test(person):
    print("person",person)
    return {"message":"Test API"} 
  
  
postRouter = APIRouter()
@postRouter.get("/")
def read_posts():
  # db request
    return {
        "status": "success",
        "data": {
            "posts": [{
              "id":1,
              "title":"Post 1",
              },
                {
              "id":2,
              "title":"Post 2",
              },
                { 
              "id":3,
              "title":"Post 3",
              }
                ]
        }
    }
    

@postRouter.post("/create")
def create_post(post_id:int,userId:str):
  # db post
    try:
      if post_id:
        return {"message":"Post created successfully"}
      else:
        return {"message":"Post not created"}
    except Exception as e:
      return {"message": str(e)}


def delete_post(post_id:int,userId:str):
  # db post
    try:
      if post_id:
        return {"message":"Post deleted successfully"}
      else:
        return {"message":"Post not deleted"}
    except Exception as e:
      return {"message": str(e)}


@postRouter.get("/like")
def like_post(post_id:int,userId:str):
  # db post
    try:
      if post_id:
        return {"message":"Post liked successfully"}
      else:
        return {"message":"Post disliked successfully"}
    except Exception as e:
      return {"message": str(e)}



@app.get("/")
def read_root():
    return {"message": "server is running"}


app.include_router(postRouter, prefix="/posts", tags=["posts"])
    # prefix  - post
    # CRUD
# https://www.google.com/search?q=user+photo&rlz=1C5CHFA_enPK1067PK1067&oq=user+photo&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORiABDIHCAEQABiABDIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIHCAkQABiABNIBCDUwMjlqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#vhid=7uu-EJt8ZSmvrM&vssid=_L_KMZ9GyI--ukdUP3rOB2AY_36
      
# http://127.0.0.1:8000/user?id=2&name=John&age=30