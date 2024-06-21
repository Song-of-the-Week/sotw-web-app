from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict

from app.schemas.base import Base
from app.db.base import Song
from app.schemas.user_song_match import UserSongMatchBase


class ResponsePost(Base):
    picked_song_1: Optional[int]
    picked_song_2: Optional[int]
    matched_user_songs: Optional[List[UserSongMatchBase]]
    next_song: str


class ResponseBase(Base):
    created_at: datetime
    next_song: Song
    matched_users_songs: Optional[List[int]] = []
    picked_song_1_id: Optional[int] = None
    picked_song_2_id: Optional[int] = None
    sotw_id: int
    week_id: int
    submitter_id: int


# properties to receive via API creation
class ResponseCreate(ResponseBase):
    next_song: Song
    sotw_id: int
    week_id: int
    submitter_id: int


# properties to receive via API update
class ResponseUpdate(ResponseBase):
    next_song: Optional[Song] = None
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
