from datetime import datetime

from app.schemas.base import Base


class SongBase(Base):
    spotify_link: str


# properties to receive via API creation
class SongCreate(SongBase):
    spotify_link: str
    submitter_id: int
    response_id: int
    week_id: datetime


# properties to receive via API update
class SongUpdate(SongBase): ...


# properties shared by models stored in DB
class SongInDBBase(SongBase):
    id: int = None

    class Config:
        from_attributes = True


# additional properties stored in DB bt not returned by API
class SongInDB(SongInDBBase): ...


# additional properties to return via API
class Song(SongInDBBase): ...
