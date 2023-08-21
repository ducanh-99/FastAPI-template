from fastapi import Depends

from app.db.provider import Provider
from app.dependencies import lang_header
from app.i18n.lang import MultiLanguage


class BaseService:
    def __init__(
        self,
        lang: MultiLanguage = Depends(lang_header),
        provider: Provider = Depends(),
    ):
        self.lang = lang
        self.provider = provider
