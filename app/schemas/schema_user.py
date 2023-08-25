from typing import Optional
from app.schemas.schema_base import MappingByFieldName


class UserPayload(MappingByFieldName):
    full_name: Optional[str]
    phone_number: Optional[str]
