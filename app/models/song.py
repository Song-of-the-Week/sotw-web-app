from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Song(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    submitter_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
    response_id: Mapped[int] = mapped_column(ForeignKey('response.id'))
    response = relationship('Response', foreign_keys=response_id, back_populates='picked_songs')
    spotify_link: Mapped[str]
