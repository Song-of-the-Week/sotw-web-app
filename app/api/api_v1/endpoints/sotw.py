from typing import Any
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from loguru import logger
from sqlalchemy.orm.session import Session
from jose import JWTError, jwt

from app import crud
from app import schemas
from app.api import deps
from app.clients.spotify import SpotifyClient
from app.core.auth import create_access_token
from app.models.sotw import Sotw
from app.models.user import User
from app.shared.config import cfg


router = APIRouter()


@router.post("/", response_model=schemas.Sotw, status_code=201)
async def create_sotw(
    session: Session = Depends(deps.get_session),
    *,
    payload: schemas.SotwCreate,
    spotify_client: SpotifyClient = Depends(deps.get_spotify_client),
    current_user: User = Depends(deps.get_current_user),
) -> schemas.Sotw:
    """
    Create a new sotw.

    Args:
        payload (schemas.SotwCreate): The details to create the sotw object with.
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        spotify_client (SpotifyClient, optional): Client for Spotify interactions. Defaults to Depends(deps.get_spotify_client).
        current_user (User, optional): Currently authenticcated user making the request. Defaults to Depends(deps.get_current_user).

    Raises:
        HTTPException: 406 when the user's Spotify has not been linked with their account.

    Returns:
        schemas.Sotw: The newly created sotw.
    """
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
    payload.master_playlist_id = master_playlist["id"]

    # create the song of the year playlist
    soty_playlist_name = f"{payload.name} Song of the Year Playlist"
    soty_playlist_description = f"The winners from each week so far of the {payload.name} Song of the Week for this year."
    soty_playlist = spotify_client.create_playlist(
        soty_playlist_name, soty_playlist_description, session, current_user.id
    )
    payload.soty_playlist_link = soty_playlist["external_urls"]["spotify"]
    payload.soty_playlist_id = soty_playlist["id"]

    payload.owner_id = current_user.id

    # create the new sotw
    sotw = crud.sotw.create(session=session, object_in=payload)

    # add current user to the sotw
    crud.user.add_user_to_sotw(session=session, db_object=current_user, object_in=sotw)

    # create the user's playlist for this sotw
    user_playlist_name = (
        f"{current_user.name}'s {payload.name} Song of the Week Playlist"
    )
    user_playlist_description = f"All songs submitted for the {payload.name} Song of the Week for this year by {current_user.name}."
    user_playlist = spotify_client.create_playlist(
        user_playlist_name, user_playlist_description, session, current_user.id
    )
    user_playlist_create = schemas.UserPlaylistCreate(
        playlist_id=user_playlist["id"],
        playlist_link=user_playlist["external_urls"]["spotify"],
        sotw_id=sotw.id,
        user_id=current_user.id,
    )
    crud.user_playlist.create(session, object_in=user_playlist_create)

    return schemas.Sotw(
        created_at=sotw.created_at,
        id=str(sotw.id),
        master_playlist_id=sotw.master_playlist_id,
        master_playlist_link=sotw.master_playlist_link,
        name=sotw.name,
        owner_id=str(sotw.owner_id),
        results_datetime=sotw.results_datetime,
        results_timezone=sotw.results_timezone,
        soty_playlist_id=sotw.soty_playlist_id,
        soty_playlist_link=sotw.soty_playlist_link,
    )

@router.put("/{sotw_id}/update_next_theme")
async def update_sotw_theme(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    sotw_update_theme: schemas.SotwUpdateTheme,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update the theme for a sotw.

    Args:
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        sotw_id (int): ID of the sotw to update
        theme (str): The new theme for the sotw.
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users

    Returns:
        Any: the updated sotw object
    """
    week = crud.week.get_current_week(session=session, sotw_id=sotw_id)
    sotw = crud.sotw.get(session=session, id=sotw_id)

    if current_user.id != sotw.owner_id:
        raise HTTPException(status_code=403, detail=f"Not authorized to update.")

    # update the theme in the database
    crud.week.add_theme_to_week(session=session, db_object=week, theme=sotw_update_theme.theme, theme_description=sotw_update_theme.theme_description)

    return {"status": 200}


@router.put("/{sotw_id}", response_model=schemas.Sotw)
async def update_sotw(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    spotify_client: SpotifyClient = Depends(deps.get_spotify_client),
    payload: schemas.SotwUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> schemas.Sotw:
    """
    Update the sotw object in the db and any related playlists.

    Args:
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        sotw_id (int): ID of the sotw to update
        spotify_client (SpotifyClient, optional): Client for Spotify interactions. Defaults to Depends(deps.get_spotify_client).
        payload (schemas.SotwUpdate): Data to update sotw with.
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users

    Returns:
        Any: the updated sotw object
    """
    sotw = crud.sotw.get(session=session, id=sotw_id)

    if current_user.id != sotw.owner_id:
        raise HTTPException(status_code=403, detail=f"Not authorized to update.")

    if payload.name or payload.results_datetime or payload.results_timezone:
        # update the sotw name in database
        sotw = crud.sotw.update(session=session, db_object=sotw, object_in=payload)

    if payload.name:
        # update playlist names
        update_master_playlist_name(session, sotw, current_user.id, spotify_client)
        update_soty_playlist_name(session, sotw, current_user.id, spotify_client)
        update_all_sotw_weeks_playlist_names(
            session, sotw, current_user.id, spotify_client
        )
        update_all_sotw_user_playlist_names(session, sotw, spotify_client)

    return schemas.Sotw(
        created_at=sotw.created_at,
        id=str(sotw.id),
        master_playlist_id=sotw.master_playlist_id,
        master_playlist_link=sotw.master_playlist_link,
        name=sotw.name,
        owner_id=str(sotw.owner_id),
        results_datetime=sotw.results_datetime,
        results_timezone=sotw.results_timezone,
        soty_playlist_id=sotw.soty_playlist_id,
        soty_playlist_link=sotw.soty_playlist_link,
    )


def update_master_playlist_name(
    session: Session, sotw: Sotw, user_id: int, spotify_client: SpotifyClient
):
    """
    Update the master playlist name for a sotw.

    Args:
        session (Session): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        sotw (Sotw): The sotw with the playlist to be updated.
        user_id (int): ID of the sotw owner.
        spotify_client (SpotifyClient): Client for Spotify interactions. Defaults to Depends(deps.get_spotify_client).
    """
    new_master_playlist_name = f"{sotw.name} Master Playlist"
    new_master_playlist_description = (
        f"All the songs contained in every week of the {sotw.name} song of the week."
    )
    spotify_client.update_playlist_details(
        sotw.master_playlist_id,
        new_master_playlist_name,
        new_master_playlist_description,
        session,
        user_id,
    )


def update_soty_playlist_name(
    session: Session, sotw: Sotw, user_id: int, spotify_client: SpotifyClient
):
    """
    Update the soty playlist name for a sotw.

    Args:
        session (Session): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        sotw (Sotw): The sotw with the playlist to be updated.
        user_id (int): ID of the sotw owner.
        spotify_client (SpotifyClient): Client for Spotify interactions. Defaults to Depends(deps.get_spotify_client).
    """
    new_soty_playlist_name = f"{sotw.name} Song of the Year Playlist"
    new_soty_playlist_description = f"The winners from each week so far of the {sotw.name} Song of the Week for this year."
    spotify_client.update_playlist_details(
        sotw.soty_playlist_id,
        new_soty_playlist_name,
        new_soty_playlist_description,
        session,
        user_id,
    )


def update_all_sotw_weeks_playlist_names(
    session: Session, sotw: Sotw, user_id: int, spotify_client: SpotifyClient
):
    """
    Update all the week playlist names for a sotw.

    Args:
        session (Session): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        sotw (Sotw): The sotw with the weeks to be updated.
        user_id (int): ID of the sotw owner.
        spotify_client (SpotifyClient): Client for Spotify interactions. Defaults to Depends(deps.get_spotify_client).
    """
    all_weeks = crud.week.get_all_weeks_in_sotw(session=session, sotw_id=sotw.id)
    for week in all_weeks:
        if week.week_num == 0:
            continue
        new_week_playlist_name = f"{sotw.name} SOTW #{week.week_num}"
        new_week_playlist_desciption = (
            f"Week {week.week_num} for {sotw.name} Song of the Week."
        )
        week_playlist_id = week.playlist_link.split("/")[-1]
        spotify_client.update_playlist_details(
            week_playlist_id,
            new_week_playlist_name,
            new_week_playlist_desciption,
            session,
            user_id,
        )


def update_all_sotw_user_playlist_names(
    session: Session, sotw: Sotw, spotify_client: SpotifyClient
):
    """
    Update all the user playlist names for a sotw's users.

    Args:
        session (Session): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        sotw (Sotw): The sotw with the users playlists to be updated.
        spotify_client (SpotifyClient): Client for Spotify interactions. Defaults to Depends(deps.get_spotify_client).
    """
    for user in sotw.user_list:
        # get the user's playlist
        user_playlist = crud.user_playlist.get_playlist_for_user_for_sotw(
            session=session, user_id=user.id, sotw_id=sotw.id
        )
        new_user_playlist_name = f"{user.name}'s {sotw.name} Song of the Week Playlist"
        new_user_playlist_description = f"All songs submitted for the {sotw.name} Song of the Week for this year by {user.name}."
        spotify_client.update_playlist_details(
            user_playlist.playlist_id,
            new_user_playlist_name,
            new_user_playlist_description,
            session,
            user.id,
        )


@router.get("/{sotw_id}", response_model=schemas.Sotw)
async def get_sotw(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> schemas.Sotw:
    """
    Retrieve a sotw object from the database.

    Args:
        sotw_id (int): ID of the sotw to retreive.
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users.

    Returns:
        schemas.Sotw: The sotw object retreived.
    """
    sotw = crud.sotw.get(session=session, id=sotw_id)

    if sotw is None:
        raise HTTPException(
            status_code=404, detail=f"Sotw with given id {sotw_id} not found."
        )
    if current_user not in sotw.user_list:
        raise HTTPException(status_code=403, detail=f"Not authorized.")

    return schemas.Sotw(
        created_at=sotw.created_at,
        id=str(sotw.id),
        master_playlist_id=sotw.master_playlist_id,
        master_playlist_link=sotw.master_playlist_link,
        name=sotw.name,
        owner_id=str(sotw.owner_id),
        results_datetime=sotw.results_datetime,
        results_timezone=sotw.results_timezone,
        soty_playlist_id=sotw.soty_playlist_id,
        soty_playlist_link=sotw.soty_playlist_link,
    )


@router.get("/{sotw_id}/invite", response_model=schemas.SotwInvite)
async def get_sotw_invite_link(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> schemas.SotwInvite:
    """
    Generate a link for sharing the sotw.

    Args:
        sotw_id (int): ID of the sotw to share.
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users.

    Returns:
        schemas.SotwInvite: The share link for the sotw.
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
) -> schemas.SotwInfo:
    """
    Intermediate step for joining a sotw.

    Args:
        share_token (int): JWT token with the sotw id for the user to get the name from
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users

    Returns:
        schemas.SotwInfo: The info for the sotw being joined.
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
        return schemas.SotwInfo(id=str(sotw.id), name=sotw.name, already_in=True)

    return schemas.SotwInfo(id=str(sotw.id), name=sotw.name)


@router.get("/invite/join/{share_token}", response_model=schemas.SotwInfo)
async def get_sotw_invite_join(
    session: Session = Depends(deps.get_session),
    *,
    share_token: str,
    spotify_client: SpotifyClient = Depends(deps.get_spotify_client),
    current_user: User = Depends(deps.get_current_user),
) -> schemas.SotwInfo:
    """
    Join a sotw from the share_token.

    Args:
        share_token (int): JWT token with the sotw id for the user to join.
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users

    Returns:
        schemas.SotwInfo: The id of the sotw object to be joined.
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

    try:
        # add current user to the sotw
        crud.user.add_user_to_sotw(
            session=session, db_object=current_user, object_in=sotw
        )

        if not crud.user_playlist.get_playlist_for_user_for_sotw(
            session=session, user_id=current_user.id, sotw_id=sotw.id
        ):
            # create the user's playlist for this sotw if it does not already exist
            user_playlist_name = (
                f"{current_user.name}'s {sotw.name} Song of the Week Playlist"
            )
            user_playlist_description = f"All songs submitted for the {sotw.name} Song of the Week for this year by {current_user.name}."
            user_playlist = spotify_client.create_playlist(
                user_playlist_name,
                user_playlist_description,
                session,
                current_user.id,
            )
            user_playlist_create = schemas.UserPlaylistCreate(
                playlist_id=user_playlist["id"],
                playlist_link=user_playlist["external_urls"]["spotify"],
                sotw_id=sotw.id,
                user_id=current_user.id,
            )
            crud.user_playlist.create(session, object_in=user_playlist_create)
    except Exception as e:
        crud.user.remove_user_from_sotw(
            session=session, db_object=current_user, object_in=sotw
        )
        raise HTTPException(status_code=400, detail=f"An error occurred: '{str(e)}'")

    return schemas.SotwInfo(id=str(sotw.id))


@router.get("/{sotw_id}/members", response_model=list[schemas.User])
async def get_sotw_members(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> list[schemas.User]:
    """
    Get the list of members for a specific SOTW.

    Args:
        sotw_id (int): ID of the sotw to get members from
        session (Session): Database session
        current_user (User): Currently authenticated user

    Raises:
        HTTPException: 404 if SOTW not found, 403 if user not authorized

    Returns:
        list[schemas.User]: List of users in the SOTW
    """
    sotw = crud.sotw.get(session=session, id=sotw_id)

    if sotw is None:
        raise HTTPException(
            status_code=404, detail=f"Sotw with given id {sotw_id} not found."
        )
    if current_user not in sotw.user_list:
        raise HTTPException(status_code=403, detail=f"Not authorized.")

    users = [
        schemas.User(
            id=str(user.id),
            email=user.email,
            name=user.name,
            is_superuser=user.is_superuser,
            spotify_linked=user.spotify_linked,
            playlists=[
                schemas.UserPlaylist(
                    id=str(playlist.id),
                    playlist_id=playlist.playlist_id,
                    playlist_link=playlist.playlist_link,
                    sotw_id=str(playlist.sotw_id),
                    user_id=str(playlist.user_id),
                )
                # make sure we're only returning the playlists for this competition
                for playlist in user.playlists
                if playlist.sotw_id == sotw_id
            ],
            # we don't need the sotw_list for members at this time
            sotw_list=[],
        )
        for user in sotw.user_list
    ]
    return users


@router.get("/{sotw_id}/leave", response_model=schemas.User)
async def get_leave_sotw(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> schemas.User:
    """
    Retrieve a sotw object from the database.

    Args:
        sotw_id (int): ID of the sotw to retreive.
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users.

    Returns:
        schemas.User: The user object after being removed from the sotw.
    """
    sotw = crud.sotw.get(session=session, id=sotw_id)

    if sotw is None:
        raise HTTPException(
            status_code=404, detail=f"Sotw with given id {sotw_id} not found."
        )
    if current_user not in sotw.user_list:
        return schemas.User(
            id=str(current_user.id),
            email=current_user.email,
            name=current_user.name,
            is_superuser=current_user.is_superuser,
            spotify_linked=current_user.spotify_linked,
            playlists=[
                schemas.UserPlaylist(
                    id=str(playlist.id),
                    playlist_id=playlist.playlist_id,
                    playlist_link=playlist.playlist_link,
                    sotw_id=str(playlist.sotw_id),
                    user_id=str(playlist.user_id),
                )
                for playlist in current_user.playlists
            ],
            sotw_list=[
                schemas.Sotw(
                    created_at=sotw.created_at,
                    id=str(sotw.id),
                    master_playlist_id=sotw.master_playlist_id,
                    master_playlist_link=sotw.master_playlist_link,
                    name=sotw.name,
                    owner_id=str(sotw.owner_id),
                    results_datetime=sotw.results_datetime,
                    results_timezone=sotw.results_timezone,
                    soty_playlist_id=sotw.soty_playlist_id,
                    soty_playlist_link=sotw.soty_playlist_link,
                )
                for sotw in current_user.sotw_list
            ],
        )

    # remove user from sotw
    crud.user.remove_user_from_sotw(
        session=session, db_object=current_user, object_in=sotw
    )

    session.refresh(current_user)
    return schemas.User(
        id=str(current_user.id),
        email=current_user.email,
        name=current_user.name,
        is_superuser=current_user.is_superuser,
        spotify_linked=current_user.spotify_linked,
        playlists=[
            schemas.UserPlaylist(
                id=str(playlist.id),
                playlist_id=playlist.playlist_id,
                playlist_link=playlist.playlist_link,
                sotw_id=str(playlist.sotw_id),
                user_id=str(playlist.user_id),
            )
            for playlist in current_user.playlists
        ],
        sotw_list=[
            schemas.Sotw(
                created_at=sotw.created_at,
                id=str(sotw.id),
                master_playlist_id=sotw.master_playlist_id,
                master_playlist_link=sotw.master_playlist_link,
                name=sotw.name,
                owner_id=str(sotw.owner_id),
                results_datetime=sotw.results_datetime,
                results_timezone=sotw.results_timezone,
                soty_playlist_id=sotw.soty_playlist_id,
                soty_playlist_link=sotw.soty_playlist_link,
            )
            for sotw in current_user.sotw_list
        ],
    )
