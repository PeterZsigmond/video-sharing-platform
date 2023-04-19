from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from server import config
from server.controllers.user import create_user, get_user_by_username, verify_user, create_jwt_token, hash_password
from server.schemas.user import User, UserCreate
from server.schemas.token import Token
from server.database.session import get_db_session


router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)


@router.post("/token", response_model=Token)
def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db_session)]):
    user = verify_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password.", headers={"WWW-Authenticate": "Bearer"})
    jwt_token = create_jwt_token(user.username, timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": jwt_token, "token_type": "bearer"}


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Annotated[Session, Depends(get_db_session)]):
    db_user = get_user_by_username(user.username, db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered.")
    return create_user(user.username, hash_password(user.password), db)
