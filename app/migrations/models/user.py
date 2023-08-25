import enum

from sqlalchemy import Boolean, Column, Enum as SQLAlchemyEnum, String

from .base_model import BareBaseModel


class UserStatus(enum.Enum):
    active = "active"
    delete = "delete"


class User(BareBaseModel):
    __tablename__ = 'user'

    full_name = Column(String(256), comment="Full Name User")
    phone_number = Column(String(12))
    email = Column(String(256))
    password = Column(String(1024))
    salt = Column(String(256), comment="Salt for hash password")
    role = Column(String(256))
    verify = Column(Boolean, default=False)
    device_code = Column(String(256))
    avatar = Column(String(256))
    status = Column(SQLAlchemyEnum(UserStatus), default=UserStatus.active)
