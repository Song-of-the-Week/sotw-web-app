from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.song import Song
from app.schemas.song import SongCreate
from app.schemas.song import SongUpdate


class CRUDSong(CRUDBase[Song, SongCreate, SongUpdate]):
    def get_songs_from_week(
        self, session: Session, *, sotw_id: int, week_id: int
    ) -> Song:
        """
        Retrieves all the songs that were given in responses for a given week in a given sotw
        :session: a SQLAlchemy Session object that is connected to the database
        :sotw_id: the id of the sotw for which the songs were submitted
        :week_id: the id of the week the songs were submitted
        """
        return (
            session.query(Song)
            .filter(
                and_(Song.response.sotw_id == sotw_id, Song.response.week_id == week_id)
            )
            .all()
        )


song = CRUDSong(Song)
