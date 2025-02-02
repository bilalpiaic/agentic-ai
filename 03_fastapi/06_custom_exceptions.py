from fastapi import FastAPI, HTTPException, File, UploadFile
from pydantic import BaseModel,EmailStr,Field
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Request

app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(map(str, error["loc"])),  # Converts tuple path to a string
            "message": error["msg"]
        })
    
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "message": "Validation failed",
            "errors": errors
        }
    )

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}


# Pydantic Validations 
class Student(BaseModel):
    name: str
    age: int
    email: EmailStr
    address: str = Field(None, title="Address", max_length=50)


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str, student: Student):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}