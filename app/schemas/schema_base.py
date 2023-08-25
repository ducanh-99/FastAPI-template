from datetime import datetime
from typing import Generic, Optional, TypeVar

from humps import camelize
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

from app.helpers.convert import convert_datetime_to_json_decode
from app.i18n.errors import ErrorCode
from app.i18n.lang import MultiLanguage

T = TypeVar("T")


def to_camel(string):
    return camelize(string)


class ResponseSchemaBase(BaseModel):
    __abstract__ = True

    code: str = ''
    message: str = ''

    def custom_response(self, code: str, message: str):
        self.code = code
        self.message = message
        return self

    def success_response(self):
        self.code = ErrorCode.SUCCESS_0000
        self.message = "Success"
        return self


class ResponseSchemaBaseNew(BaseModel):
    __abstract__ = True

    code: str = ''
    message: str = ''
    trace_id: Optional[str] = Field('', alias="traceId")

    def custom_response(self, code: str, message: str, trace_id: str, data: T):
        pass

    def success_response(self, data: T, lang: MultiLanguage, trace_id: Optional[str]):
        pass


class DataResponse(ResponseSchemaBase, GenericModel, Generic[T]):
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def custom_response(self, code: str, message: str, data: T):
        self.code = code
        self.message = message
        self.data = data
        return self

    def success_response(self, data: T, lang: MultiLanguage):
        self.code = ErrorCode.SUCCESS_0000
        self.message = lang.get(ErrorCode.SUCCESS_0000)
        self.data = data
        return self


class DataResponseNew(ResponseSchemaBaseNew, GenericModel, Generic[T]):
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def custom_response(self, code: str, message: str, data: T, trace_id: str = ''):
        self.code = code
        self.message = message
        self.trace_id = trace_id
        self.data = data
        return self

    def success_response(self, data: T, lang: MultiLanguage, trace_id: Optional[str]):
        self.code = ErrorCode.SUCCESS_0000
        self.message = lang.get(ErrorCode.SUCCESS_0000)
        self.data = data
        self.trace_id = trace_id
        return self


class MappingByFieldName(BaseModel):
    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
        use_enum_values = True
        json_encoders = {
            datetime: convert_datetime_to_json_decode,
        }


class BaseModelUseEnumValues(BaseModel):
    class Config:
        use_enum_values = True


class PaginationReq(MappingByFieldName):
    page: Optional[int] = Field(default=1, ge=1)
    page_size: Optional[int] = Field(default=10, alias="pageSize", ge=1, le=1000)


class PaginationResp(MappingByFieldName):
    current_page: int
    page_size: int
    total_items: int
