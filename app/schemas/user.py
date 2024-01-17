from typing import List, Optional
from pydantic import EmailStr
from pydantic import HttpUrl

from app.schemas.base import Base

class UserBase(Base):
    email: Optional[EmailStr]
    name: Optional[str]
    is_superuser: bool = False


# properties to receive via API creation
class UserCreate(UserBase):
    email: EmailStr
    password: str
    sotw_list: Optional[List[int]] = []
    responses: Optional[List[int]] = []

# properties to receive via API update
class UserUpdate(UserBase):
    sotw_id: Optional[int]


# properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int = None

    class Config:
        orm_mode = True


# additional properties stored in DB bt not returned by API
class UserInDB(UserInDBBase):
    password: str


# additional properties to return via API
class User(UserInDBBase):
    # playlist_link: Optional[HttpUrl]
    sotw_list: List[int]
    responses: List[int]
