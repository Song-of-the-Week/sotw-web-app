from typing import Union
from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from requests import HTTPError
from sqlalchemy.orm.session import Session
from loguru import logger

from app import crud
from app import schemas
from app.api import deps
from app.clients.spotify import SpotifyClient
from app.models.user import User


router = APIRouter()


@router.post(
    "/{sotw_id}/{week_num}",
    response_model=schemas.ResponseResponse,
    status_code=201,
)
async def post_survey_response(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    week_num: int,
    payload: schemas.ResponsePost,
    current_user: User = Depends(deps.get_current_user),
    spotify_client: SpotifyClient = Depends(deps.get_spotify_client),
) -> schemas.ResponseResponse:
    """
    Receive and process a survey response from the front end.

    Args:
        sotw_id (int): URL param for the id of the sotw being responded to.
        week_num (int): URL param number of the week that the response is for.
        payload (schemas.ResponsePost): The answers to the survey.
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently authenticated user. Defaults to Depends(deps.get_current_user).
        spotify_client (SpotifyClient, optional): Client for Spotify interactions. Defaults to Depends(deps.get_spotify_client).

    Raises:
        HTTPException: 404 - sotw not found
        HTTPException: 403 - user not authorized
        HTTPException: 404 - week not found
        HTTPException: 406 - wrong week
        HTTPException: 400 - incorrect payload

    Returns:
        schemas.ResponseResponse: A response telling the front end if the song submitted is a repeat.s
    """
    # get the sotw and check permissions
    sotw = crud.sotw.get(session=session, id=sotw_id)

    if sotw is None:
        raise HTTPException(
            status_code=404, detail=f"Sotw with given id {sotw_id} not found."
        )
    if current_user not in sotw.user_list:
        raise HTTPException(status_code=403, detail=f"Not authorized.")

    # query to find out what the current week is
    current_week = crud.week.get_current_week(session=session, sotw_id=sotw.id)

    if not current_week:
        raise HTTPException(
            status_code=404,
            detail=f"This song of the week competition hasn't started yet!",
        )

    if current_week.week_num != week_num:
        raise HTTPException(
            status_code=406,
            detail=f"Survey responses can only be sent for the current week.",
        )

    # validate the spotify link
    next_song_track_id = payload.next_song.split("/")[-1].split("?")[0]
    try:
        song = spotify_client.get_track_info(
            next_song_track_id, session, current_user.id
        )
    except HTTPError:
        return schemas.ResponseResponse(repeat=False, valid=False)

    # check to see if current_user has submitted a response already and delete that response if so
    for response in current_week.responses:
        if current_user.id == response.submitter_id:
            # delete the song from this response
            crud.song.delete(session=session, id=response.next_song_id)
            # delete all the user song matches
            for match in response.user_song_matches:
                crud.user_song_match.delete(session=session, id=match.id)
            # delete the response
            crud.response.delete(session=session, id=response.id)

    if week_num == 0:
        # get song info and create the song in the db
        song_name = f"{song['name']} - {song['artists'][0]['name']}"
        for artist in song["artists"][1:]:
            song_name = song_name + f", {artist['name']}"

        song_in = schemas.SongCreate(
            spotify_id=next_song_track_id,
            spotify_link=payload.next_song,
            name=song_name,
            submitter_id=current_user.id,
        )

        next_song_obj = crud.song.create(session=session, object_in=song_in)

        # create response object in db
        response_in = schemas.ResponseCreate(
            next_song_id=next_song_obj.id,
            sotw_id=current_week.sotw_id,
            week_id=current_week.id,
            submitter_id=current_user.id,
        )
        response = crud.response.create(session=session, object_in=response_in)

        # add response to week
        crud.week.add_response_to_week(
            session=session, db_object=current_week, object_in=response
        )

        # return a response with the current week
        return schemas.ResponseResponse(repeat=False, valid=True)
    else:
        song_name = f"{song['name']} - {song['artists'][0]['name']}"
        for artist in song["artists"][1:]:
            song_name = song_name + f", {artist['name']}"

        # determine if this song has been submitted before:
        if (
            crud.song.get_song_by_name(
                session=session,
                name=song_name,
                sotw_id=sotw.id,
                week_id=current_week.id,
            )
            and not payload.repeat_approved
        ):
            return schemas.ResponseResponse(repeat=True, valid=True)

        song_in = schemas.SongCreate(
            spotify_id=next_song_track_id,
            spotify_link=payload.next_song,
            name=song_name,
            submitter_id=current_user.id,
        )

        next_song_obj = crud.song.create(session=session, object_in=song_in)

        # create response object in db
        response_in = schemas.ResponseCreate(
            next_song_id=next_song_obj.id,
            sotw_id=current_week.sotw_id,
            week_id=current_week.id,
            submitter_id=current_user.id,
            picked_song_1_id=payload.picked_song_1,
            picked_song_2_id=payload.picked_song_2,
        )
        response = crud.response.create(session=session, object_in=response_in)

        # create user song matches
        number_correct_matches = 0
        for match in payload.user_song_matches:
            song = crud.song.get(session=session, id=int(match.song_id))
            # the payload has some sort of error if the song can't be found
            if not song:
                raise HTTPException(
                    status_code=400,
                    detail=f"There's something wrong with your request. A song with the given id {match.song_id} does not exist.",
                )
            user_song_match_in = schemas.UserSongMatchCreate(
                song_id=int(match.song_id),
                user_id=int(match.user_id),
                correct_guess=match.user_id == song.submitter_id,
                response_id=response.id,
            )
            number_correct_matches += 1 if user_song_match_in.correct_guess else 0
            crud.user_song_match.create(session=session, object_in=user_song_match_in)

        # update the response
        session.refresh(response)
        response = crud.response.update(
            session=session,
            db_object=response,
            object_in=schemas.ResponseUpdate(
                number_correct_matches=number_correct_matches
            ),
        )

        # add response to week
        crud.week.add_response_to_week(
            session=session, db_object=current_week, object_in=response
        )

        # return a response with the current week
        return schemas.ResponseResponse(repeat=False, valid=True)
