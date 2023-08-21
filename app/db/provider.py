import logging

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.base import get_session
from app.dependencies import lang_header
from app.helpers.exception_handler import CustomException
from app.i18n.errors import ErrorCode
from app.i18n.lang import MultiLanguage

logger = logging.getLogger(__name__)


class Provider:
    def __init__(self, session: Session = Depends(get_session), lang: MultiLanguage = Depends(lang_header)):
        self.session = session
        self.lang = lang

    def rollback(self):
        self.session.rollback()

    def commit(self):
        try:
            self.session.commit()
        except Exception as err:
            logger.exception(f"Commit error: {err}")
            self.rollback()
            code = ErrorCode.ERROR_9999_INTERNAL_SERVER_ERROR
            raise CustomException(http_code=500, code=code, message=self.lang.get(code))
