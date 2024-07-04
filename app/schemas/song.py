from datetime import datetime

from pydantic import ConfigDict

from app.schemas.base import Base


class SongBase(Base):
    spotify_uri: str


# properties to receive via API creation
class SongCreate(SongBase):
    name: str
    spotify_link: str
    submitter_id: int


# properties to receive via API update
class SongUpdate(SongBase): ...


# properties shared by models stored in DB
class SongInDBBase(SongBase):
    id: int = None
    model_config = ConfigDict(from_attributes=True)


# additional properties stored in DB bt not returned by API
class SongInDB(SongInDBBase): ...


# additional properties to return via API
class Song(SongInDBBase): ...
