from datetime import datetime
from pydantic import HttpUrl

from app.schemas.base import Base

class SongBase(Base):
    spotify_link: HttpUrl


# properties to receive via API creation
class SongCreate(SongBase):
    spotify_link: HttpUrl
    submitter_id: int
    response_id: int
    week_id: datetime


# properties to receive via API update
class SongUpdate(SongBase):
    ...


# properties shared by models stored in DB
class SongInDBBase(SongBase):
    id: int = None

    class Config:
        orm_mode = True


# additional properties stored in DB bt not returned by API
class SongInDB(SongInDBBase):
    ...


# additional properties to return via API
class Song(SongInDBBase):
    ...