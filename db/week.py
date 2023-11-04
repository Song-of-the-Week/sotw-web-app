from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from db.init import Base
from db.result import Result
from db.response import Response


class Week(Base):
    __tablename__ = 'week'

    id: Mapped[int] = mapped_column(primary_key=True)
    responses: Mapped[List[Response]] = relationship(back_populates='week')
    user: Mapped[Result] = relationship(back_populates='week')
    form_id: Mapped[int]