from typing import Any
from jose import JWTError, jwt

from fastapi import APIRouter, BackgroundTasks
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.orm.session import Session

from app import crud
from app import schemas
from app.api import deps
from app.clients.email import EmailClient
from app.core.auth import authenticate, create_access_token
from app.core.security import get_password_hash
from app.models.user import User
from app.shared.config import cfg


router = APIRouter()


@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    session: Session = Depends(deps.get_session),
    *,
    user_id: int,
    email_client: EmailClient = Depends(deps.get_email_client),
    background_tasks: BackgroundTasks,
    payload: schemas.UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update the user object in the db.

    Args:
        user_id (int): ID of the user to update
        payload (schemas.UserUpdate): Data to update user with
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users or for incorrect password

    Returns:
        Any: the uupdated user object
    """
    if not current_user.is_superuser and user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"Not authorized to update.")

    if payload.current_password is not None and payload.new_password is not None:
        if authenticate(
            email=current_user.email, password=payload.current_password, session=session
        ):
            payload = schemas.UserUpdate(
                password=get_password_hash(payload.new_password)
            )
        else:
            raise HTTPException(status_code=400, detail=f"Incorrect password.")
    elif payload.spotify_linked == False and payload.spotify_linked != None:
        payload = schemas.UserUpdate(
            spotify_linked=False,
            spotify_access_token=None,
            spotify_refresh_token=None,
        )
    elif payload.email is not None and cfg.SEND_REGISTRATION_EMAILS:
        # create an email verification token
        verification_token = create_access_token(
            sub=payload.email,
            lifetime=cfg.VERIFICATION_TOKEN_EXPIRE_MINUTES,
        )
        background_tasks.add_task(
            email_client.send_change_verification_email,
            token_url=f"{cfg.EMAIL_CHANGE_VERIFICATION_URL}{verification_token}",
            to=payload.email,
            to_name=current_user.name,
        )
        return current_user

    return crud.user.update(session=session, db_object=current_user, object_in=payload)


@router.get("/verify/{verification_token}", response_model=schemas.User)
async def verify_email_change(
    session: Session = Depends(deps.get_session),
    *,
    verification_token: str,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Update the user object in the db.

    Args:
        verification_token (int): Token for email verification.
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users or for incorrect password

    Returns:
        Any: A user with an updated email
    """
    try:
        # decode the token
        payload = jwt.decode(
            verification_token,
            cfg.JWT_SECRET,
            algorithms=[cfg.ALGORITHM],
            options={"verify_aud": False},
        )
        user_in: schemas.UserUpdate = schemas.UserUpdate(email=payload.get("sub"))
    except JWTError:
        raise HTTPException(
            status_code=403,
            detail=f"The token is no longer valid.",
        )

    return crud.user.update(session=session, db_object=current_user, object_in=user_in)


@router.post("/reset-password")
async def reset_password(
    session: Session = Depends(deps.get_session),
    *,
    email_client: EmailClient = Depends(deps.get_email_client),
    background_tasks: BackgroundTasks,
    payload: schemas.UserUpdate,
) -> Any:
    """
    Generate a token with which to let a user reset their password and email it to the user.

    Args:
        email_client (EmailClient): Client for sending emails.
        background_tasks (BackgroundTasks): FastAPIs method of completing tasks in background to be able to return a response.
        payload (schemas.UserUpdate): User email.
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).

    Raises:
        HTTPException: 403 for unauthorized users or for incorrect password

    Returns:
        Any: the uupdated user object
    """
    # TODO implement this with tests as well as other endpoint to handle token decoding "reset-password-change"
    email = payload.email
    user = crud.user.get_by_email(session=session, email=email)
    if not user:
        raise HTTPException(
            status_code=404, detail=f"No user found with email {email}."
        )

    if email is not None and cfg.SEND_REGISTRATION_EMAILS:
        # create an email verification token
        verification_token = create_access_token(
            sub=email,
            lifetime=cfg.VERIFICATION_TOKEN_EXPIRE_MINUTES,
        )
        background_tasks.add_task(
            email_client.send_password_reset_email,
            token_url=f"{cfg.PASSWORD_RESET_VERIFICATION_URL}{verification_token}",
            to=email,
            to_name=user.name,
        )
        return {"status": 200}

    return {"status": 200}


@router.post("/reset-password-change/{verification_token}")
async def reset_password_change(
    session: Session = Depends(deps.get_session),
    *,
    verification_token: str,
    payload: schemas.UserUpdate,
) -> Any:
    """
    Update the user object in the db.

    Args:
        verification_token (int): Token for email verification.
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        payload: (schemas.UserUpdate): The user's new password.

    Raises:
        HTTPException: 403 for unauthorized users

    Returns:
        Any: A 200 response.
    """
    new_password = payload.new_password

    if not new_password:
        raise HTTPException(
            status_code=400,
            detail=f"Request payload is incomplete.",
        )

    try:
        # decode the token
        payload = jwt.decode(
            verification_token,
            cfg.JWT_SECRET,
            algorithms=[cfg.ALGORITHM],
            options={"verify_aud": False},
        )
        email = payload.get("sub")
        user = crud.user.get_by_email(session=session, email=email)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"It seems that there is something wrong with your verification token. Please try resetting your password again.",
            )
        user_in = schemas.UserUpdate(password=get_password_hash(new_password))
    except JWTError:
        raise HTTPException(
            status_code=403,
            detail=f"The token is no longer valid.",
        )

    session.refresh(user)
    user = crud.user.update(session=session, db_object=user, object_in=user_in)

    return {"status": 200}


@router.delete(
    "/{user_id}",
    response_model=schemas.User,
)
async def delete_user(
    session: Session = Depends(deps.get_session),
    *,
    user_id: int,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    """
    Delete specified user.

    Args:
        user_id (int): ID of the user to  delete
        session (Session, optional): A SQLAlchemy Session object that is connected to the database. Defaults to Depends(deps.get_session).
        current_user (User, optional): Currently logged in user. Dependency ensures they are logged in.

    Raises:
        HTTPException: 403 for unauthorized users.s

    Returns:
        Any: The deleted object.
    """
    if not current_user.is_superuser and user_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"Not authorized to delete.")

    return crud.user.delete(session=session, id=user_id)
