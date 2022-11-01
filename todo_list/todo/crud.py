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


def create_todo_list_task(db: Session, todo_list_task_create: ToDoListTaskCreate, user_id: int) -> ToDoListTaskModel:
    todo_list_task = ToDoListTaskModel(**todo_list_task_create.dict())
    todo_list_task.done = False

    db.add(todo_list_task)
    db.commit()
    db.refresh(todo_list_task)

    return todo_list_task


def get_todo_list_task(db: Session, todo_list_task_id: int) -> Optional[ToDoListTaskModel]:
    stmt = select(ToDoListTaskModel).where(ToDoListTaskModel.id == todo_list_task_id)
    result: Result = db.execute(stmt)
    return result.scalar()


def get_todo_list_tasks(db: Session, user_id: int) -> List[ToDoListTask]:
    stmt = select(ToDoListTaskModel).where(ToDoListModel.owner_id == user_id)
    result: Result = db.execute(stmt)
    return result.scalars().all()


def update_todo_list_task(db: Session, todo_list_task: ToDoListTaskModel) -> ToDoListTaskModel:
    db.add(todo_list_task)
    db.commit()
    db.refresh(todo_list_task)
    return todo_list_task


def delete_todo_list_task(db: Session, todo_list_task: ToDoListTaskModel) -> None:
    db.delete(todo_list_task)
    db.commit()
