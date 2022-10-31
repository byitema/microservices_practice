from fastapi import FastAPI

from .auth.routers import router as auth_router
from .todo.routers import router as todo_router
from .database import engine
from .todo import models

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(auth_router)
app.include_router(todo_router)
