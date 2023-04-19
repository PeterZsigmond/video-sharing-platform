from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, Form, HTTPException, status
from fastapi.responses import FileResponse
from server.routers.users import authenticate_user
from server.schemas.user import User
from server.schemas.video import Video, VideoCreate
from server.controllers.video import create_video
from sqlalchemy.orm import Session
from server.database.session import get_db_session
from pydantic import ValidationError


router = APIRouter(
    prefix = "/videos",
    tags = ["videos"]
)


@router.post("/upload", response_model=Video, status_code=status.HTTP_201_CREATED)
def upload_video(
        title: Annotated[str, Form()],
        private: Annotated[bool, Form()],
        video: UploadFile,
        user: Annotated[User, Depends(authenticate_user)],
        db: Annotated[Session, Depends(get_db_session)]
    ):
    try:
        video_data = VideoCreate(title=title, private=private)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())
    db_video = create_video(video_data.title, user.id, video_data.private, db)
    with open("videos/" + str(db_video.id) + ".mp4", 'wb') as f:
        f.write(video.file.read())
    return db_video
