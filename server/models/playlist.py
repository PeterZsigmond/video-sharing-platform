from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table, Column
from server.database.session import Base
from server.models.video import VideoModel


playlists_videos = Table(
    "playlists_videos",
    Base.metadata,
    Column("playlist_id", ForeignKey("playlists.id"), primary_key=True),
    Column("video_id", ForeignKey("videos.id"), primary_key=True)
)


class PlaylistModel(Base):
    __tablename__ = "playlists"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    private: Mapped[bool] = mapped_column(Boolean, nullable=False)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    creator = relationship("UserModel", back_populates="playlists")
    videos: Mapped[list[VideoModel]] = relationship(secondary=playlists_videos)
