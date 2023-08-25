import json
import logging
from typing import Any, Union, List

import humps
from fastapi import APIRouter
from fastapi.params import Depends

from app.schemas.schema_base import DataResponse
from app.schemas.schema_user import UserPayload
from app.services.user_service import UserService


logger = logging.getLogger(__name__)
router = APIRouter()
router_lead = APIRouter()


@router.get("", response_model=DataResponse[Any])
def get_user(payload: UserPayload, user_service: UserService = Depends(),):
    res = user_service.create_user(payload)
    return DataResponse().success_response(res, lang=user_service.lang)
