from datetime import datetime, timedelta

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.user_playlist import UserPlaylist
from app.schemas.user_playlist import UserPlaylistCreate
from app.schemas.user_playlist import UserPlaylistUpdate


class CRUDUserPlaylist(CRUDBase[UserPlaylist, UserPlaylistCreate, UserPlaylistUpdate]):

    def get_playlist_for_user_for_sotw(
        self, session: Session, *, user_id: int, sotw_id: int
    ):
        """
        Retrieves a user playlist object with the given sotw id and user id.

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            user_id (int): The id of the user for which the playlist is being sought.
            sotw_id (int): The id of the sotw for which the playlist is being sought.
        """
        return (
            session.query(UserPlaylist)
            .filter(
                and_(UserPlaylist.user_id == user_id, UserPlaylist.sotw_id == sotw_id)
            )
            .first()
        )


user_playlist = CRUDUserPlaylist(UserPlaylist)
