from pydantic import BaseModel


class Base(BaseModel):
    class Config:
        arbitrary_types_allowed = True