from typing import Any, Union

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from app import crud
from app import schemas
from app.api import deps
from app.models.user import User


router = APIRouter()


@router.get(
    "/{sotw_id}/{week_num}",
    response_model=Union[schemas.Results, schemas.ResultsErrorResponse],
)
async def get_results(
    session: Session = Depends(deps.get_session),
    *,
    sotw_id: int,
    week_num: int,
    current_user: User = Depends(deps.get_current_user),
) -> schemas.Results:
    """
    Get the results for the given week of the given sotw.

    Args:
        sotw_id (int): ID of the sotw to query
        week_num (int): Number of the week for which the results are sought.
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users

    Returns:
        schemas.Results: The results for the given sotw and week num.
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
            detail=f"Week {week_num} not found for sotw {sotw.id}.",
        )

    # get the results from the given week and sotw
    results = crud.results.get_results_by_week(
        session=session, week_id=week.id, sotw_id=sotw.id
    )

    if results is None:
        return schemas.ResultsErrorResponse(
            message=f"Results for week {week_num} for {sotw.name} not yet available.",
            release_time=week.next_results_release,
        )

    return results
