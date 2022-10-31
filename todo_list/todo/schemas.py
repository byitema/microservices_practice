from pydantic import BaseModel, Field


class ToDoListBase(BaseModel):
    title: str = Field(..., example="today's tasks", max_length=254)


class ToDoList(ToDoListBase):
    id: int = Field(..., gt=0, example=1)

    class Config:
        orm_mode = True


class ToDoListCreateUpdate(ToDoListBase):
    pass


class ToDoListTaskBase(BaseModel):
    title: str = Field(..., example="running", max_length=254)


class ToDoListTask(ToDoListTaskBase):
    id: int = Field(..., gt=0, example=1)
    done: bool = Field(False, description="task is done or not")

    class Config:
        orm_mode = True


class ToDoListTaskCreate(ToDoListTaskBase):
    todo_list_id: int = Field(..., gt=0, example=1)


class ToDoListTaskUpdate(ToDoListTaskBase):
    done: bool = Field(False, description="task is done or not")
