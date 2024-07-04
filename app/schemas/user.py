from datetime import datetime
from typing import List, Optional
from pydantic import ConfigDict
from pydantic import EmailStr

from app.schemas.base import Base
from app.schemas import Sotw, UserPlaylist


class UserLoginRequest(Base):
    username: str
    password: str


class UserBase(Base):
    email: Optional[EmailStr]
    name: Optional[str]
    is_superuser: bool = False


# properties to receive via API creation
class UserCreate(UserBase):
    email: EmailStr
    name: str
    password: str
    spotify_linked: Optional[bool] = False
    playlists: Optional[List[int]] = []
    sotw_list: Optional[List[int]] = []


# properties to receive via API update
class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    sotw: Optional[int] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None
    spotify_linked: Optional[bool] = None
    spotify_access_token: Optional[str] = None
    spotify_refresh_token: Optional[str] = None
    spotify_user_id: Optional[str] = None
    spotify_accessed_date: Optional[datetime] = None


# properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int = None
    model_config = ConfigDict(from_attributes=True)


# additional properties stored in DB but not returned by API
class UserInDB(UserInDBBase):
    password: str


# additional properties to return via API
class User(UserInDBBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    name: str
    is_superuser: bool
    spotify_linked: bool
    playlists: Optional[List[UserPlaylist]]
    sotw_list: List[Sotw]


class UserSpotifyAuth(Base):
    code: Optional[str] = None
    error: Optional[str] = None
    state: str
