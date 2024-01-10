from typing import Optional

from sqlalchemy.orm import Session

from app.crud.crud_base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserUpdate
from app.core.security import get_password_hash


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, session: Session, *, email: str) -> Optional[User]:
        """
        Session query to get an object from the database with the specified email
        :session: a SQLAlchemy Session object that is connected to the database
        :email: the email of the object being sought after
        """
        return session.query(User).filter(User.email == email).first()
    
    def create(self, session: Session, *, object_in: UserCreate) -> User:
        """
        Creates a User in the database and creates a spotify playlist for the user
        :session: a SQLAlchemy Session object that is connected to the database
        :object_in: a pydantic model UserCreate object
        """
        create_data = object_in.model_dump()
        create_data.pop('password')
        db_object = User(**create_data)
        db_object.password = get_password_hash(object_in.password)
        # TODO fill in spotify api stuff to create a playlist for this new user and add the link to the new object
        db_object.playlist_link = ''
        session.add(db_object)
        session.commit()

    def add_user_to_sotw(self, session: Session, *, db_object: User, object_in: UserUpdate) -> User:
        """
        Adds the sotw to the user (and vice versa via model relationship)
        :session: a SQLAlchemy Session object that is connected to the database
        :db_object: a model object of the ser to update
        :object_in: a pydantic model UserUpdate object with a reference to the sotw model object
        """
        db_object.sotw_list.append(object_in.sotw)
        session.add(db_object)
        session.commit()
        session.refresh(db_object)
        return db_object


user = CRUDUser(User)
