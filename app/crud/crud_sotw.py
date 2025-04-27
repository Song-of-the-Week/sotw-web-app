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
    def add_next_theme_to_sotw(
        self, session: Session, *, sotw_id: int, theme: str, theme_description: str
    ) -> Sotw:
        """
        Adds a theme to the sotw.

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            sotw_id (int): The sotw ID of the Sotw being sought after.
            theme (str): The theme to add to the sotw.
            theme_description (str): The description of the theme.

        Returns:
            Sotw: The updated sotw object.
        """
        db_object = self.get(session=session, id=sotw_id)
        db_object.theme = theme
        db_object.theme_description = theme_description

        session.commit()

        return db_object
    def pop_theme_from_sotw(
        self, session: Session, *, sotw_id: int
    ) -> Sotw:
        """
        Pops the theme from the sotw.

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            sotw_id (int): The sotw ID of the Sotw being sought after.

        Returns:
            Sotw: The updated sotw object.
        """
        db_object = self.get(session=session, id=sotw_id)
        db_object.next_theme = None
        db_object.next_theme_description = None

        session.commit()

        return db_object


sotw = CRUDSotw(Sotw)
