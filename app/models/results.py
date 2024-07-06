from datetime import datetime
from typing import List

from sqlalchemy import DateTime, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.song import Song
from app.models.user_song_match import UserSongMatch


class Results(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow()
    )
    sotw_id: Mapped[int] = mapped_column(ForeignKey("sotw.id"))
    week_id: Mapped[str] = mapped_column(ForeignKey("week.id"))
    first_place: Mapped[str] = mapped_column(nullable=False)
    second_place: Mapped[str] = mapped_column(nullable=False)
    all_songs: Mapped[str] = mapped_column(String, default="", nullable=False)
    guessing_data: Mapped[str] = mapped_column(String, default="", nullable=False)
