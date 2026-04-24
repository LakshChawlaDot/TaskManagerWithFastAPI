from fastapi import APIRouter
from schemas import Task,TaskResponse
from database import SessionLocal
from models import TaskDB
from sqlalchemy.orm import Session
from fastapi import Depends
from database import get_db

router = APIRouter()

tasks = []

@router.post("/tasks", response_model=TaskResponse)
def create_task(task: Task, db: Session = Depends(get_db)):
    db_task = TaskDB(**task.dict())

    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(TaskDB).all()


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if task:
        return task
    return {"error": "Not found"}


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if task:
        return task
    return {"error": "Not found"}


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()

    if task:
        db.delete(task)
        db.commit()
        return {"message": "Deleted"}

    return {"error": "Not found"}