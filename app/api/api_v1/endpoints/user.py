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


router = APIRouter()


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    session: Session = Depends(deps.get_session),
    *,
    user_id: int,
    payload: schemas.UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Fetch the current logged in user
    """
    if user_id != current_user.id or not current_user.is_superuser:
        raise HTTPException(status_code=403, detail=f"Not authorized to update")

    user = crud.user.get(session=session, id=user_id)

    return crud.user.update(session=session, db_object=user, object_in=payload)


@router.delete(
    "/{user_id}",
    response_model=schemas.User,
)
async def delete_user(
    session: Session = Depends(deps.get_session),
    *,
    user_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    if user_id != current_user.id or not current_user.is_superuser:
        raise HTTPException(status_code=403, detail=f"Not authorized to delete")

    return crud.user.delete(session=session, id=user_id)
