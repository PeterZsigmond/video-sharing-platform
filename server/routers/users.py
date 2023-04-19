from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from server import config
from server.controllers.user import create_user, get_user_by_username
from server.database.session import SessionLocal
from server.schemas.user import User, UserCreate
from server.schemas.token import Token, TokenData


router = APIRouter(
    prefix = "/users",
    tags = ["users"]
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(password, hash):
    return pwd_context.verify(password, hash)


def hash_password(password):
    return pwd_context.hash(password)


def verify_user(username: str, password: str, db: Session):
    user = get_user_by_username(username, db)
    if user is None:
        return None
    if not verify_password(password, user.password):
        return None
    return user


def create_jwt_token(sub: str, expires_delta: timedelta):
    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": sub, "exp": expire}
    jwt_token = jwt.encode(to_encode, config.SECRET_KEY, algorithm="HS256")
    return jwt_token


def authenticate_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db)]):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials.", headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=["HS256"])
    except JWTError:
        raise credentials_exception
    username = payload.get("sub")
    if username is None:
        raise credentials_exception
    token_data = TokenData(username=username)
    user = get_user_by_username(token_data.username, db)
    if user is None:
        raise credentials_exception
    return user


@router.post("/token", response_model=Token)
def get_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(get_db)]):
    user = verify_user(form_data.username, form_data.password, db)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password.", headers={"WWW-Authenticate": "Bearer"})
    jwt_token = create_jwt_token(user.username, timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": jwt_token, "token_type": "bearer"}


@router.get("/me", response_model=User)
def get_authenticated_user(user: Annotated[User, Depends(authenticate_user)]):
    return user


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    db_user = get_user_by_username(user.username, db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username already registered.")
    return create_user(user.username, hash_password(user.password), db)
