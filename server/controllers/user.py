from sqlalchemy.orm import Session
from server.models.user import UserModel


def get_user_by_username(username: str, db: Session):
    return db.query(UserModel).filter(UserModel.username == username).first()


def create_user(username: str, password: str, db: Session):
    user = UserModel(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
