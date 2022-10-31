from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from .schemas import *
from .crud import create_user
from .service import *

from ..database import get_db

router = APIRouter(prefix="", tags=["user"])


@router.post("/user", response_model=Token)
def register_user(
    form_data: UserCreate = Depends(),
    db: Session = Depends(get_db)
):
    form_data.password = get_hashed_password(form_data.password)
    user = create_user(db, form_data)
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/user/me", response_model=User)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
