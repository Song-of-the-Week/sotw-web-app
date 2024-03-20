from typing import List, Optional
from pydantic import ConfigDict
from pydantic import EmailStr

from app.models.response import Response
from app.schemas.base import Base
from app.schemas import Sotw


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
    sotw: Optional[int] = None
    current_password: Optional[str] = None
    new_password: Optional[str] = None


# properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int = None

    class Config:
        from_attributes = True


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
    sotw_list: List[Sotw]
    responses: List[Response]
