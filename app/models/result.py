from datetime import datetime
from typing import List

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.song import Song
from app.models.user_song_match import UserSongMatch


class Result(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    next_song_id: Mapped[int]
    matched_users_songs: Mapped[List[UserSongMatch]] = relationship(
        back_populates="response"
    )
    picked_songs: Mapped[List[Song]] = relationship(back_populates="response")
    sotw_id: Mapped[int] = mapped_column(ForeignKey("sotw.id"))
    week_id: Mapped[int] = mapped_column(ForeignKey("week.id"))
    week = relationship("Week", foreign_keys=week_id, back_populates="responses")
    submitter_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    submitter = relationship(
        "User", foreign_keys=submitter_id, back_populates="responses"
    )
