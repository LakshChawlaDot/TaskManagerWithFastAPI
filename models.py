from sqlalchemy import Column, Integer, String, Boolean,ForeignKey
from database import Base

class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    completed = Column(Boolean)
    user_id = Column(Integer, ForeignKey("users.id"))

class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)