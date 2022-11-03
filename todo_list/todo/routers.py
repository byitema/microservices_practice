import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from kafka import KafkaProducer
from sqlalchemy.orm import Session

from .schemas import *
from .crud import create_todo_list, get_todo_list, get_todo_lists, update_todo_list, delete_todo_list, \
    get_todo_list_tasks, create_todo_list_task, get_todo_list_task, update_todo_list_task

from ..auth.schemas import *
from ..auth.service import get_current_active_user
from ..database import get_db

router = APIRouter(prefix="/todo_list", tags=["todo_list"])
producer = KafkaProducer(bootstrap_servers='kafka:9092', api_version=(2, 0, 2),
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))


@router.get("", response_model=List[ToDoList])
def list_todo_list_(
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    return get_todo_lists(db, current_user.id)


@router.post("", response_model=ToDoList)
def create_todo_list_(
        todo_list_body: ToDoListCreateUpdate,
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    return create_todo_list(db, todo_list_body, current_user.id)


@router.put("/{todo_list_id}", response_model=ToDoList)
def update_todo_list_(
        todo_list_body: ToDoListCreateUpdate,
        todo_list_id: int = Path(..., gt=0),
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    todo_list = get_todo_list(db, todo_list_id)
    if todo_list is None:
        raise HTTPException(status_code=404, detail="ToDoList not found")
    if todo_list.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Not authenticated for updating this ToDoList")
    todo_list.title = todo_list_body.title
    return update_todo_list(db, todo_list)


@router.delete("/{todo_list_id}", response_model=None)
def delete_todo_list_(
        todo_list_id: int = Path(..., gt=0),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    todo_list = get_todo_list(db, todo_list_id)
    if todo_list is None:
        raise HTTPException(status_code=404, detail="ToDoList not found")
    if todo_list.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Not authenticated for deleting this ToDoList")
    delete_todo_list(db, todo_list)


router_task = APIRouter(prefix="/{todo_list_id}/task", tags=["todo_list_task"])


@router_task.get("", response_model=List[ToDoListTask])
def list_todo_list_task_(
        todo_list_id: int = Path(..., gt=0),
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    return get_todo_list_tasks(db, current_user.id, todo_list_id)


@router_task.post("", response_model=ToDoListTask)
def create_todo_list_task_(
        todo_list_task_body: ToDoListTaskCreate,
        todo_list_id: int = Path(..., gt=0),
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db)
):
    task = create_todo_list_task(db, todo_list_task_body, current_user.id, todo_list_id)
    producer.send('statistics', {'user_id': current_user.id, 'task_id': task.id, 'method': 'create'})
    producer.flush()
    return task


@router_task.put("/{todo_list_task_id}", response_model=ToDoListTask)
def update_todo_list_task_(
        todo_list_task_body: ToDoListTaskUpdate,
        todo_list_id: int = Path(..., gt=0),
        todo_list_task_id: int = Path(..., gt=0),
        current_user: User = Depends(get_current_active_user),
        db: Session = Depends(get_db),
):
    task = get_todo_list_task(db, todo_list_task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="ToDoListTask not found")
    if task.todo_list.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Not authenticated for updating this ToDoListTask")
    task.done = todo_list_task_body.done
    task.title = todo_list_task_body.title

    updated_task = update_todo_list_task(db, task)
    if task.done:
        producer.send('statistics', {'user_id': current_user.id, 'task_id': task.id, 'method': 'finish'})
        producer.flush()
    return updated_task


@router_task.delete("/{todo_list_task_id}", response_model=None)
def delete_todo_list_task_(
        todo_list_id: int = Path(..., gt=0),
        todo_list_task_id: int = Path(..., gt=0),
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_active_user)
):
    task = get_todo_list_task(db, todo_list_task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="ToDoListTask not found")
    if task.todo_list.owner_id != current_user.id:
        raise HTTPException(status_code=401, detail="Not authenticated for deleting this ToDoListTask")
    delete_todo_list(db, task)
    producer.send('statistics', {'user_id': current_user.id, 'task_id': task.id, 'method': 'delete'})
    producer.flush()


router.include_router(router_task)
