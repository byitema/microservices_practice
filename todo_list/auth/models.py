from sqlalchemy import Column, String, Integer, Boolean
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
