from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(60))
    email = Column(String(254), unique=True)
    password = Column(String(60))
    activated = Column(Boolean)

    todo_lists = relationship("ToDoList", back_populates="owner")


class ToDoList(Base):
    __tablename__ = "todo_list"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(254))
    owner_id = Column(Integer, ForeignKey("user.id"))

    owner = relationship("User", back_populates="todo_lists")
    tasks = relationship("ToDoListTask", back_populates="todo_list")


class ToDoListTask(Base):
    __tablename__ = "todo_list_task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(254))
    done = Column(Boolean)
    todo_list_id = Column(Integer, ForeignKey("todo_list.id"))

    todo_list = relationship("ToDoList", back_populates="tasks")
