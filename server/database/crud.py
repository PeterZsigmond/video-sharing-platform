from sqlalchemy.orm import Session

from server.database.models.user import User


def get_user_by_username(username: str, db: Session):
    return db.query(User).filter(User.username == username).first()


def create_user(username: str, password: str, db: Session):
    user = User(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
