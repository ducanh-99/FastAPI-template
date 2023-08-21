from functools import lru_cache
from typing import Optional

from fastapi.params import Header
from fastapi.security import HTTPBearer

from app.i18n.lang import Language, MultiLanguage

bearer = HTTPBearer()


# this decorator make fun only build one time, and next time func return cache
@lru_cache
def lang_header(language: Optional[Language] = Header(Language.EN)):
    return MultiLanguage(lang=language)


@lru_cache
def lang_validator(language: str) -> MultiLanguage:
    if not language:
        return MultiLanguage(lang=Language.EN)
    language = language.lower()
    all_languages = [v.value.lower() for k, v in Language._member_map_.items()]
    if language not in all_languages:
        return MultiLanguage(lang=Language.EN)
    return MultiLanguage(lang=Language(language))
