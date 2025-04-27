from datetime import datetime
from typing import List

from pydantic import ConfigDict

from app.schemas.base import Base


class WeekBase(Base):
    id: str
    week_num: int
    playlist_link: str
    sotw_id: int


# properties to receive via API creation
class WeekCreate(WeekBase):
    next_results_release: int
    responses: List[int] = []
    survey: str = ""
    theme: str = None
    theme_description: str = None


# properties to receive via API update
class WeekUpdate(WeekBase): ...


# properties shared by models stored in DB
class WeekInDBBase(WeekBase):
    id: str = None
    model_config = ConfigDict(from_attributes=True)


# additional properties stored in DB bt not returned by API
class WeekInDB(WeekInDBBase): ...


# additional properties to return via API
class Week(WeekInDBBase):
    sotw_id: str
    week_num: int
    playlist_link: str
    next_results_release: int
    survey: str
    submitted: bool
    theme: str = ""
    theme_description: str = ""


class WeekErrorResponse(Base):
    week: Week
    status: int
    message: str
