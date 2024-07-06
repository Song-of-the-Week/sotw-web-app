from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Song(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    submitter_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    response = relationship("Response", back_populates="next_song", uselist=False)
    spotify_link: Mapped[str]
    spotify_id: Mapped[str]
