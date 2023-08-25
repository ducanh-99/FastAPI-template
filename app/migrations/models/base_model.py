from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.orm import as_declarative, declared_attr

from .utils import get_current_time


@as_declarative()
class Base:
    __abstract__ = True
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()


class BareBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    created_at = Column(DateTime, default=get_current_time, nullable=False)
    modified_at = Column(DateTime, default=get_current_time,
                         onupdate=get_current_time, nullable=False)
