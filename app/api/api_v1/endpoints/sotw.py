from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from loguru import logger

from app import crud
from app import schemas
from app.api import deps
from app.models.user import User
from app.models.sotw import Sotw


router = APIRouter()


# @router.post("/", response_model=schemas.Sotw, status_code=201)
@router.post("/", status_code=201)
async def create_sotw(
    session: Session = Depends(deps.get_session),
    *,
    payload: schemas.SotwCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    logger.error(f"Successfully got the payload! {payload}")
    # TODO create the object and keep going!
    # if current_user.is_superuser:
    #     raise HTTPException(status_code=403, detail=f"Not authorized to update.")
    return {"id": 1}
