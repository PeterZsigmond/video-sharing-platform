from sqlalchemy.orm import Session
from datetime import datetime
from server.database.models.user import UserModel
from server.database.models.video import VideoModel


def get_user_by_username(username: str, db: Session):
    return db.query(UserModel).filter(UserModel.username == username).first()


def create_user(username: str, password: str, db: Session):
    user = UserModel(username=username, password=password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create_video(title: str, uploader_id: int, private: bool, db: Session):
    video = VideoModel(title=title, uploader_id=uploader_id, uploaded_at=datetime.utcnow(), private=private)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video
