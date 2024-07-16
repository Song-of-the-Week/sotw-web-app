from app.crud.crud_base import CRUDBase
from app.models.response import Response
from app.schemas.response import ResponseCreate
from app.schemas.response import ResponseUpdate


class CRUDResponse(CRUDBase[Response, ResponseCreate, ResponseUpdate]): ...


response = CRUDResponse(Response)
