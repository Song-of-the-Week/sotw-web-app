from typing import List, Optional
from pydantic import ConfigDict
from pydantic import EmailStr
from pydantic import HttpUrl

from app.schemas.base import Base


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
    playlists: Optional[List[int]] = []
    sotw_list: Optional[List[int]] = []
    responses: Optional[List[int]] = []


# properties to receive via API update
class UserUpdate(UserBase):
    name: Optional[str] = None
    email: Optional[str] = None
    sotw_list: Optional[List[int]] = None


# properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int = None

    class Config:
        orm_mode = True


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
    playlists: Optional[List[int]]
    sotw_list: List[int]
    responses: List[int]