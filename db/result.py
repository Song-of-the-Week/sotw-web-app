from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.init import Base
from db.week import Week
from db.user import User


class Result(Base):
    __tablename__ = 'response'

    id: Mapped[int] = mapped_column(primary_key=True)
    week: Mapped[Week] = relationship(back_populates='result')
    first_place_song: Mapped[List[User]]
    second_place_song: Mapped[List[User]]
    first_place_guesses: Mapped[List[User]]
    second_place_guesses: Mapped[List[User]]