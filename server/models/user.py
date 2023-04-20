from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from server.database.session import Base
from server.models.video import VideoModel
from server.models.playlist import PlaylistModel


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password: Mapped[str] = mapped_column(String(100))

    videos = relationship("VideoModel", back_populates="uploader")
    playlists = relationship("PlaylistModel", back_populates="creator")
