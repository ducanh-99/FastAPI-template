import io
import logging
from typing import Any

from fastapi import APIRouter, Path, UploadFile
from fastapi.params import Depends, File
from fastapi.security import HTTPBearer
from starlette.responses import StreamingResponse

from app.helpers.exception_handler import CustomException
from app.schemas.schema_base import DataResponse
from app.schemas.schema_common import UploadFileResponse
from app.storage.minio_handler import MinioHandler

logger = logging.getLogger(__name__)

router = APIRouter()
oauth2_scheme = HTTPBearer()


def check_available_file_name(file_ext):
    # if file_ext.lower() not in (
    #         'jpg', 'png', 'pdf', 'xlsx', 'xls', 'svg', 'pdf', 'doc', 'docx', 'rar', 'zip', 'heic', 'jpeg'):
    #     raise CustomException(http_code=400, code="1002", message="format file")
    pass


@router.post("/upload/minio", response_model=DataResponse[UploadFileResponse], dependencies=[Depends(oauth2_scheme)])
def upload_file_to_minio(file: UploadFile = File(...), minio_handler: MinioHandler = Depends()):
    try:
        data = file.file.read()
        if len(data) > 1024 * 1024 * 50:
            raise CustomException(http_code=400, code=1000, message="Too large")

        file_name = " ".join(file.filename.strip().split())
        file_ext = file_name.split('.')[-1]
        check_available_file_name(file_ext)

        data_file = minio_handler.put_object(
            file_name=file_name,
            file_data=io.BytesIO(data),
            content_type=file.content_type
        )
        return DataResponse().success_response(data_file, minio_handler.lang)
    except CustomException as e:
        raise e
    except Exception as e:
        logger.error(str(e))
        if e.__class__.__name__ == 'MaxRetryError':
            raise CustomException(http_code=400, code=1001, message="Không thể kết nối")
        raise CustomException(code=9999, message="Error Server")


@router.get("/download/minio/{filePath}")
def download_file_from_minio(
        *,
        filePath: str = Path(..., title="The relative path to the file", min_length=1, max_length=500),
        minio_handler: MinioHandler = Depends()
) -> Any:
    try:
        if not minio_handler.check_file_name_exists(filePath):
            raise CustomException(http_code=400, code="1002", message="Not found")
        file = minio_handler.read(file_name=filePath)
        return StreamingResponse(io.BytesIO(file))
    except CustomException as e:
        raise e
    except Exception as e:
        logger.error(str(e))
        if e.__class__.__name__ == 'MaxRetryError':
            raise CustomException(http_code=400, code="1001", message="Cannot connect Minio")
        raise CustomException(code="999", message="Internal service")
