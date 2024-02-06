from typing import Any
from typing import Dict
from typing import Generic
from typing import Optional
from typing import TypeVar
from typing import Type
from typing import Union
from pydantic import BaseModel

from fastapi.encoders import jsonable_encoder
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session

from app.db.base import Base
import app.shared.config as cfg

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]) -> None:
        """
        CRUD object with default methods to Create, Read, Update, and Delete
        :model: a SQLAlchemy model class
        """
        self.model = model

    def get(self, session: Session, id: Any) -> Optional[ModelType]:
        """
        Session query to get an object from the database with the specified id
        :session: a SQLAlchemy Session object that is connected to the database
        :id: the id of the object being sought after
        """
        return session.query(self.model).filter(self.model.id == id).first()

    def create(self, session: Session, *, object_in: CreateSchemaType) -> ModelType:
        """
        Creates an object in the database with the type ModelType
        :session: a SQLAlchemy Session object that is connected to the database
        :object_in: a pydantic model object of type CreateSchemaType
        """
        db_object = self.model(**jsonable_encoder(object_in))
        session.add(db_object)
        session.commit()
        session.refresh(db_object)
        return db_object

    def update(
        self,
        session: Session,
        *,
        db_object: ModelType,
        object_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Updates an object in the database
        :session: a SQLAlchemy Session object that is connected to the database
        :db_object: an object of type ModelType from the database
        :object_in: a pydantic model object of type UpdateSchemaType
        """
        # update the db object
        update_data = (
            object_in
            if isinstance(object_in, dict)
            else object_in.model_dump(exclude_unset=True)
        )
        for field in jsonable_encoder(db_object):
            if field in update_data.keys():
                setattr(db_object, field, update_data[field])
        # update the db object through the session
        session.add(db_object)
        session.commit()
        session.refresh(db_object)
        return db_object

    def delete(self, session: Session, *, id: int) -> ModelType:
        """
        Deletes an object from the database
        :session: a SQLAlchemy Session object that is connected to the database
        :id: the id of the object being removed
        """
        object = session.query(self.model).get(id)
        session.delete(object)
        session.commit()
        return object
