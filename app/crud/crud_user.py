from typing import List, Optional

from sqlalchemy.orm import Session
from loguru import logger

from app.crud.crud_base import CRUDBase
from app.models.response import Response
from app.models.sotw import Sotw
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate
from app.core.security import get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, session: Session, *, email: str) -> Optional[User]:
        """
        Get a user model object from the database with the specified email

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            email (str): The email of the user being sought after.

        Returns:
            Optional[User]: The user with the given email.
        """
        return session.query(User).filter(User.email == email).first()

    def create(self, session: Session, *, object_in: UserCreate) -> User:
        """
        Creates a User in the database with a hashed password.

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            object_in (UserCreate): A pydantic model used to create the user.

        Returns:
            User: The newly created user.
        """

        create_data = object_in.model_dump()
        create_data.pop("password")
        db_object = User(**create_data)
        db_object.password = get_password_hash(object_in.password)
        session.add(db_object)
        session.commit()

        return self.get_by_email(session=session, email=db_object.email)

    def add_user_to_sotw(
        self, session: Session, *, db_object: User, object_in: Sotw
    ) -> User:
        """
        Adds the sotw to the user (and vice versa via model relationship)

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            db_object (User): A model object of the user to update.
            object_in (Sotw): A sotw model object to add to the user.

        Returns:
            User: The newly updated user.
        """
        db_object.sotw_list.append(object_in)
        session.add(db_object)
        session.commit()
        session.refresh(db_object)
        return db_object

    def remove_user_from_sotw(
        self, session: Session, *, db_object: User, object_in: Sotw
    ) -> User:
        """
        Removes the sotw from the user (and vice versa via model relationship)

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            db_object (User): A model object of the user to update.
            object_in (Sotw): A sotw model object to remove from the user.

        Returns:
            User: The newly updated user.
        """
        index = None
        for i, sotw in enumerate(db_object.sotw_list):
            if sotw.id == object_in.id:
                index = i
                break
        if index is not None:
            del db_object.sotw_list[index]
        session.add(db_object)
        session.commit()
        session.refresh(db_object)
        return db_object

    def get_submitted_users(self, session: Session, *, week_id: str) -> List[User]:
        """
        Gets all the user's who have submitted a response for the given week id

        Args:
            session (Session): A SQLAlchemy Session object that is connected to the database.
            week_id (str): A week id string.

        Returns:
            List[User]: list of users who have submitted a response for the week with the given week id.
        """
        return (
            session.query(User)
            .join(Response, Response.submitter_id == User.id)
            .filter(Response.week_id == week_id)
            .all()
        )


user = CRUDUser(User)
