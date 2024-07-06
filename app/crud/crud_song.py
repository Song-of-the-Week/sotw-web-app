from datetime import datetime, timedelta
from typing import List, Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.response import Response
from app.models.song import Song
from app.schemas.song import SongCreate
from app.schemas.song import SongUpdate


class CRUDSong(CRUDBase[Song, SongCreate, SongUpdate]):
    def get_songs_from_week(
        self, session: Session, *, sotw_id: int, week_id: int
    ) -> List[Song]:
        """
        Retrieves all the songs that were given in responses for a given week in a given sotw

        Args:
            session (Session): a SQLAlchemy Session object that is connected to the database
            sotw_id (int): the id of the sotw for which the songs were submitted
            week_id (int): the id of the week the songs were submitted

        Returns:
            Song: A list of song objects
        """
        return (
            session.query(Song)
            .join(Response)
            .filter(and_(Response.sotw_id == sotw_id, Response.week_id == week_id))
            .all()
        )

    def get_song_by_name(self, session: Session, *, name: str) -> Song | None:
        """
        Retrieves a song with the same name value as the one given

        Args:
            session (Session): a SQLAlchemy Session object that is connected to the database
            name (str): the name of a song and the artist(s) like `song_name - artist(1, artist2, etc.)

        Returns:
            Song: A Song object from the db
        """
        return session.query(Song).filter(Song.name == name).first()


song = CRUDSong(Song)
