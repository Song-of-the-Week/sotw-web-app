from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.week import Week
from app.schemas.week import WeekCreate
from app.schemas.week import WeekUpdate


class CRUDWeek(CRUDBase[Week, WeekCreate, WeekUpdate]):
    def get_by_sotw_id(self, session: Session, *, sotw_id: int) -> Optional[Week]:
        """
        Session query to get all the weeks in a sotw
        :session: a SQLAlchemy Session object that is connected to the database
        :sotw_id: the sotw id of the Weeks being sought after
        """
        return session.query(Week).filter(Week.sotw_id == sotw_id).all()

    def get_current_week(self, session: Session, *, sotw_id: int) -> Optional[Week]:
        """
        Session query to get the current week from a sotw
        :session: a SQLAlchemy Session object that is connected to the database
        :sotw_id: the sotw id of the Week being sought after
        """
        return (
            session.query(func.max(Week.week_num))
            .filter(Week.sotw_id == sotw_id)
            .first()
        )

    def _get_current_week_num(
        self, session: Session, *, sotw_id: int
    ) -> Optional[Week]:
        """
        Session query to get the current week from a sotw
        :session: a SQLAlchemy Session object that is connected to the database
        :sotw_id: the sotw id of the Week being sought after
        """
        current_week = self.get_current_week(session, sotw_id=sotw_id)

        if current_week:
            return current_week.week_num
        else:
            return 0

    def create(self, session: Session, *, object_in: WeekCreate) -> Week:
        """
        Creates a Week object in the database and creates a spotify playlist for the
        object as well as instatiates the datetime fields in the object
        :session: a SQLAlchemy Session object that is connected to the database
        :object_in: a pydantic model WeekCreate object
        """
        db_object = Week(**object_in.model_dump())

        # get this week's number
        db_object = self._get_current_week_num(session, sotw_id=WeekCreate.sotw_id) + 1

        today = datetime.today()
        # calculate next wednesday
        wed_td = timedelta((10 - today.isoweekday()) % 7)
        if wed_td == 0 and today > today.replace(hour=9):
            wed_td = 7
        next_wed = (today + wed_td).replace(hour=9, minute=0, second=0, microsecond=0)
        db_object.survey_release = next_wed

        # calculate next friday
        fri_td = timedelta((12 - today.isoweekday()) % 7)
        if fri_td == 0 and today > today.replace(hour=9):
            fri_td = 7
        next_fri = (today + fri_td).replace(hour=9, minute=0, second=0, microsecond=0)
        db_object.results_release = next_fri

        # TODO fill in spotify api stuff to create a playlist for this new user and add the link to the new object
        db_object.playlist_link = ""
        session.add(db_object)
        session.commit()


week = CRUDWeek(Week)
