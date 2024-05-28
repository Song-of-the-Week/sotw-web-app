from typing import List

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.models.sotw_user_association import sotw_user_association_table
from app.db.base_class import Base
from app.models.user_playlist import UserPlaylist
from app.models.response import Response


class User(Base):

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    name: Mapped[str] = mapped_column(String, nullable=False)
    is_superuser: Mapped[bool] = mapped_column(nullable=False, default=False)
    spotify_linked: Mapped[bool] = mapped_column(nullable=False, default=False)
    spotify_access_token: Mapped[str] = mapped_column(nullable=True)
    spotify_refresh_token: Mapped[str] = mapped_column(nullable=True)
    playlists: Mapped[List[UserPlaylist]] = relationship(
        cascade="all,delete-orphan", back_populates="user"
    )
    sotw_list = relationship(
        "Sotw", secondary=sotw_user_association_table, back_populates="user_list"
    )
    responses: Mapped[List[Response]] = relationship(
        cascade="all,delete-orphan", back_populates="submitter"
    )
