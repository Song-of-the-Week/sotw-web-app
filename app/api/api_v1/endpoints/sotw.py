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


@router.post("/", response_model=schemas.Sotw, status_code=201)
async def create_sotw(
    session: Session = Depends(deps.get_session),
    *,
    payload: schemas.SotwCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    # create sotw
    sotw = crud.sotw.create(session=session, object_in=payload)

    # add current user to the sotw
    crud.user.add_user_to_sotw(session=session, db_object=current_user, object_in=sotw)

    return sotw


@router.get("/{sotw_id}", response_model=schemas.Sotw)
async def update_user(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update the user object in the db.

    Args:
        sotw_id (int): ID of the sotw to retreive
        session (Session, optional): Sqlalchemy db session for db operations. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users

    Returns:
        Any: the sotw object retreived
    """
    sotw = crud.sotw.get(session=session, id=sotw_id)

    if sotw is None:
        raise HTTPException(
            status_code=404, detail=f"Sotw with given id {sotw_id} not found."
        )
    if current_user not in sotw.user_list:
        raise HTTPException(status_code=403, detail=f"Not authorized.")

    return sotw
