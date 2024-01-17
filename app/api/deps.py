from typing import Optional
from typing import AsyncGenerator
from typing import Generator
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm.session import Session

from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from sqlalchemy.orm.session import Session

from app.db.session import SessionLocal
from app.db.session import AsyncSessionLocal
from app.models.user import User
from app.core.auth import oauth2_scheme
from app.shared.config import cfg


class TokenData(BaseModel):
    username: Optional[str] = None


# synchronous orm session
def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


# synchronous orm session
def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        session.close()


async def get_current_user(
    session: Session = Depends(get_session), token: str = Depends(oauth2_scheme)
) -> User:
    """
    Get the user that corresponds to the JWT given
    :session: a SQLAlchemy Session object that is connected to the database
    :token: a JWT with the id of the user being requested
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            cfg.JWT_SECRET,
            algorithms=[cfg.ALGORITHM],
            options={"verify_aud": False},
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = session.query(User).filter(User.id == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user