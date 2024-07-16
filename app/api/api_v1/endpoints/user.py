from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from app import crud
from app import schemas
from app.api import deps
from app.core.auth import authenticate
from app.core.security import get_password_hash
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
    Update the user object in the db.

    Args:
        user_id (int): ID of the user to update
        payload (schemas.UserUpdate): Data to update user with
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users or for incorrect password

    Returns:
        Any: the uupdated user object
    """
    if not current_user.is_superuser and user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"Not authorized to update.")

    if payload.current_password is not None and payload.new_password is not None:
        if authenticate(
            email=current_user.email, password=payload.current_password, session=session
        ):
            payload = {"password": get_password_hash(payload.new_password)}
        else:
            raise HTTPException(status_code=403, detail=f"Incorrect password.")
    elif payload.spotify_linked == False and payload.spotify_linked != None:
        payload = {
            "spotify_linked": False,
            "spotify_access_token": None,
            "spotify_refresh_token": None,
        }

    return crud.user.update(session=session, db_object=current_user, object_in=payload)


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
    """
    Delete specified user.

    Args:
        user_id (int): ID of the user to  delete
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users.s

    Returns:
        Any: The deleted object.
    """
    if not current_user.is_superuser and user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"Not authorized to delete.")

    return crud.user.delete(session=session, id=user_id)
