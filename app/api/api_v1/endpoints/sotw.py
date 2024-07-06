from datetime import datetime
from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm.session import Session
from loguru import logger
from jose import JWTError, jwt

from app import crud
from app import schemas
from app.api import deps
from app.clients.spotify import SpotifyClient
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
    spotify_client: SpotifyClient = Depends(deps.get_spotify_client),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    if not current_user.spotify_linked:
        raise HTTPException(
            status_code=406,
            detail=f"You must link your spotify account from your profile page in order to create a Song of the Week competition.",
        )

    # create the master playlist
    master_playlist_name = f"{payload.name} Master Playlist"
    master_playlist_description = (
        f"All the songs contained in every week of the {payload.name} song of the week."
    )
    master_playlist = spotify_client.create_playlist(
        master_playlist_name, master_playlist_description, session, current_user.id
    )
    payload.master_playlist_link = master_playlist["external_urls"]["spotify"]

    # create the master playlist
    soty_playlist_name = f"{payload.name} Song of the Year Playlist"
    soty_playlist_description = f"The winners from each week so far of the {payload.name} Song of the Week for this year."
    soty_playlist = spotify_client.create_playlist(
        soty_playlist_name, soty_playlist_description, session, current_user.id
    )
    payload.soty_playlist_link = soty_playlist["external_urls"]["spotify"]

    payload.owner_id = current_user.id

    # create the new sotw
    sotw = crud.sotw.create(session=session, object_in=payload)

    # add current user to the sotw
    crud.user.add_user_to_sotw(session=session, db_object=current_user, object_in=sotw)

    # create the user's playlist for this sotw
    user_playlist_name = (
        f"{current_user.spotify_user_id}'s {payload.name} Song of the Week Playlist"
    )
    user_playlist_description = f"All songs submitted for the {payload.name} Song of the Week for this year by {current_user.spotify_user_id}."
    user_playlist = spotify_client.create_playlist(
        user_playlist_name, user_playlist_description, session, current_user.id
    )
    user_playlist_create = schemas.UserPlaylistCreate(
        id=user_playlist["id"],
        playlist_link=user_playlist["external_urls"]["spotify"],
        sotw_id=sotw.id,
        user_id=current_user.id,
    )
    crud.user_playlist.create(session, object_in=user_playlist_create)

    return sotw


@router.get("/{sotw_id}", response_model=schemas.Sotw)
async def get_sotw(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve a sotw object from the databases

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
    share_token: str,
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
    try:
        # decode the token
        payload = jwt.decode(
            share_token,
            cfg.JWT_SECRET,
            algorithms=[cfg.ALGORITHM],
            options={"verify_aud": False},
        )
        sotw_id: int = payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=403,
            detail=f"This token is no longer valid, please ask the person who invited you to generate a new one.",
        )

    sotw = crud.sotw.get(session=session, id=sotw_id)

    if sotw is None:
        raise HTTPException(
            status_code=404, detail=f"Sotw with given id {sotw_id} not found."
        )
    # don't worry about if the user's already in the sotw
    if current_user in sotw.user_list:
        return schemas.SotwInfo(id=sotw.id, name=sotw.name, already_in=True)

    return schemas.SotwInfo(id=sotw.id, name=sotw.name)


@router.get("/invite/join/{share_token}", response_model=schemas.SotwInfo)
async def get_sotw_invite_join(
    session: Session = Depends(deps.get_session),
    *,
    share_token: str,
    spotify_client: SpotifyClient = Depends(deps.get_spotify_client),
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
    # must have spotify linked to join a sotw
    if not current_user.spotify_linked:
        raise HTTPException(
            status_code=406,
            detail=f"You must link your spotify account from your profile page in order to join a Song of the Week competition.",
        )
    try:
        # decode the token
        payload = jwt.decode(
            share_token,
            cfg.JWT_SECRET,
            algorithms=[cfg.ALGORITHM],
            options={"verify_aud": False},
        )
        sotw_id: int = payload.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=403,
            detail=f"This token is no longer valid, please ask the person who invited you to generate a new one.",
        )

    sotw = crud.sotw.get(session=session, id=sotw_id)

    if sotw is None:
        raise HTTPException(
            status_code=404, detail=f"Sotw with given id {sotw_id} not found."
        )

    # add current user to the sotw
    crud.user.add_user_to_sotw(session=session, db_object=current_user, object_in=sotw)

    # create the user's playlist for this sotw
    user_playlist_name = (
        f"{current_user.spotify_user_id}'s {sotw.name} Song of the Week Playlist"
    )
    user_playlist_description = f"All songs submitted for the {sotw.name} Song of the Week for this year by {current_user.spotify_user_id}."
    user_playlist = spotify_client.create_playlist(
        user_playlist_name, user_playlist_description, session, current_user.id
    )
    user_playlist_create = schemas.UserPlaylistCreate(
        id=user_playlist["id"],
        playlist_link=user_playlist["external_urls"]["spotify"],
        sotw_id=sotw.id,
        user_id=current_user.id,
    )
    crud.user_playlist.create(session, object_in=user_playlist_create)

    return schemas.SotwInfo(id=sotw.id)
