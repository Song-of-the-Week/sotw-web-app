from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.response import Response
from app.schemas.response import ResponseCreate
from app.schemas.response import ResponseUpdate


class CRUDResponse(CRUDBase[Response, ResponseCreate, ResponseUpdate]):
    ...

    # def create(self, session: Session, *, object_in: ResponseCreate) -> Response:
    #     """
    #     Creates a Response in the database
    #     :session: a SQLAlchemy Session object that is connected to the database
    #     :object_in: a pydantic model ResponseCreate object
    #     """
    #     # TODO once we know what the data coming from the api endpoint looks like

    # def update(
    #     self, session: Session, *, db_object: Response, object_in: ResponseUpdate
    # ) -> Response:
    #     """
    #     Updates an object in the database
    #     :session: a SQLAlchemy Session object that is connected to the database
    #     :db_object: an object of type ModelType from the database
    #     :object_in: a pydantic model object of type CreateSchemaType
    #     """
    #     # TODO once we know what the data coming from the api endpoint looks like


response = CRUDResponse(Response)
