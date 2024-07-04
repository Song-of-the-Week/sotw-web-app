from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict

from app.schemas.base import Base
from app.schemas.user_song_match import UserSongMatchBase


class ResponsePost(Base):
    picked_song_1: Optional[int]
    picked_song_2: Optional[int]
    matched_user_songs: Optional[List[UserSongMatchBase]]
    next_song: str


class ResponseBase(Base):
    next_song_id: int
    matched_users_songs: Optional[List[int]] = []
    picked_song_1_id: Optional[int] = None
    picked_song_2_id: Optional[int] = None
    sotw_id: int
    week_id: str
    submitter_id: int


# properties to receive via API creation
class ResponseCreate(ResponseBase):
    next_song_id: int
    sotw_id: int
    week_id: str
    submitter_id: int


# properties to receive via API update
class ResponseUpdate(ResponseBase):
    next_song_id: Optional[int] = None
    matched_users_songs: Optional[List[int]] = []
    picked_song_1_id: Optional[int] = None
    picked_song_2_id: Optional[int] = None


# properties shared by models stored in DB
class ResponseInDBBase(ResponseBase):
    id: int = None
    model_config = ConfigDict(from_attributes=True)


# additional properties stored in DB bt not returned by API
class ResponseInDB(ResponseInDBBase): ...


# additional properties to return via API
class Response(ResponseInDBBase):
    submitter_id: int
    user_song_match: List[int]
    num_correct_guesses: int
    votes: List[int]
