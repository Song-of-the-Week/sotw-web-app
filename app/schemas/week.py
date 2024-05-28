from datetime import datetime
from typing import List

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


# properties to receive via API update
class WeekUpdate(WeekBase): ...


# properties shared by models stored in DB
class WeekInDBBase(WeekBase):
    id: str = None

    class Config:
        from_attributes = True


# additional properties stored in DB bt not returned by API
class WeekInDB(WeekInDBBase): ...


# additional properties to return via API
class Week(WeekInDBBase):
    week_num: int
    playlist_link: str
    next_results_release: int
    survey: str
