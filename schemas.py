from pydantic import BaseModel

class Task(BaseModel):
    id: int
    title: str
    completed: bool

class TaskResponse(BaseModel):
    id: int
    title: str
    completed: bool

    class Config:
        from_attributes = True

class User(BaseModel):
    username: str
    password: str