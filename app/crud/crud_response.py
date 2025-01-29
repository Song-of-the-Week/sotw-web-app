from typing import Optional

from sqlalchemy.orm import Session
from app.crud.crud_base import CRUDBase
from app.models.response import Response
from app.schemas.response import ResponseCreate
from app.schemas.response import ResponseUpdate


class CRUDResponse(CRUDBase[Response, ResponseCreate, ResponseUpdate]):
    def get_by_sotw_and_submitter(
        self, 
        session: Session, 
        *, 
        sotw_id: int, 
        submitter_id: int,
        week_id: int
    ) -> Optional[Response]:
        """
        Retrieve the response object with the corresponding sotw id and submitter id

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            sotw_id (int): The ID of the sotw for which the response is being sought.
            submitter_id (int): The ID of the user for which the response is being sought.
            week_id (int): The ID of the week for which the response is being sought.

        Returns:
            Optional[Response]: A response model object.
        """        
        response = session.query(Response).filter(
            Response.sotw_id == sotw_id,
            Response.submitter_id == submitter_id,
            Response.week_id == week_id
        ).first()
        return response



response = CRUDResponse(Response)
