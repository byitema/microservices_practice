from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session

from .models import ToDoList as ToDoListModel
from .models import ToDoListTask as ToDoListTaskModel
from .schemas import *

from ..auth.models import User as UserModel


def create_todo_list(db: Session, todo_list_create: ToDoListCreateUpdate, user_id: int) -> ToDoListModel:
    todo_list = ToDoListModel(**todo_list_create.dict(), owner_id=user_id)
    todo_list.done = False

    db.add(todo_list)
    db.commit()
    db.refresh(todo_list)

    return todo_list


def get_todo_list(db: Session, todo_list_id: int) -> Optional[ToDoListModel]:
    stmt = select(ToDoListModel).where(ToDoListModel.id == todo_list_id)
    result: Result = db.execute(stmt)
    return result.scalar()


def get_todo_lists(db: Session, user_id: int) -> List[ToDoList]:
    stmt = select(ToDoListModel).where(UserModel.id == user_id)
    result: Result = db.execute(stmt)
    return result.scalars().all()


def update_todo_list(db: Session, todo_list: ToDoListModel) -> ToDoListModel:
    db.add(todo_list)
    db.commit()
    db.refresh(todo_list)
    return todo_list


def delete_todo_list(db: Session, todo_list: ToDoListModel) -> None:
    db.delete(todo_list)
    db.commit()
