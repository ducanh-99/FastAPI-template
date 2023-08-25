
from app.migrations.models.user import User
from app.repositories.base_repository import AbstractRepository
from app.schemas.schema_user import UserPayload


class UserRepository(AbstractRepository):

    def create_user(self, user_payload: UserPayload) -> User:
        new_user = User(
            **user_payload.dict()
        )
        self.session.add(new_user)
        return new_user
