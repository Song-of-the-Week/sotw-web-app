import logging
from typing import Any

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm.session import Session

from app import crud
from app  import schemas
from app.api import deps
# from app.clients.email import EmailClient
# from app.core.email import send_registration_confirmed_email
from app.core.auth import authenticate
from app.core.auth import create_access_token
from app.models.user import User
from app.shared.config import cfg


logger = logging.getLogger(__name__)


router = APIRouter()


@router.post("/login")
def login(
    session: Session = Depends(deps.get_session),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    Get the JWT for a user from OAuth2 request body
    """
    user = authenticate(email=form_data.username, password=form_data.password, session=session)
    if not user:
        raise HTTPException(status_code=400, detail='Incorrect username or password')
    
    return {
        'access_token': create_access_token(sub=user.id),
        'token_type': 'bearer',
    }


@router.get('/current_user', response_model=schemas.User)
def get_current_user(
    current_user: User = Depends(deps.get_current_user)
):
    """
    Fetch the current logged in user
    """

    user = current_user
    return user


@router.post('/register', response_model=schemas.User, status_code=201)
def register(
    *,
    session: Session = Depends(deps.get_session),
    # email_client: EmailClient = Depends(deps.get_email_client),
    # background_tasks: BackgroundTasks,
    user_in: schemas.user.UserCreate,
) -> Any:
    """
    Register a new user
    """

    user = crud.user.get_by_email(session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists",
        )
    user = crud.user.create(session=session, object_in=user_in)

    # if cfg.SEND_REGISTRATION_EMAILS:
    #     background_tasks.add_task(send_registration_confirmed_email, user=user, client=email_client)
    
    return user