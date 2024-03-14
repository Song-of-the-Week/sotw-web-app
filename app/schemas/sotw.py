from datetime import datetime
from typing import List
from pydantic import HttpUrl

from app.schemas.base import Base


class SotwBase(Base):
    name: str
    playlist_link: HttpUrl = "https://www.spotify.com/"
    survey_datetime: datetime
    results_datetime: datetime


# properties to receive via API creation
class SotwCreate(SotwBase):
    created_at: datetime = datetime.now()


# properties to receive via API update
class SotwUpdate(SotwBase): ...


# properties shared by models stored in DB
class SotwInDBBase(SotwBase):
    id: int = None

    class Config:
        from_attributes = True


# additional properties stored in DB bt not returned by API
class SotwInDB(SotwInDBBase):
    user_list: List[int]


# additional properties to return via API
class Sotw(SotwInDBBase): ...
