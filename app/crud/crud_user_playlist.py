from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.user_playlist import UserPlaylist
from app.schemas.user_playlist import UserPlaylistCreate
from app.schemas.user_playlist import UserPlaylistUpdate


class CRUDUserPlaylist(CRUDBase[UserPlaylist, UserPlaylistCreate, UserPlaylistUpdate]):

    def create(
        self, session: Session, *, object_in: UserPlaylistCreate
    ) -> UserPlaylist:
        """
        Creates a Response in the database
        :session: a SQLAlchemy Session object that is connected to the database
        :object_in: a pydantic model ResponseCreate object
        """
        # TODO once we know what the data coming from the api endpoint looks like

    def update(
        self,
        session: Session,
        *,
        db_object: UserPlaylist,
        object_in: UserPlaylistUpdate
    ) -> UserPlaylist:
        """
        Updates an object in the database
        :session: a SQLAlchemy Session object that is connected to the database
        :db_object: an object of type ModelType from the database
        :object_in: a pydantic model object of type CreateSchemaType
        """
        # TODO once we know what the data coming from the api endpoint looks like


user_playlist = CRUDUserPlaylist(UserPlaylist)
