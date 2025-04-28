from typing import List, Optional

from pydantic import ConfigDict

from app.schemas.base import Base


class ResultsBase(Base):
    sotw_id: int
    week_id: str


# properties to receive via API creation
class ResultsCreate(ResultsBase):
    first_place: str
    second_place: str
    all_songs: str
    guessing_data: str
    theme: Optional[str] = None
    theme_description: Optional[str] = None


# properties to receive via API update
class ResultsUpdate(ResultsBase): ...


# properties shared by models stored in DB
class ResultsInDBBase(ResultsBase):
    id: int = None
    model_config = ConfigDict(from_attributes=True)


# additional properties stored in DB bt not returned by API
class ResultsInDB(ResultsInDBBase): ...


# additional properties to return via API
class Results(ResultsInDBBase):
    id: str
    sotw_id: str
    first_place: str
    second_place: str
    all_songs: str
    guessing_data: str
    theme: Optional[str] = None
    theme_description: Optional[str] = None


class ResultsErrorResponse(Base):
    message: str
    release_time: int
