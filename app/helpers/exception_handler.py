from fastapi import Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.dependencies import lang_validator
from app.i18n.errors import PYDANTIC_ERROR_MAPPING, ErrorCode
from app.i18n.lang import MultiLanguage
from app.schemas.schema_base import ResponseSchemaBase


class CustomException(Exception):
    http_code: int
    code: str
    message: str

    def __init__(self, http_code: int = None, code: str = None, message: str = None):
        self.http_code = http_code if http_code else 500
        self.code = code if code else str(self.http_code)
        self.message = message


class ValidateException(CustomException):

    def __init__(self, code: str = None, message: str = None):
        self.http_code = 400
        self.code = code if code else str(self.http_code)
        self.message = message


async def http_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.http_code,
        content=jsonable_encoder(
            ResponseSchemaBase().custom_response(exc.code, exc.message))
    )


async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(
            '400', get_message_validation(exc)))
    )


async def fastapi_error_handler(request, exc):
    language = request.headers.get('language')
    lang: MultiLanguage = lang_validator(language)
    
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(
            ErrorCode.ERROR_9999_INTERNAL_SERVER_ERROR, lang.get(ErrorCode.ERROR_9999_INTERNAL_SERVER_ERROR)))
    )


class NotMatchException(Exception):
    """Raised when multi-file lang not match"""

    def __init__(self, message="multi-file language not match"):
        self.message = message

    def __str__(self):
        return f'{self.message}'


def get_message_validation(exc):
    message = ""
    for error in exc.errors():
        message += "/'" + str(error.get("loc")
                              [1]) + "'/" + ': ' + error.get("msg") + ", "

    message = message[:-2]
    return message

def build_err_location(arr: tuple) -> str:
    result = []
    for item in arr:
        if isinstance(item, str):
            result.append(item)
        elif isinstance(item, int):
            last_item = result.pop()
            result.append(f"{last_item}[{item}]")
        else:
            raise Exception(f"Unsupported {type(item)}")
    return ".".join(result)

def get_validation_resp(lang: MultiLanguage, errors: dict) -> dict:
    loc = errors.get("loc")
    msg = errors.get("msg")
    type = errors.get("type")

    err_location = build_err_location(loc[1:])

    if type not in PYDANTIC_ERROR_MAPPING:
        raise Exception(f"Loc: {err_location}\nMsg: {msg}\nType: {type}\nCòn chần chờ gì mà không thêm type ({type}) vào PYDANTIC_ERROR_MAPPING đi chứ còn gì nữa ??? 🙂😀 ???")
    code = PYDANTIC_ERROR_MAPPING[type]
    ctx = errors.get('ctx')
    values = []
    if ctx:
        values = ctx.values()
    
    message = lang.get(code, err_location, *values)

    return {
        "code": code,
        "message": message,
    }


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    language = request.headers.get('language')
    lang: MultiLanguage = lang_validator(language)

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            get_validation_resp(lang, exc.errors()[0])
        ),
    )
