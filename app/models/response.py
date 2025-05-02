from datetime import datetime, timezone
from typing import List

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.user_song_match import UserSongMatch


class Response(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.now(timezone.utc)
    )
    next_song_id: Mapped[int] = mapped_column(ForeignKey("song.id"), nullable=True)
    next_song = relationship("Song", back_populates="response", uselist=False)
    user_song_matches: Mapped[List[UserSongMatch]] = relationship(
        back_populates="response",
    )
    number_correct_matches: Mapped[int] = mapped_column(default=0)
    picked_song_1_id: Mapped[int] = mapped_column(nullable=True)
    picked_song_2_id: Mapped[int] = mapped_column(nullable=True)
    sotw_id: Mapped[int] = mapped_column(ForeignKey("sotw.id"))
    week_id: Mapped[str] = mapped_column(ForeignKey("week.id"))
    week = relationship("Week", foreign_keys=week_id, back_populates="responses")
    submitter_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    submitter = relationship(
        "User", foreign_keys=submitter_id, back_populates="responses"
    )
    theme: Mapped[str] = mapped_column(nullable=True)
    theme_description: Mapped[str] = mapped_column(nullable=True)
