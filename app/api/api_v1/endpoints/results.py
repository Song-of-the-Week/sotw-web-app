from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from app import crud
from app import schemas
from app.api import deps
from app.models.user import User


router = APIRouter()


@router.get("/{sotw_id}/{week_num}", response_model=schemas.Results)
async def get_results(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    week_num: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Get the results for the given week of the given sotw

    Args:
        sotw_id (int): ID of the sotw to query
        week_num (int): number of the week for which the results are sought
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

    # get the week from the number given
    week = crud.week.get_week_by_number(
        session=session, week_num=week_num, sotw_id=sotw.id
    )

    if week is None:
        raise HTTPException(
            status_code=404,
            detail=f"Results for week {week_num} not found for sotw {sotw.id}.",
        )

    # get the results from the given week and sotw
    results = crud.results.get_results_by_week(
        session=session, week_id=week.id, sotw_id=sotw.id
    )

    return results
