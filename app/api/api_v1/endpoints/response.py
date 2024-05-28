from datetime import datetime
import json
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


@router.post("/{sotw_id}/{week_num}", response_model=schemas.Week)
async def post_survey_response(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    week_num: int,
    payload: schemas.ResponsePost,
    current_user: User = Depends(deps.get_current_user),
    spotify_client: SpotifyClient = Depends(deps.get_spotify_client)
) -> Any:
    """
    Retrieve the current week for the sotw with the sotw id given.

    Args:
        sotw_id (int): ID of the sotw to retreive
        week_num (int): The week number for which this response was sent
        session (Session, optional): Sqlalchemy db session for db operations. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users

    Returns:
        Any: 200 response
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
            status_code=417,
            detail=f"Survey responses can only be sent for the current week.",
        )

    if week_num == 0:
        # payload is the following structure
        """
        payload = {
            next_song: "www.spotify.com",
          };
        class ResponseCreate(ResponseBase):
            next_song: Song
            sotw_id: int
            week_id: int
            submitter_id: int
        class SongCreate(SongBase):
            name: str
            spotify_link: str
            submitter_id: int
            response_id: int
            week_id: datetime
        """
        # TODO create spotify client
        pass
    else:
        # payload is the following structure
        """payload = {
            picked_song_1: 0,
            picked_song_2: 1,
            matched_user_songs: [
                {
                    song_id: song.id,
                    user_id: user.id,
                },
            ],
            next_song: "www.spotify.com",
          };
        """
        
        pass

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
        # TODO create spotify playlist for this next week with the responses from `current_week`
        playlist_link = ""
        # create survey object with the responses from `current_week`
        survey = {
            "songs": [],
            "users": [],
        }
        current_week.responses.shuffle()
        for response in current_week.responses:
            survey["songs"].append(
                {
                    "id": response.next_song.id,
                    "name": response.next_song.name,
                }
            )
        current_week.responses.shuffle()
        for response in current_week.responses:
            survey["users"].append(
                {
                    "id": response.submitter_id,
                    "name": response.submitter.name,
                    "matched": False,
                }
            )

        # create the new week
        next_week = schemas.WeekCreate(
            id=f"{sotw.id} + {current_week.next_results_release}",
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
