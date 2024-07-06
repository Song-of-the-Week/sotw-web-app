from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserPlaylist(Base):

    id: Mapped[str] = mapped_column(String, primary_key=True)
    playlist_link: Mapped[str] = mapped_column(String, nullable=True)
    sotw_id: Mapped[int] = mapped_column(ForeignKey("sotw.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user = relationship("User", foreign_keys=user_id, back_populates="playlists")
