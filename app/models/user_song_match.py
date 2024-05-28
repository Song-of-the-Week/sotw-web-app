from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class UserSongMatch(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    song_id: Mapped[int] = mapped_column(ForeignKey("song.id"))
    correct_guess: Mapped[bool]
    response_id: Mapped[int] = mapped_column(ForeignKey("response.id"))
    response = relationship(
        "Response", foreign_keys=response_id, back_populates="matched_users_songs"
    )
