from pydantic import ConfigDict
from app.schemas.base import Base
from app.models.response import Response


class UserSongMatchBase(Base):
    user_id: int
    song_id: int


# properties to receive via API creation
class UserSongMatchCreate(UserSongMatchBase):
    correct_guess: bool
    response_id: int


# properties to receive via API update
class UserSongMatchUpdate(UserSongMatchBase): ...


# properties shared by models stored in DB
class UserSongMatchInDBBase(UserSongMatchBase):
    id: int = None
    model_config = ConfigDict(from_attributes=True)


# additional properties stored in DB bt not returned by API
class UserSongMatchInDB(UserSongMatchInDBBase):
    response: Response = None


# additional properties to return via API
class UserSongMatch(UserSongMatchInDBBase):
    user_id: str
    song_id: str
    correct_guess: bool
    response_id: str
