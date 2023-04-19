from sqlalchemy.orm import Session
from datetime import datetime
from server.models.video import VideoModel


def create_video(title: str, uploader_id: int, private: bool, db: Session):
    video = VideoModel(title=title, uploader_id=uploader_id, uploaded_at=datetime.utcnow(), private=private)
    db.add(video)
    db.commit()
    db.refresh(video)
    return video
