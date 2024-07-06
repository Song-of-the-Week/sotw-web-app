from datetime import datetime, timedelta
from typing import Optional

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.results import Results
from app.schemas.results import ResultsCreate
from app.schemas.results import ResultsUpdate


class CRUDResults(CRUDBase[Results, ResultsCreate, ResultsUpdate]):
    def get_results_by_week(
        self, session: Session, *, week_id: int, sotw_id: int
    ) -> Optional[Results]:
        """
        Retrieve the results object with the corresponding week id and sotw id

        Args:
            session (Session): a SQLAlchemy Session object that is connected to the database
            week_id (int): the ID of the week for which the results are being sought
            sotw_id (int): the ID of the sotw for which the results are being sought

        Returns:
            Optional[Results]: a results object
        """
        return (
            session.query(Results)
            .filter(and_(Results.week_id == week_id, Results.sotw_id == sotw_id))
            .scalar()
        )


results = CRUDResults(Results)
