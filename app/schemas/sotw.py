from datetime import datetime
from typing import Optional

from pydantic import ConfigDict

from app.schemas.base import Base


class SotwBase(Base):
    master_playlist_link: str = "https://www.spotify.com/"
    soty_playlist_link: str = "https://www.spotify.com/"


# properties to receive via API creation
class SotwCreate(SotwBase):
    name: str
    created_at: datetime = datetime.now()
    owner_id: Optional[int] = None
    results_datetime: int


# properties to receive via API update
class SotwUpdate(SotwBase): ...


# properties shared by models stored in DB
class SotwInDBBase(SotwBase):
    id: int = None
    model_config = ConfigDict(from_attributes=True)


# additional properties stored in DB bt not returned by API
class SotwInDB(SotwInDBBase): ...


# additional properties to return via API
class Sotw(SotwInDBBase):
    id: int
    name: str
    created_at: datetime
    owner_id: int
    results_datetime: int


# invite link
class SotwInvite(Base):
    url: str


# info to give to invitees
class SotwInfo(Base):
    id: Optional[int] = 0
    name: Optional[str] = ""
    already_in: Optional[bool] = False
