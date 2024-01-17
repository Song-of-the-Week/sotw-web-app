from typing import Optional, MutableMapping, List, Union
from datetime import datetime, timedelta

from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm.session import Session
from jose import jwt

from app.models.user import User
from app.shared.config import cfg
from app.core.security import verify_password


JWTPayloadMapping = MutableMapping[
    str, Union[datetime, bool, str, List[str], List[int]]
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f'{cfg.API_V1_STR}/auth/login')


def authenticate(*, email: str, password: str, session: Session) -> Optional[User]:
    """
    Authenticate the user with the email and password provided
    :email: the email of the user to be authenticated
    :password: the password of the user to be authenticated
    :session: a database session
    """
    user = session.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    
    return user


def create_access_token(*, sub: str) -> str:
    return _create_token(
        token_type='access_token',
        lifetime=timedelta(minutes=cfg.ACCESS_TOKEN_EXPIRE_MINUTES),
        sub=sub,
    )


def _create_token(token_type: str, lifetime: timedelta, sub: str) -> str:
    payload = {}
    expire = datetime.utcnow() + lifetime
    payload['type'] = token_type
    
    # https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.3
    # The "exp" (expiration time) claim identifies the expiration time on
    # or after which the JWT MUST NOT be accepted for processing
    payload["exp"] = expire

    # The "iat" (issued at) claim identifies the time at which the
    # JWT was issued.
    payload["iat"] = datetime.utcnow()

    # The "sub" (subject) claim identifies the principal that is the
    # subject of the JWT
    payload["sub"] = str(sub)
    return jwt.encode(payload, cfg.JWT_SECRET, algorithm=cfg.ALGORITHM)