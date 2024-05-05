from datetime import datetime
import logging
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app import crud
from app import schemas

logger = logging.getLogger(__name__)


def init_db(session: Session):
    # create a superuser
    user = crud.user.get_by_email(session, email="admin@admin.admin")
    if not user:
        user_in = schemas.UserCreate(
            email="admin@admin.admin",
            name="admin",
            is_superuser=True,
            password="password",
        )
        user = crud.user.create(session, object_in=user_in)
    else:
        logger.warning(f"Skipping creating superuser. User already exists.")
    # create a test sotw for the user
    sotw = crud.sotw.get(session, id=1)
    if not sotw:
        sotw_in = schemas.SotwCreate(
            name="test",
            survey_datetime=datetime(1907, 3, 5, 8, 0),
            results_datetime=datetime(1907, 3, 3, 8, 0),
        )
        sotw = crud.sotw.create(session, object_in=sotw_in)
        crud.user.add_user_to_sotw(session=session, db_object=user, object_in=sotw)
    else:
        logger.warning(f"Skipping creating test sotw. Test sotw already exists.")


def main():
    logger.info("Creating inital data")
    with SessionLocal() as session:
        init_db(session)
    logger.info("Initial data created")
