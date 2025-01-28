from typing import Optional

from sqlalchemy.orm import Session
from app import crud
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
        submitter_id: str
    ) -> Optional[Response]:
        current_week = crud.week.get_current_week(session=session, sotw_id=sotw_id)
        
        response = session.query(Response).filter(
            Response.sotw_id == sotw_id,
            Response.submitter_id == submitter_id,
            Response.week_id == current_week.id
        ).first()
        response.submitter_id = str(response.submitter_id)
        return response



response = CRUDResponse(Response)
