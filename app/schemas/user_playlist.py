from typing import List, Optional
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import HttpUrl

from app.schemas.base import Base


class UserPlaylistBase(Base):
    playlist_link: HttpUrl


# properties to receive via API creation
class UserPlaylistCreate(UserPlaylistBase):
    user_id: Optional[int]
    sotw_id: Optional[int]


# properties to receive via API update
class UserPlaylistUpdate(UserPlaylistBase):
    playlist_link: Optional[HttpUrl]


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

    playlist_link: List[HttpUrl]
