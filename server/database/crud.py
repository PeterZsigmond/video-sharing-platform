from sqlalchemy.orm import Session

from server.database.models.user import User


def get_user_by_username(username: str, db: Session) -> User | None:
    return db.query(User).filter(User.username == username).first()
