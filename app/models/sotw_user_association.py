from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Table

from app.db.base_class import Base


sotw_user_association_table = Table(
    "sotw_user_association_table",
    Base.metadata,
    Column("sotw_id", ForeignKey('sotw.id'), primary_key=True),
    Column("user_id", ForeignKey('user.id'), primary_key=True),
)