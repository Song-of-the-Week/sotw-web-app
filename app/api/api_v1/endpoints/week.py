from datetime import datetime
import json
import random
from typing import Union
from zoneinfo import ZoneInfo

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from app import crud
from app import schemas
from app.api import deps
from app.clients.spotify import SpotifyClient
from app.models.sotw import Sotw
from app.models.user import User
from app.models.week import Week
from app.shared.utils import get_next_datetime


router = APIRouter()


@router.get(
    "/{sotw_id}/current_week",
    response_model=Union[schemas.Week, schemas.WeekErrorResponse],
)
async def get_current_week(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    spotify_client: SpotifyClient = Depends(deps.get_spotify_client),
    current_user: User = Depends(deps.get_current_user),
) -> schemas.Week:
    """
    Retrieve the current week for the sotw with the sotw id given.

    Args:
        sotw_id (int): ID of the sotw to retreive
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        spotify_client (SpotifyClient, optional): Client to communicate with spotify api.
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users.

    Returns:
        schemas.Week: the week object retreived - the current week for the given sotw.
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

    submitted = False
    if current_week is not None:
        for response in current_week.responses:
            if current_user.id == response.submitter_id:
                submitted = True
                break

    # check to see if we need a new week
    if not current_week:
        current_week = create_week_zero(sotw, session)
    elif datetime.now().timestamp() * 1000 >= current_week.next_results_release:
        no_new_week = do_not_create_new_week(sotw, current_week, submitted, session)
        if no_new_week:
            return no_new_week

        # create the results for the previous week and update user playlists
        if current_week.week_num >= 1:
            create_results(sotw, current_week, session, spotify_client)

        # get the next results release timestamp
        results_datetime = datetime.fromtimestamp(
            sotw.results_datetime / 1000.0, tz=ZoneInfo(sotw.results_timezone)
        )
        next_results_release = get_next_datetime(
            target_day=results_datetime.weekday(),
            target_hour=results_datetime.hour,
            target_minute=results_datetime.minute,
            timezone=sotw.results_timezone,
        )

        responses, playlist_link = create_weekly_playlist(
            sotw, current_week, spotify_client, session
        )

        survey = create_survey(responses)

        # create the new week
        next_week = schemas.WeekCreate(
            id=f"{sotw.id}+{current_week.next_results_release}",
            week_num=current_week.week_num + 1,
            playlist_link=playlist_link,
            sotw_id=sotw.id,
            next_results_release=next_results_release,
            survey=json.dumps(survey),
            responses=[],
        )
        if sotw.next_theme:
            next_week.theme = sotw.next_theme
            next_week.theme_description = sotw.next_theme_description

        # create the new current week
        current_week = crud.week.create(session=session, object_in=next_week)

        # remove the theme from the sotw
        crud.sotw.pop_theme_from_sotw(session=session, sotw_id=sotw_id)

        # user has not submitted for this new week
        submitted = False

    return schemas.Week(
        id=current_week.id,
        sotw_id=str(current_week.sotw_id),
        week_num=current_week.week_num,
        playlist_link=current_week.playlist_link,
        next_results_release=current_week.next_results_release,
        survey=current_week.survey,
        submitted=submitted,
        theme=current_week.theme or "",
        theme_description=current_week.theme_description or "",
    )

# @router.put("/{sotw_id}/add_theme",
#             response_model=Union[schemas.Week, schemas.WeekErrorResponse])
# async def add_theme(
#     session: Session = Depends(deps.get_session),
#     *,
#     sotw_id: int,
#     theme: str,
#     current_user: User = Depends(deps.get_current_user),
# ) -> schemas.Week:
#     """
#     Add a theme to the current week of the sotw.

#     Args:
#         sotw_id (int): ID of the sotw to add a theme to
#         session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
#         theme (str): The theme to add to the current week.
#         current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

#     Raises:
#         HTTPException: 403 for unauthorized users.

#     Returns:
#         schemas.Week: The week object with the new theme added.
#     """
#     # get the sotw and check permissions
#     sotw = crud.sotw.get(session=session, id=sotw_id)

#     if sotw is None:
#         raise HTTPException(
#             status_code=404, detail=f"Sotw with given id {sotw_id} not found."
#         )
#     if current_user not in sotw.user_list:
#         raise HTTPException(status_code=403, detail=f"Not authorized.")

#     # query to find out what the current week is
#     current_week = crud.week.get_current_week(session=session, sotw_id=sotw.id)

#     if current_week is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"Could not find a current week for sotw {sotw.id}.",
#         )

#     # add the theme to the current week
#     return crud.week.add_theme_to_week(session=session, db_object=current_week, theme=theme)

def create_week_zero(sotw: Sotw, session: Session):
    """
    Create week zero for sotw.

    Args:
        sotw (Sotw): Sotw model object.
        session (Session): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).

    Returns:
        schemas.Week: A week object for week 0 of a sotw competition.
    """
    results_datetime = datetime.fromtimestamp(
        sotw.results_datetime / 1000.0, tz=ZoneInfo(sotw.results_timezone)
    )
    next_results_release = get_next_datetime(
        target_day=results_datetime.weekday(),
        target_hour=results_datetime.hour,
        target_minute=results_datetime.minute,
        timezone=sotw.results_timezone,
    )
    first_week = schemas.WeekCreate(
        id=str(sotw.id) + "+0",
        week_num=0,
        playlist_link="",
        sotw_id=sotw.id,
        next_results_release=next_results_release,
        responses=[],
    )
    # create the first week of this sotw
    return crud.week.create(session=session, object_in=first_week)


def do_not_create_new_week(
    sotw: Sotw, current_week: Week, submitted: bool, session: Session
):
    """
    Returns error responses when a new week cannot be created.

    Args:
        sotw (Sotw): Sotw model object.
        current_week (Week): Week model object representing the current week for sotw.
        submitted (bool): Flag to indicate if the user has submitted or not.
        session (Session): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).

    Returns:
        A WeekErrorResponse when a sotw does not have at least 3 players or when not everyone in a sotw has
        submitted for the current week. Otherwise, return None.
    """
    sotw_num_users = len(sotw.user_list)
    if sotw_num_users < 3:
        return schemas.WeekErrorResponse(
            week=schemas.Week(
                id=current_week.id,
                sotw_id=str(current_week.sotw_id),
                week_num=current_week.week_num,
                playlist_link=current_week.playlist_link,
                next_results_release=current_week.next_results_release,
                survey=current_week.survey,
                submitted=submitted,
            ),
            status=406,
            message=f"You will need at least three players in your Song of the Week competition in order to continue playing.",
        )
    if len(current_week.responses) < sotw_num_users:
        submitted_users = crud.user.get_submitted_users(
            session=session, week_id=current_week.id
        )
        unsubmitted_users = []
        for user in sotw.user_list:
            if user not in submitted_users:
                unsubmitted_users.append(user.name)

        if len(unsubmitted_users) == 1:
            unsubmitted_user_string = unsubmitted_users[0]
        elif len(unsubmitted_users) == 2:
            unsubmitted_user_string = (
                f"{unsubmitted_users[0]} and {unsubmitted_users[1]}"
            )
        else:
            unsubmitted_user_string = (
                ", ".join(unsubmitted_users[:-1]) + ", and " + unsubmitted_users[-1]
            )
        return schemas.WeekErrorResponse(
            week=schemas.Week(
                id=current_week.id,
                sotw_id=str(current_week.sotw_id),
                week_num=current_week.week_num,
                playlist_link=current_week.playlist_link,
                next_results_release=current_week.next_results_release,
                survey=current_week.survey,
                submitted=submitted,
            ),
            status=406,
            message=f"Please make sure everyone has submitted their surveys for the week. Looks like we're still waiting on {sotw_num_users - len(current_week.responses)} player{'s' if sotw_num_users - len(current_week.responses) > 1 else ''} to submit: {unsubmitted_user_string}",
        )

    return None


def create_results(
    sotw: Sotw, current_week: Week, session: Session, spotify_client: SpotifyClient
):
    """
    Create results for a week and adds winning songs to the song of the year playlist.

    Args:
        sotw (Sotw): Sotw model object.
        current_week (Week): Week model object representing the current week for sotw.
        session (Session): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        spotify_client (SpotifyClient, optional): Client to communicate with spotify api.

    Raises:
        HTTPException: 404 when no previous week is found.
    """
    previous_week = crud.week.get_week_by_number(
        session=session, week_num=current_week.week_num - 1, sotw_id=sotw.id
    )
    if not previous_week:
        raise HTTPException(
            status_code=404,
            detail=f"Could not find a previous week with the number {current_week.week_num - 1} for sotw {sotw.id}.",
        )

    all_songs = get_all_songs(
        sotw, current_week, previous_week, session, spotify_client
    )

    guessing_data = get_guessing_data(current_week, all_songs, session)

    first_place_names, first_place_ids, second_place_names, second_place_ids = (
        calculate_first_second_place(all_songs)
    )

    # create the results for the previous week
    results_in = schemas.ResultsCreate(
        sotw_id=sotw.id,
        week_id=current_week.id,
        first_place=json.dumps(first_place_names),
        second_place=json.dumps(second_place_names),
        all_songs=json.dumps(all_songs),
        guessing_data=json.dumps(
            sorted(
                guessing_data,
                key=lambda x: x["num_correct_guesses"],
                reverse=True,
            )
        ),
    )
    crud.results.create(session=session, object_in=results_in)

    add_songs_to_soty_playlist(
        sotw, first_place_ids, second_place_ids, session, spotify_client
    )


def get_all_songs(
    sotw: Sotw,
    current_week: Week,
    previous_week: Week,
    session: Session,
    spotify_client: SpotifyClient,
):
    """
    Get all the songs from the previous week.

    Args:
        sotw (Sotw): Sotw model object.
        current_week (Week): Week model object representing the current week for sotw.
        previous_week (Week): Week model object representing the previous week for sotw.
        session (Session): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        spotify_client (SpotifyClient, optional): Client to communicate with spotify api.

    Return:
        A dictionary of all the songs in the previous week with voting data attached.
    """
    # get all the songs for the week
    previous_week_songs = crud.song.get_songs_from_week(
        session=session, sotw_id=sotw.id, week_id=previous_week.id
    )
    all_songs = {}
    for song in previous_week_songs:
        # get the playlist for this song's submitter
        playlist = crud.user_playlist.get_playlist_for_user_for_sotw(
            session=session, user_id=song.submitter_id, sotw_id=sotw.id
        )
        # add the song to the playlist
        spotify_client.add_songs_to_playlist(
            playlist_id=playlist.playlist_id,
            uris=[f"spotify:track:{song.spotify_id}"],
            session=session,
            user_id=song.submitter_id,
        )

        # add the song to the songs list
        user = crud.user.get(session=session, id=song.submitter_id)
        all_songs[song.id] = {
            "name": song.name,
            "voters": [],
            "submitter": user.name,
            "spotify_id": song.spotify_id,
        }

    # order songs in the same order as the survey data (and thus the playlist)
    survey = json.loads(current_week.survey)

    ordered_all_songs = {
        int(song["id"]): all_songs[int(song["id"])] for song in survey["songs"]
    }

    return ordered_all_songs


def get_guessing_data(current_week: Week, all_songs: dict, session: Session):
    """
    Get the guessing data from the current week's responses for the previous week's playlist.

    Args:
        current_week (Week): Week model object representing the current week for sotw.
        all_songs (dict): Dictionary of all the songs from the previous week.
        session (Session): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).

    Return:
        A list of guessing data.
    """
    # create a mapping of song names to index in survey song list
    survey = json.loads(current_week.survey)
    song_name_order = {
        song["name"]: index for index, song in enumerate(survey["songs"])
    }

    guessing_data = []
    for response in current_week.responses:
        # fill out all_songs
        all_songs[response.picked_song_1_id]["voters"].append(response.submitter.name)
        all_songs[response.picked_song_2_id]["voters"].append(response.submitter.name)
        # fill out guessing data
        guesses = []
        for match in response.user_song_matches:
            user = crud.user.get(session=session, id=match.user_id)
            guesses.append(
                {
                    "song": all_songs[match.song_id]["name"],
                    "submitter_guess": user.name,
                    "correct": match.correct_guess,
                }
            )
        guessing_data.append(
            {
                "id": response.submitter_id,
                "name": response.submitter.name,
                "guesses": sorted(
                    guesses, key=lambda guess: song_name_order[guess["song"]]
                ),
                "num_correct_guesses": response.number_correct_matches,
            }
        )
    return guessing_data


def calculate_first_second_place(all_songs: dict):
    """
    Calculate the first and second place songs from the previous week's playlist based on voting data.

    Args:
        all_songs (dict): Dictionary of all the songs from the previous week.

    Return:
        A tuple of the first place song names, first place song ids, second place song names, and second place song ids.
    """
    first_place_names = []
    first_place_ids = []
    first_place_votes = 0
    second_place_names = []
    second_place_ids = []
    second_place_votes = 0
    for song_id in all_songs:
        num_votes = len(all_songs[song_id]["voters"])
        if num_votes == first_place_votes:
            # add first place ties
            first_place_names.append(all_songs[song_id]["name"])
            first_place_ids.append(all_songs[song_id]["spotify_id"])
        elif num_votes > first_place_votes:
            # new first place votes
            second_place_votes = first_place_votes
            first_place_votes = num_votes
            second_place_names = first_place_names
            second_place_ids = first_place_ids
            first_place_names = [all_songs[song_id]["name"]]
            first_place_ids = [all_songs[song_id]["spotify_id"]]
        elif num_votes == second_place_votes:
            # add second place ties
            second_place_names.append(all_songs[song_id]["name"])
            second_place_ids.append(all_songs[song_id]["spotify_id"])
        elif num_votes > second_place_votes:
            # new second place votes
            second_place_votes = num_votes
            second_place_names = [all_songs[song_id]["name"]]
            second_place_ids = [all_songs[song_id]["spotify_id"]]

    return first_place_names, first_place_ids, second_place_names, second_place_ids


def add_songs_to_soty_playlist(
    sotw: Sotw,
    first_place_ids: list,
    second_place_ids: list,
    session: Session,
    spotify_client: SpotifyClient,
):
    """
    Add the first (and second) place song(s) to the song of the year playlist for sotw.

    Args:
        sotw (Sotw): Sotw model object.
        first_place_ids (list): A list of the first place song ids.
        second_place_ids (list): A list of the second place song ids.
        session (Session): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        spotify_client (SpotifyClient, optional): Client to communicate with spotify api.
    """
    uris = []
    if len(first_place_ids) == 1:
        for song_id in first_place_ids + second_place_ids:
            uris.append(f"spotify:track:{song_id}")
        spotify_client.add_songs_to_playlist(
            sotw.soty_playlist_id, uris, session, sotw.owner_id
        )
    else:
        for song_id in first_place_ids:
            uris.append(f"spotify:track:{song_id}")
        spotify_client.add_songs_to_playlist(
            sotw.soty_playlist_id, uris, session, sotw.owner_id
        )


def create_weekly_playlist(
    sotw: Sotw, current_week: Week, spotify_client: SpotifyClient, session: Session
):
    """
    Create the new playlist for the new week from the current week's responses.

    Args:
        sotw (Sotw): Sotw model object.
        current_week (Week): Week model object representing the current week for sotw.
        session (Session): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        spotify_client (SpotifyClient, optional): Client to communicate with spotify api.

    Returns:
        A tuple with the responses from the current week and the playlist link for the new week's playlist
    """
    week_playlist_name = f"{sotw.name} SOTW #{current_week.week_num + 1}"
    week_playlist_description = (
        f"Week {current_week.week_num + 1} for {sotw.name} Song of the Week."
    )
    week_playlist = spotify_client.create_playlist(
        week_playlist_name, week_playlist_description, session, sotw.owner_id
    )
    playlist_link = week_playlist["external_urls"]["spotify"]
    playlist_id = week_playlist["id"]

    # add all responses from `current_week` to the new playlist
    uris = []
    responses = list(current_week.responses)
    random.shuffle(responses)
    for response in responses:
        uris.append(f"spotify:track:{response.next_song.spotify_id}")
    spotify_client.add_songs_to_playlist(playlist_id, uris, session, sotw.owner_id)
    # also add these songs to the master playlist for the sotw
    spotify_client.add_songs_to_playlist(
        sotw.master_playlist_id, uris, session, sotw.owner_id
    )

    return responses, playlist_link


def create_survey(responses: list):
    """
    Create the next week's survey dictionary using the responses from the current week.

    Args:
        responses (list): List of the current week's responses.

    Returns:
        A dictionary representing a survey for the new week.
    """
    survey = {
        "songs": [],
        "users": [],
    }
    for response in responses:
        # note: the `id` is the id of the Song object in the database
        survey["songs"].append(
            {
                "id": str(response.next_song.id),
                "name": response.next_song.name,
            }
        )
    random.shuffle(responses)
    for response in responses:
        survey["users"].append(
            {
                "id": str(response.submitter_id),
                "name": response.submitter.name,
                "matched": False,
            }
        )

    return survey
