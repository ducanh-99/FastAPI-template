from pydantic import BaseModel, validator
from pydantic.fields import Field

from app.helpers.exception_handler import ValidateException
from app.schemas.schema_base import MappingByFieldName


class UploadFileResponse(MappingByFieldName):
    file_name: str = Field(..., alias='fileName')


class DownloadFileRequest(BaseModel):
    relative_path: str

    @validator("relative_path")
    def validate_relative_path(cls, v):
        if len(v) < 1 or len(v) > 500:
            raise ValidateException("004", f"Trường dữ liệu không hợp lệ: Độ dài relative_path phải từ 1-500")
        return v


class Identity(BaseModel):
    id: int
    name: str


class Type(BaseModel):
    code: str
    name: str
