from typing import Annotated
from sqlalchemy.orm import Session
from server.models.user import UserModel
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from server.schemas.token import TokenData
from server import config
from server.database.session import get_db_session


def get_user_by_username(username: str, db: Session):
    return db.query(UserModel).filter(UserModel.username == username).first()


def create_user(username: str, password: str, db: Session):
    user = UserModel(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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


def authenticate_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(get_db_session)]):
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
