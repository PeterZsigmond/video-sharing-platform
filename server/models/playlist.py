from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Boolean, Integer, ForeignKey
from server.database.session import Base


class PlaylistModel(Base):
    __tablename__ = "playlists"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), index=True, nullable=False)
    private: Mapped[bool] = mapped_column(Boolean, nullable=False)
    creator_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)

    creator = relationship("UserModel", back_populates="playlists")
