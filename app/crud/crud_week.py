from typing import List, Optional
from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from loguru import logger

from app.crud.crud_base import CRUDBase
from app.models.response import Response
from app.models.week import Week
from app.schemas.week import WeekCreate
from app.schemas.week import WeekUpdate


class CRUDWeek(CRUDBase[Week, WeekCreate, WeekUpdate]):
    def get_by_sotw_id(self, session: Session, *, sotw_id: int) -> Optional[List[Week]]:
        """
        Get all the weeks in a sotw.

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            sotw_id (int): The sotw ID of the Weeks being sought after.

        Returns:
            Optional[List[Week]]: A list of week model objects for the given sotw.
        """
        return session.query(Week).filter(Week.sotw_id == sotw_id).all()

    def get_current_week(self, session: Session, *, sotw_id: int) -> Optional[Week]:
        """
        Session query to get the current week from a sotw

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            sotw_id (int): The sotw ID of the Week being sought after.

        Returns:
            Optional[Week]: The latest week model object in the sotw.
        """
        sub_query = self._get_current_week_num(session=session, sotw_id=sotw_id)
        return (
            session.query(Week)
            .filter(Week.sotw_id == sotw_id, Week.week_num == sub_query)
            .one_or_none()
        )

    def _get_current_week_num(
        self, session: Session, *, sotw_id: int
    ) -> Optional[Week]:
        """
        Helper function to get the current week in a sotw.

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            sotw_id (int): The sotw ID of the Week being sought after.

        Returns:
            Optional[Week]: The week model object with the maximum week_num value for the given sotw.
        """
        return (
            session.query(func.max(Week.week_num))
            .filter(Week.sotw_id == sotw_id)
            .scalar()
        )

    def get_week_by_number(
        self, session: Session, *, week_num: int, sotw_id: int
    ) -> Optional[Week]:
        """
        Session query to get the current week from a sotw

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            week_num (int): The number of the week being sought after.
            sotw_id (int): The sotw ID of the week being sought after.

        Returns:
            Optional[Week]: The week model object with the given number for the given sotw.
        """
        return (
            session.query(Week)
            .filter(and_(Week.week_num == week_num, Week.sotw_id == sotw_id))
            .scalar()
        )

    def add_response_to_week(
        self, session: Session, *, db_object: Week, object_in: Response
    ) -> Week:
        """
        Adds the response to the week (and vice versa via model relationship)

        Args:
            session (Session): a SQLAlchemy Session object that is connected to the database.
            db_object (Week): a model object of the week to update.
            object_in (Response): A response model object.

        Returns:
            Week: The week given with the new response in it's responses list.
        """
        db_object.responses.append(object_in)
        session.add(db_object)
        session.commit()
        session.refresh(db_object)
        return db_object

    def get_all_weeks_in_sotw(self, session: Session, *, sotw_id) -> List[Week]:
        """
        Session query to get the all the weeks in a sotw

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            sotw_id (int): The sotw ID to get weeks from.

        Returns:
            List[Week]: All the weeks in the sotw with the given ID.
        """
        return session.query(Week).filter(Week.sotw_id == sotw_id).all()
    def add_theme_to_week(
        self, session: Session, *, db_object: Week, theme: str, theme_description: str
    ) -> Week:
        """
        Adds the theme to the week (and vice versa via model relationship)

        Args:
            session (Session): a SQLAlchemy Session object that is connected to the database.
            db_object (Week): a model object of the week to update.
            theme (str): The theme to add to the week.

        Returns:
            Week: The week given with the new theme in it's theme attribute.
        """
        db_object.theme = theme
        db_object.theme_description = theme_description
        session.add(db_object)
        session.commit()
        session.refresh(db_object)
        return db_object
    


week = CRUDWeek(Week)
