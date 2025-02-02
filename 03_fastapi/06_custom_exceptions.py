# poetry add python-multipart
from fastapi import Request, FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

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


@app.get("/items/{item_id}")
def read_item(item_id: int):
    if item_id == 0:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"item_id": item_id}
