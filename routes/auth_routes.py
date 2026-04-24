from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import UserDB
from schemas import User
from auth import hash_password, verify_password, create_access_token
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from jose import JWTError, jwt
from auth import SECRET_KEY, ALGORITHM
from schemas import Task, TaskResponse
from models import TaskDB

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@router.post("/signup")
def signup(user: User, db: Session = Depends(get_db)):
    hashed = hash_password(user.password)

    db_user = UserDB(
        username=user.username,
        password=hashed
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": "User created"}

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    db_user = db.query(UserDB).filter(UserDB.username == form_data.username).first()

    if not db_user:
        return {"error": "User not found"}

    if not verify_password(form_data.password, db_user.password):
        return {"error": "Wrong password"}

    token = create_access_token({"sub": form_data.username})

    return {"access_token": token, "token_type": "bearer"}



def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        return username
    except JWTError:
        return None


def get_current_user(db: Session = Depends(get_db),token: str = Depends(oauth2_scheme)):
    username = verify_token(token)

    if username is None:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = db.query(UserDB).filter(UserDB.username == username).first()

    return user

@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    user: str = Depends(get_current_user)   # 🔥 PROTECTION
):
    return db.query(TaskDB).filter(TaskDB.user_id == user.id).all()

@router.post("/tasks", response_model=TaskResponse)
def create_task(
    task: Task,
    db: Session = Depends(get_db),
    user:UserDB = Depends(get_current_user)
):
    db_task = TaskDB( title=task.title,
        completed=task.completed,
        user_id=user.id )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    return db_task