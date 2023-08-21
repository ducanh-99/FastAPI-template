import logging

import uvicorn
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.concurrency import iterate_in_threadpool
from starlette.middleware.cors import CORSMiddleware

from app.api.api import router
from app.core.config import settings
from app.helpers.exception_handler import CustomException, fastapi_error_handler, http_exception_handler, \
    validation_exception_handler

logging.config.fileConfig(settings.LOGGING_CONFIG_FILE, disable_existing_loggers=False)



def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, openapi_url=f'/openapi.json',
        docs_url='/docs', redoc_url="/re-doc",
        description=settings.PROJECT_NAME,
        debug=settings.DEBUG,
    )
    application.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    application.include_router(router=router, prefix='/api')
    application.add_exception_handler(CustomException, http_exception_handler)
    application.add_exception_handler(Exception, fastapi_error_handler)
    application.add_exception_handler(
        RequestValidationError, validation_exception_handler)
    application.add_exception_handler(RequestValidationError, validation_exception_handler)
    return application


app = get_application()


@app.middleware("http")
async def add_log_error(request: Request, call_next):
    await set_body(request, await request.body())
    request_body_bytes = await get_body(request)
    response = await call_next(request)
    if response.status_code != 200:
        response_body = [chunk async for chunk in response.body_iterator]
        response.body_iterator = iterate_in_threadpool(iter(response_body))
        logging.error(f"response_body={response_body[0].decode()}")
        logging.error(request_body_bytes.decode(encoding="utf-8", errors="ignore"))
    return response


async def set_body(request: Request, body: bytes):
    async def receive():
        return {"type": "http.request", "body": body}

    request._receive = receive


async def get_body(request: Request) -> bytes:
    body = await request.body()
    await set_body(request, body)
    return body


if __name__ == '__main__':
    uvicorn.run("app.main:app", port=5000, reload=True)
