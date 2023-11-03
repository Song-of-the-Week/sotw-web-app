from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.init import Base
from db.week import Week
from db.user import User


class Response(Base):
    __tablename__ = 'response'

    id: Mapped[int] = mapped_column(primary_key=True)
    week: Mapped[Week] = relationship(back_populates='responses')
    user: Mapped[User] = relationship(back_populates='responses')
    top_two_songs: Mapped[List[str]]
    user_song_matches: Mapped[str] #TODO finalize structure
    previous_song: Mapped[str] #TODO finalize structure
    next_song: Mapped[str] #TODO finalize structure