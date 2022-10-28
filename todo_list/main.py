from fastapi import FastAPI

from .database import engine
from .todo import models

models.Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
