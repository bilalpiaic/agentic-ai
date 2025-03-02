import email
from pydantic import BaseModel,Field,AfterValidator
from typing_extensions import Annotated


class TodoCreate(BaseModel):
    title: str
    description: str = None  # type: ignore
    completed: bool = False
    

class LoginUser(BaseModel):
    email: str
    password: str



def is_even(value: int) -> int:
    if value % 2 == 1:
        raise ValueError(f'{value} is not an even number')
    return value
class UserCreate(BaseModel):
    name: Annotated[str, Field(min_length=3,max_length=50)]
    email: Annotated[str, Field(pattern=r'^\S+@\S+$')]
    password: Annotated[str, Field(min_length=6)]
    number: Annotated[int, AfterValidator(is_even)]
