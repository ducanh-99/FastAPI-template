import logging

from fastapi import APIRouter, Depends
from fastapi.responses import ORJSONResponse

from app.helpers.db import check_database_connect
from app.helpers.exception_handler import CustomException
from app.i18n.errors import ErrorCode
from app.schemas.schema_base import ResponseSchemaBase

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/live", response_model=ResponseSchemaBase, response_class=ORJSONResponse)
async def get():
    return {
        "code": ErrorCode.SUCCESS_0000,
        "message": "Health check success"
    }

@router.get("/ready", response_model=ResponseSchemaBase, response_class=ORJSONResponse)
async def get(result = Depends(check_database_connect)):
    is_database_connect, output = result
    if is_database_connect:
        return {
            "code": ErrorCode.SUCCESS_0000,
            "message": "Ready check success"
        }
    else:
        raise CustomException(message="Ready check false", code="9999")
