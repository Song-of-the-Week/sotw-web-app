from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from loguru import logger
from jose import jwt

from app import crud
from app import schemas
from app.api import deps
from app.core.auth import create_access_token
from app.models.user import User
from app.models.sotw import Sotw
from app.shared.config import cfg


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
async def get_sotw(
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


@router.get("/{sotw_id}/invite", response_model=schemas.SotwInvite)
async def get_sotw_invite_link(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Generate a link for sharing the sotw

    Args:
        sotw_id (int): ID of the sotw to share
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

    # create token for sharing
    share_token = create_access_token(
        sub=sotw.id, lifetime=cfg.SHARE_TOKEN_EXPIRE_MINUTES
    )

    invite_url = cfg.INVITE_LINK_URL + share_token

    return schemas.SotwInvite(url=invite_url)


@router.get("/invite/pending/{share_token}", response_model=schemas.SotwInfo)
async def get_sotw_invite_pending(
    session: Session = Depends(deps.get_session),
    *,
    share_token: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get the basic info from the sotw

    Args:
        share_token (int): JWT token with the sotw id for the user to get the name from
        session (Session, optional): Sqlalchemy db session for db operations. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users

    Returns:
        Any: the sotw object retreived
    """
    # decode the token
    payload = jwt.decode(
        share_token,
        cfg.JWT_SECRET,
        algorithms=[cfg.ALGORITHM],
        options={"verify_aud": False},
    )
    sotw_id: int = payload.get("sub")

    sotw = crud.sotw.get(session=session, id=sotw_id)

    if sotw is None:
        raise HTTPException(
            status_code=404, detail=f"Sotw with given id {sotw_id} not found."
        )
    # don't worry about if the user's already in the sotw
    if current_user in sotw.user_list:
        return schemas.SotwInfo()

    return schemas.SotwInfo(name=sotw.name)


@router.get("/invite/join/{share_token}", response_model=schemas.SotwInfo)
async def get_sotw_invite_join(
    session: Session = Depends(deps.get_session),
    *,
    share_token: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Join a sotw from the share_token

    Args:
        share_token (int): JWT token with the sotw id for the user to join
        session (Session, optional): Sqlalchemy db session for db operations. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users

    Returns:
        Any: The id of the sotw object to be joined
    """
    # decode the token
    payload = jwt.decode(
        share_token,
        cfg.JWT_SECRET,
        algorithms=[cfg.ALGORITHM],
        options={"verify_aud": False},
    )
    sotw_id: int = payload.get("sub")

    sotw = crud.sotw.get(session=session, id=sotw_id)

    if sotw is None:
        raise HTTPException(
            status_code=404, detail=f"Sotw with given id {sotw_id} not found."
        )
    # don't worry about if the user's already in the sotw
    if current_user in sotw.user_list:
        schemas.SotwInfo(id=sotw.id)

    # add current user to the sotw
    crud.user.add_user_to_sotw(session=session, db_object=current_user, object_in=sotw)

    return schemas.SotwInfo(id=sotw.id)
