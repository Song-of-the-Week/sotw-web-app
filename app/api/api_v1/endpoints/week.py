from datetime import datetime
import json
import random
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
from app.shared.utils import get_next_datetime


router = APIRouter()


@router.get("/{sotw_id}/current_week", response_model=schemas.Week)
async def get_current_week(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    spotify_client: SpotifyClient = Depends(deps.get_spotify_client),
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Retrieve the current week for the sotw with the sotw id given.

    Args:
        sotw_id (int): ID of the sotw to retreive
        session (Session, optional): Sqlalchemy db session for db operations. Defaults to Depends(deps.get_session).
        spotify_client (SpotifyClient, optional): Client to communicate with spotify api.
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users

    Returns:
        Any: the sotw object retreived
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
            raise HTTPException(
                status_code=417,
                detail=f"You will need at least three players in your Song of the Week competition in order to continue playing.",
            )
        if len(current_week.responses) < sotw_num_users:
            raise HTTPException(
                status_code=417,
                detail=f"Please make sure everyone has submitted their surveys for the week. Looks like we're still waiting on {sotw_num_users - len(current_week.responses)} players to submit.",
            )

        # get the next results release timestamp
        results_datetime = datetime.fromtimestamp(sotw.results_datetime / 1000.0)
        next_results_release = get_next_datetime(
            target_day=results_datetime.weekday(),
            target_hour=results_datetime.hour,
            target_minute=results_datetime.minute,
        )

        # create spotify playlist for this next week
        week_playlist_name = f"{sotw.name} SOTW #{current_week.week_num}"
        week_playlist_description = (
            f"Week {current_week.week_num} for {sotw.name} Song of the Week."
        )
        week_playlist = spotify_client.create_playlist(
            week_playlist_name, week_playlist_description, session, current_user.id
        )
        playlist_link = week_playlist["external_urls"]["spotify"]
        playlist_id = week_playlist["id"]

        # add all responses from `current_week` to the new playlist
        uris = []
        responses = list(current_week.responses)
        random.shuffle(responses)
        for response in responses:
            uris.append(response.next_song.spotify_uri)
        spotify_client.add_songs_to_playlist(
            playlist_id, uris, session, current_user.id
        )

        # create survey object with the responses from `current_week`
        survey = {
            "songs": [],
            "users": [],
        }
        random.shuffle(responses)
        for response in responses:
            survey["songs"].append(
                {
                    "id": response.next_song.id,
                    "name": response.next_song.name,
                }
            )
        random.shuffle(responses)
        for response in responses:
            survey["users"].append(
                {
                    "id": response.submitter_id,
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

    return current_week
