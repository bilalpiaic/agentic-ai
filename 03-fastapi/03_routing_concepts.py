from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class Person(BaseModel):
    id: int
    name: str
    age: int
    email: Optional[str] = None
    address: Optional[str] = None
    

@app.post("/user/{id}")
def create_user(person: Person,id:int,query: Optional[str] = None):
    try:
      if id < 100:
        raise ValueError("ID should be greater than 100")
        # delete code?
      return {
                "status": "success",
                "data": {
                    "query": query,
                    "id": id,
                    "person":person
                    }
      }
    except Exception as e:
      return {
              "message": str(e),
                "status": "error",
                "data": None
      }

@app.get("/user")
def read_root(id: str,name:str,age:int):
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
      
      
# https://www.google.com/search?q=user+photo&rlz=1C5CHFA_enPK1067PK1067&oq=user+photo&gs_lcrp=EgZjaHJvbWUyCQgAEEUYORiABDIHCAEQABiABDIHCAIQABiABDIHCAMQABiABDIHCAQQABiABDIHCAUQABiABDIHCAYQABiABDIHCAcQABiABDIHCAgQABiABDIHCAkQABiABNIBCDUwMjlqMGo3qAIAsAIA&sourceid=chrome&ie=UTF-8#vhid=7uu-EJt8ZSmvrM&vssid=_L_KMZ9GyI--ukdUP3rOB2AY_36
      
# http://127.0.0.1:8000/user?id=2&name=John&age=30