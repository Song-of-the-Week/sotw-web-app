from typing import Any
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Session

import shared.config as cfg


class Base(DeclarativeBase):
    
    def __init__(self, **kw: Any):
        super().__init__(**kw)
        
        self.engine = create_engine(cfg.POSTGRES_URL)
    

    def get_session(self):
        return Session(self.engine)