from datetime import datetime
from typing import Optional

from pydantic import ConfigDict

from app.schemas.base import Base


class SotwBase(Base):
    master_playlist_link: str = ""
    master_playlist_id: str = ""
    soty_playlist_link: str = ""
    soty_playlist_id: str = ""


# properties to receive via API creation
class SotwCreate(SotwBase):
    name: str
    created_at: datetime = datetime.now()
    owner_id: Optional[int] = None
    results_datetime: int
    results_timezone: str


# properties to receive via API update
class SotwUpdate(Base):
    name: Optional[str] = None
    results_datetime: Optional[int] = None
    results_timezone: Optional[str] = None

class SotwUpdateTheme(Base):
    theme: Optional[str] = None
    theme_description: Optional[str] = None

# properties shared by models stored in DB
class SotwInDBBase(SotwBase):
    id: int = None
    model_config = ConfigDict(from_attributes=True)


# additional properties stored in DB bt not returned by API
class SotwInDB(SotwInDBBase): ...


# additional properties to return via API
class Sotw(SotwInDBBase):
    id: str
    name: str
    created_at: datetime
    owner_id: str
    results_datetime: int
    results_timezone: str


# invite link
class SotwInvite(Base):
    url: str


# info to give to invitees
class SotwInfo(Base):
    id: Optional[str] = ""
    name: Optional[str] = ""
    already_in: Optional[bool] = False
