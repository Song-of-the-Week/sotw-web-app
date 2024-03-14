from datetime import datetime
from typing import List
from pydantic import HttpUrl

from app.schemas.base import Base


class WeekBase(Base):
    week_num: int
    playlist_link: HttpUrl
    sotw_id: int


# properties to receive via API creation
class WeekCreate(WeekBase):
    sotw_id: int
    survey_release: datetime
    results_release: datetime
    responses: List[int] = []


# properties to receive via API update
class WeekUpdate(WeekBase): ...


# properties shared by models stored in DB
class WeekInDBBase(WeekBase):
    id: int = None

    class Config:
        from_attributes = True


# additional properties stored in DB bt not returned by API
class WeekInDB(WeekInDBBase): ...


# additional properties to return via API
class Week(WeekInDBBase):
    survey_release: datetime
    results_release: datetime
    responses: List[int]
