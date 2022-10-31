from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.orm import Session

from .schemas import *
from .models import User as UserModel


def create_user(db: Session, form_data: UserCreate) -> UserModel:
    user = UserModel(**form_data.dict())
    user.activated = True

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user(db: Session, username: str):
    stmt = select(UserModel).where(UserModel.username == username)
    result: Result = db.execute(stmt)
    return result.scalar()
