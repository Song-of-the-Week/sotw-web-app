from typing import Any
from typing import Dict

from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    id: Any
    __name__: str
    
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
    
    def __repr__(self) -> str:
        return self.as_dict().__repr__()
    
    def as_dict(self) -> Dict[str, Any]:
        dict_obj = {
            c.name: getattr(self, c.name) for c in self.__table__.columns
        }
        return dict_obj