from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict

from app.schemas.base import Base
from app.schemas.user_song_match import UserSongMatch, UserSongMatchBase


class ResponsePost(Base):
    picked_song_1: Optional[int] = None
    picked_song_2: Optional[int] = None
    user_song_matches: Optional[List[UserSongMatchBase]] = None
    next_song: str
    repeat_approved: Optional[bool] = False
    theme: Optional[str] = None
    theme_description: Optional[str] = None


class ResponseResponse(Base):
    valid: Optional[bool] = False
    repeat: Optional[bool] = False


class ResponseBase(Base):
    picked_song_1_id: Optional[int] = None
    picked_song_2_id: Optional[int] = None


# properties to receive via API creation
class ResponseCreate(ResponseBase):
    next_song_id: int
    sotw_id: int
    week_id: str
    submitter_id: int
    theme: Optional[str] = None
    theme_description: Optional[str] = None


# properties to receive via API update
class ResponseUpdate(ResponseBase):
    number_correct_matches: int = 0


# properties shared by models stored in DB
class ResponseInDBBase(ResponseBase):
    id: int = None
    model_config = ConfigDict(from_attributes=True)


# additional properties stored in DB bt not returned by API
class ResponseInDB(ResponseInDBBase): ...


# additional properties to return via API
class Response(ResponseInDBBase):
    submitter_id: str
    user_song_matches: List[UserSongMatch]
    number_correct_matches: int
    next_song: str
    picked_song_1_id: str
    picked_song_2_id: str
    sotw_id: str
    week_id: str
    theme: str
    theme_description: str
