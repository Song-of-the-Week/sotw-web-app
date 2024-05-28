from datetime import datetime
from loguru import logger
from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app import crud
from app import schemas


def init_db(session: Session):
    # create a superuser
    superuser = crud.user.get_by_email(session, email="admin@admin.admin")
    if not superuser:
        user_in = schemas.UserCreate(
            email="admin@admin.admin",
            name="admin",
            is_superuser=True,
            password="password",
        )
        superuser = crud.user.create(session, object_in=user_in)
    else:
        logger.warning(f"Skipping creating superuser. Superuser already exists.")
    # create a regular user
    user = crud.user.get_by_email(session, email="a@b.c")
    if not user:
        user_in = schemas.UserCreate(
            email="a@b.c",
            name="adam",
            is_superuser=False,
            password="password",
        )
        user = crud.user.create(session, object_in=user_in)
    else:
        logger.warning(f"Skipping creating user. User already exists.")
    # create a test sotw
    sotw = crud.sotw.get(session, id=1)
    if not sotw:
        sotw_in = schemas.SotwCreate(
            name="test",
            results_datetime=datetime(1907, 3, 3, 8, 0).timestamp() * 1000,
            owner_id=1,
        )
        sotw = crud.sotw.create(session, object_in=sotw_in)
        crud.user.add_user_to_sotw(session=session, db_object=superuser, object_in=sotw)
    else:
        logger.warning(f"Skipping creating test sotw. Test sotw already exists.")


def main():
    logger.info("Creating inital data")
    with SessionLocal() as session:
        init_db(session)
    logger.info("Initial data created")
