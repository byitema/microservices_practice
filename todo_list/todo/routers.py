from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session

from .schemas import *
from .crud import create_todo_list, get_todo_list, get_todo_lists, update_todo_list, delete_todo_list

from ..auth.schemas import *
from ..auth.service import get_current_active_user
from ..database import get_db

router = APIRouter(prefix="/todo_list", tags=["todo_list"])


@router.get("", response_model=List[ToDoList])
def list_todo_list(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return get_todo_lists(db, current_user.id)


@router.post("", response_model=ToDoList)
def create_todo_list(
    todo_list_body: ToDoListCreateUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return create_todo_list(db, todo_list_body, current_user.id)


@router.put("/{todo_list_id}", response_model=ToDoList)
def update_todo_list(
    todo_list_body: ToDoListCreateUpdate,
    todo_list_id: int = Path(..., gt=0),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db),
):
    task = get_todo_list(db, todo_list_id)
    if task is None:
        raise HTTPException(status_code=404, detail="ToDoList not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Not authenticated for updating this ToDoList")
    task.title = todo_list_body.title
    return update_todo_list(db, task)


@router.delete("/{todo_list_id}", response_model=None)
def delete_todo_list(
    todo_list_id: int = Path(..., gt=0),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = get_todo_list(db, todo_list_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    if task.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Not authenticated for deleting this task")
    delete_todo_list(db, task)
