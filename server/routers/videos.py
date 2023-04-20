from typing import Annotated
from fastapi import APIRouter, Depends, UploadFile, Form, status, Query
from fastapi.responses import FileResponse
from server.schemas.user import User
from server.schemas.video import Video
from server.controllers.user import authenticate_user
from server.controllers.video import create_video, get_video_data, get_all_public_videos, validate_video_exists, validate_video_owner, validate_video_file, validate_video_create_data, write_video_file, video_file_path
from server.controllers.thumbnail import validate_thumbnail_file, write_thumbnail_file, delete_thumbnail, get_thumbnail_path
from sqlalchemy.orm import Session
from server.database.session import get_db_session


router = APIRouter(
    prefix = "/videos",
    tags = ["videos"]
)


@router.post("/upload", response_model=Video, status_code=status.HTTP_201_CREATED)
def upload_video(
        title: Annotated[str, Form()],
        private: Annotated[bool, Form()],
        video: Annotated[UploadFile, Depends(validate_video_file)],
        user: Annotated[User, Depends(authenticate_user)],
        db: Annotated[Session, Depends(get_db_session)]
    ):
    video_data = validate_video_create_data(title, private)
    db_video = create_video(video_data.title, user.id, video_data.private, db)
    write_video_file(video, db_video.id)
    return db_video


@router.get("/browse", response_model=list[Video])
def browse_public_videos(
        db: Annotated[Session, Depends(get_db_session)],
        skip: Annotated[int, Query(ge=0)] = 0,
        limit: Annotated[int, Query(ge=1, le=50)] = 50
    ):
    return get_all_public_videos(skip, limit, db)


@router.post("/upload-thumbnail", status_code=status.HTTP_201_CREATED)
def upload_thumbnail(
        video_id: Annotated[int, Form()],
        thumbnail: Annotated[UploadFile, Depends(validate_thumbnail_file)],
        user: Annotated[User, Depends(authenticate_user)],
        db: Annotated[Session, Depends(get_db_session)]
    ):
    video_data = validate_video_exists(video_id, db)
    validate_video_owner(video_data, user)
    delete_thumbnail(video_data.id)
    write_thumbnail_file(thumbnail, video_data.id)    
    return {"detail": "Successfully uploaded thumbnail."}


@router.get("/thumbnail/{video_id}")
def get_thumbnail(video_data: Annotated[Video, Depends(get_video_data)]):
    thumbnail_path = get_thumbnail_path(video_data.id)
    return FileResponse(thumbnail_path)


@router.get("/data/{video_id}", response_model=Video)
def show_video_data(video_data: Annotated[Video, Depends(get_video_data)]):
    return video_data


@router.get("/{video_id}")
def show_video(video_data: Annotated[Video, Depends(get_video_data)]):
    return FileResponse(video_file_path(video_data.id))
