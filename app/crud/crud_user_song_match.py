from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.crud.crud_song import song
from app.models.response import UserSongMatch
from app.schemas.user_song_match import UserSongMatchCreate
from app.schemas.user_song_match import UserSongMatchUpdate


class CRUDUserSongMatch(CRUDBase[UserSongMatch, UserSongMatchCreate, UserSongMatchUpdate]):
    ...


user_song_match = CRUDUserSongMatch(UserSongMatch)
