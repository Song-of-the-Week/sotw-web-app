import logging
from sqlalchemy.orm import Session

from app import crud
from app import schemas

logger = logging.getLogger(__name__)


def init_db(session: Session):
    # create a superuser
    user = crud.user.get_by_email(session, email='admin@admin.admin')
    if not user:
        user_in = schemas.UserCreate(
            email='admin@admin.admin',
            name='admin',
            is_superuser=True,
            password='admin'
        )
        user = crud.user.create(session, object_in=user_in)
    else:
        logger.warning(f"Skipping creating superuser. User already exists.")