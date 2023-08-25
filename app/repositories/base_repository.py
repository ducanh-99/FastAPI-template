from abc import ABC
from typing import List

from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.db.base import get_session
from app.migrations.models import BareBaseModel


class AbstractRepository(ABC):
    model: BareBaseModel

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_by_id(self, id_: int) -> object:
        return self.session.query(self.model).filter(self.model.id == id_).first()

    def get_in_ids(self, ids: List[int]):
        return self.session.query(self.model).filter(self.model.id.in_(ids)).all()

    def delete_from_id(self, id_: int):
        self.session.query(self.model).filter(self.model.id == id_).delete()
