from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.sotw import Sotw
from app.schemas.sotw import SotwCreate
from app.schemas.sotw import SotwUpdate


class CRUDSotw(CRUDBase[Sotw, SotwCreate, SotwUpdate]):
    def create(self, session: Session, *, object_in: SotwCreate) -> Sotw:
        """
        Creates a Sotw object in the database and creates a spotify playlist for the
        object as well as instatiates the datetime fields in the object
        :session: a SQLAlchemy Session object that is connected to the database
        :object_in: a pydantic model SotwCreate object
        """
        db_object = Sotw(**object_in.model_dump())

        # TODO fill in spotify api stuff to create a playlist for this new user and add the link to the new object
        db_object.playlist_link = ""
        session.add(db_object)
        session.commit()


sotw = CRUDSotw(Sotw)
