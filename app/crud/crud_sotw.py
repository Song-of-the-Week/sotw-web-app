from datetime import datetime, timedelta
import random
import string
from sqlalchemy.orm import Session
from loguru import logger

from app.crud.crud_base import CRUDBase
from app.models.sotw import Sotw
from app.schemas.sotw import SotwCreate
from app.schemas.sotw import SotwUpdate
from app.shared.config import cfg


class CRUDSotw(CRUDBase[Sotw, SotwCreate, SotwUpdate]):
    def create(self, session: Session, *, object_in: SotwCreate) -> Sotw:
        """
        Creates a Sotw object in the database.

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            object_in (SotwCreate): A pydantic model to create the sotw with.

        Returns:
            Sotw: Newly created sotw object.
        """
        db_object = Sotw(**object_in.model_dump())

        session.add(db_object)
        session.commit()

        return db_object

sotw = CRUDSotw(Sotw)
