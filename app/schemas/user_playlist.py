from typing import List, Optional
from pydantic import ConfigDict

from app.models.user import User
from app.schemas.base import Base


class UserPlaylistBase(Base):
    playlist_link: str


# properties to receive via API creation
class UserPlaylistCreate(UserPlaylistBase):
    playlist_link: str
    user_id: int
    sotw_id: int
    user: User


# properties to receive via API update
class UserPlaylistUpdate(UserPlaylistBase):
    playlist_link: Optional[str]


# properties shared by models stored in DB
class UserPlaylistInDBBase(UserPlaylistBase):
    id: int = None

    class Config:
        from_attributes = True


# additional properties stored in DB but not returned by API
class UserPlaylistInDB(UserPlaylistInDBBase): ...


# additional properties to return via API
class UserPlaylist(UserPlaylistInDBBase):
    model_config = ConfigDict(from_attributes=True)

    playlist_link: List[str]
