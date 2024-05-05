from datetime import datetime
from typing import Optional

from app.schemas.base import Base


class SotwBase(Base):
    playlist_link: str = "https://www.spotify.com/"


# properties to receive via API creation
class SotwCreate(SotwBase):
    name: str
    created_at: datetime = datetime.now()
    survey_datetime: datetime
    results_datetime: datetime


# properties to receive via API update
class SotwUpdate(SotwBase): ...


# properties shared by models stored in DB
class SotwInDBBase(SotwBase):
    id: int = None

    class Config:
        from_attributes = True


# additional properties stored in DB bt not returned by API
class SotwInDB(SotwInDBBase): ...


# additional properties to return via API
class Sotw(SotwInDBBase):
    name: str
    created_at: datetime
    survey_datetime: datetime
    results_datetime: datetime
    share_id: str


# invite link
class SotwInvite(Base):
    url: str


# info to give to invitees
class SotwInfo(Base):
    id: Optional[int]
    name: Optional[str]
