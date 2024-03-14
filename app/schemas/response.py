from datetime import datetime
from typing import List

from app.schemas.base import Base


class ResponseBase(Base):
    created_at: datetime
    next_song_id: int
    matched_users_songs: List[int]
    picked_songs_ids: List[int]
    sotw_id: int
    week_id: int
    submitter_id: int


# properties to receive via API creation
class ResponseCreate(ResponseBase):
    next_song_id: int
    matched_users_songs: List[int]
    picked_songs_ids: List[int]
    sotw_id: int
    week_id: int
    submitter_id: int


# properties to receive via API update
class ResponseUpdate(ResponseBase):
    next_song_id: int
    matched_users_songs: List[int]
    picked_songs_ids: List[int]


# properties shared by models stored in DB
class ResponseInDBBase(ResponseBase):
    id: int = None

    class Config:
        from_attributes = True


# additional properties stored in DB bt not returned by API
class ResponseInDB(ResponseInDBBase): ...


# additional properties to return via API
class Response(ResponseInDBBase):
    submitter_id: int
    user_song_match: List[int]
    num_correct_guesses: int
    votes: List[int]
