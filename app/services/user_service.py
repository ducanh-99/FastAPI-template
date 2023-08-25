
from fastapi import Depends
from app.db.provider import Provider
from app.dependencies import lang_header
from app.i18n.lang import MultiLanguage
from app.repositories.user_repository import UserRepository
from app.schemas.schema_user import UserPayload
from app.services.base_service import BaseService


class UserService(BaseService):

    def __init__(
        self,
        lang: MultiLanguage = Depends(lang_header),
        provider: Provider = Depends(),
        user_repository: UserRepository = Depends()
    ):
        self.lang = lang
        self.provider = provider
        self.user_repository = user_repository

    def create_user(self, user_payload: UserPayload) -> int:
        new_user = self.user_repository.create_user(user_payload=user_payload)
        return new_user.id
