from fastapi import FastAPI
from routes.task_routes import router as task_router
from database import engine, Base
import models
from routes.auth_routes import router as auth_router

app = FastAPI()

app.include_router(task_router)
Base.metadata.create_all(bind=engine)
app.include_router(auth_router)




