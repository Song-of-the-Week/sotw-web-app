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
    results_datetime: Mapped[float]
    master_playlist_link: Mapped[str]
    master_playlist_id: Mapped[str]
    soty_playlist_link: Mapped[str]
    soty_playlist_id: Mapped[str]
    created_at: Mapped[DateTime] = mapped_column(DateTime, default=datetime.utcnow())
    owner_id: Mapped[int]
    user_list = relationship(
        "User", secondary=sotw_user_association_table, back_populates="sotw_list"
    )
