from datetime import datetime
import json
import random
from typing import Any, Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from loguru import logger
from sqlalchemy.orm.session import Session

from app import crud
from app import schemas
from app.api import deps
from app.clients.spotify import SpotifyClient
from app.models.user import User
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
        # create week 0
        results_datetime = datetime.fromtimestamp(sotw.results_datetime / 1000.0)
        next_results_release = get_next_datetime(
            target_day=results_datetime.weekday(),
            target_hour=results_datetime.hour,
            target_minute=results_datetime.minute,
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
        current_week = crud.week.create(session=session, object_in=first_week)
    elif datetime.now().timestamp() * 1000 >= current_week.next_results_release:
        # we have passed this week's next results release datetime, now determine if we can make a new week based on if there are enough players in the sotw competition and if each player in the sotw has submitted a response.
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
                message=f"Please make sure everyone has submitted their surveys for the week. Looks like we're still waiting on {sotw_num_users - len(current_week.responses)} player{'s' if sotw_num_users - len(current_week.responses) > 1 else ''} to submit.",
            )

        # create the results for the previous week and update user playlists
        if current_week.week_num >= 1:
            previous_week = crud.week.get_week_by_number(
                session=session, week_num=current_week.week_num - 1, sotw_id=sotw.id
            )
            if not previous_week:
                raise HTTPException(
                    status_code=404,
                    detail=f"Could not find a previous week with the number {current_week.week_num - 1} for sotw {sotw.id}.",
                )
            # get all the songs for this week
            previous_week_songs = crud.song.get_songs_from_week(
                session=session, sotw_id=sotw.id, week_id=previous_week.id
            )
            # go through each song and add them to the user's playlist and add the song to a dict for results
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

            # create results for previous week
            guessing_data = []
            for response in current_week.responses:
                # fill out all_songs
                all_songs[response.picked_song_1_id]["voters"].append(
                    response.submitter.name
                )
                all_songs[response.picked_song_2_id]["voters"].append(
                    response.submitter.name
                )
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
                        "guesses": sorted(guesses, key=lambda x: x["song"]),
                        "num_correct_guesses": response.number_correct_matches,
                    }
                )

            # calculate first and second places
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
                    first_place_votes = num_votes
                    second_place_names = first_place_names
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

            # create the results for the previous week
            results_in = schemas.ResultsCreate(
                sotw_id=sotw.id,
                week_id=current_week.id,
                first_place=json.dumps(first_place_names),
                second_place=json.dumps(second_place_names),
                all_songs=json.dumps(all_songs),
                guessing_data=json.dumps(sorted(guessing_data, key=lambda x: x["num_correct_guesses"], reverse=True),
            )
            crud.results.create(session=session, object_in=results_in)

            # add first and second place songs to the soty playlsit
            uris = []
            for song_id in first_place_ids + second_place_ids:
                uris.append(f"spotify:track:{song_id}")
            spotify_client.add_songs_to_playlist(
                sotw.soty_playlist_id, uris, session, sotw.owner_id
            )

        # get the next results release timestamp
        results_datetime = datetime.fromtimestamp(sotw.results_datetime / 1000.0)
        next_results_release = get_next_datetime(
            target_day=results_datetime.weekday(),
            target_hour=results_datetime.hour,
            target_minute=results_datetime.minute,
        )

        # create spotify playlist for this next week
        week_playlist_name = f"{sotw.name} SOTW #{current_week.week_num + 1}"
        week_playlist_description = (
            f"Week {current_week.week_num} for {sotw.name} Song of the Week."
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

        # create survey object with the responses from `current_week`
        survey = {
            "songs": [],
            "users": [],
        }
        random.shuffle(responses)
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

        # create the new current week
        current_week = crud.week.create(session=session, object_in=next_week)

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
    )
