from pydantic import BaseModel, Field
from datetime import datetime


class VideoCreate(BaseModel):
    title: str = Field(min_length = 4, max_length = 200)
    private: bool


class Video(VideoCreate):
    id: int
    uploaded_at: datetime
    uploader_id: int

    class Config:
        orm_mode = True
