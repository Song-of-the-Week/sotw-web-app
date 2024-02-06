from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.song import Song
from app.schemas.song import SongCreate
from app.schemas.song import SongUpdate


class CRUDSong(CRUDBase[Song, SongCreate, SongUpdate]):
    def get_song_from_user(
        self, session: Session, *, submitter_id: int, week_id: int
    ) -> Song:
        """
        Retrieves a song object from the database using the submitter's id and the week id that the song was submitted
        :session: a SQLAlchemy Session object that is connected to the database
        :submitter_id: the id of the user who submitted the song
        :week_id: the id of the week the song was created
        """
        return (
            session.query(Song)
            .filter(and_(Song.submitter_id == submitter_id, Song.week_id == week_id))
            .first()
        )


song = CRUDSong(Song)
