from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
from loguru import logger

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
        Session query to get the current week from a sotw
        :session: a SQLAlchemy Session object that is connected to the database
        :sotw_id: the sotw id of the Week being sought after
        """
        return (
            session.query(func.max(Week.week_num))
            .filter(Week.sotw_id == sotw_id)
            .scalar()
        )


week = CRUDWeek(Week)
