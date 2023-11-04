from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.init import Base
from db.response import Response


class User(Base):
    __tablename__ = 'user'

    email: Mapped[str] = mapped_column(primary_key=True)
    responses: Mapped[List[Response]] = relationship(back_populates='user')
    name: Mapped[str]