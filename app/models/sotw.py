from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.db.base_class import Base
from app.models.sotw_user_association import sotw_user_association_table


class Sotw(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    survey_datetime: Mapped[DateTime] = mapped_column(DateTime)
    results_datetime: Mapped[DateTime] = mapped_column(DateTime)
    share_id: Mapped[str]
    playlist_link: Mapped[str]
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow())
    user_list = relationship(
        "User", secondary=sotw_user_association_table, back_populates="sotw_list"
    )
