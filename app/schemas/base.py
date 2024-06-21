from pydantic import BaseModel, ConfigDict


class Base(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
