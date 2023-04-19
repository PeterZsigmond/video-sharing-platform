from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Integer, DateTime, Boolean
from server.database.session import Base
from datetime import datetime


class VideoModel(Base):
    __tablename__ = "videos"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    uploader_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    private: Mapped[bool] = mapped_column(Boolean, nullable=False)

    uploader = relationship("UserModel", back_populates="videos")
