from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    phone: str
    address: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class Todos(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    is_completed: bool
    user_id: int | None = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now())
    


class UpdateTodo(SQLModel):
    title: str | None
    description: int | None
    is_completed: bool | None
