from datetime import datetime
from typing import List
from pydantic import HttpUrl

from app.schemas.base import Base


class SotwBase(Base):
    name: str
    playlist_link: HttpUrl
    created_at: datetime


# properties to receive via API creation
class SotwCreate(SotwBase):
    name: str


# properties to receive via API update
class SotwUpdate(SotwBase):
    ...


# properties shared by models stored in DB
class SotwInDBBase(SotwBase):
    id: int = None

    class Config:
        orm_mode = True


# additional properties stored in DB bt not returned by API
class SotwInDB(SotwInDBBase):
    user_list: List[int]


# additional properties to return via API
class Sotw(SotwInDBBase):
    ...