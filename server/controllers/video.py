from typing import Annotated
from sqlalchemy.orm import Session
from datetime import datetime
from server.models.video import VideoModel
from server.schemas.user import User
from server.database.session import get_db_session
from server.controllers.user import authenticate_user_or_none
from fastapi import HTTPException, Depends, status


def create_video(title: str, uploader_id: int, private: bool, db: Session):
    video = VideoModel(title=title, uploader_id=uploader_id, uploaded_at=datetime.utcnow(), private=private)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video


def get_video_by_id(id: int, db: Session):
    return db.query(VideoModel).filter(VideoModel.id == id).first()


def get_all_public_videos(skip: int, limit: int, db: Session):
    return db.query(VideoModel).filter(VideoModel.private == False).offset(skip).limit(limit).all()


def get_video_path(id: int):
    return "videos/" + str(id) + ".mp4"


def validate_video_exists(id: int, db: Session):
    video_data = get_video_by_id(id, db)
    if video_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found.")
    return video_data


def validate_video_owner(video_data: VideoModel, user: User):
    if video_data.uploader_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Video's owner is not you.")
    

def validate_video_can_be_viewed_by_user(video_data: VideoModel, user: User):
    if video_data.private:
        if user is None or video_data.uploader_id != user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Video is private.")
        

def get_video_data(
        video_id: int,
        user: Annotated[User, Depends(authenticate_user_or_none)],
        db: Annotated[Session, Depends(get_db_session)]
    ):
    video_data = validate_video_exists(video_id, db)
    validate_video_can_be_viewed_by_user(video_data, user)
    return video_data
