import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import uuid

from app.exceptions import AppHTTPException


async def app_http_exception_handler(request: Request, exc: AppHTTPException) -> JSONResponse:
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


async def request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    details = {}
    for error in exc.errors():
        field = error["loc"][-1]
        details[field] = error["msg"]

    return JSONResponse(
        status_code=422,
        content={
            "error":   "2020_VALIDATION_ERROR",
            "message": "Данные не прошли валидацию.",
            "details": details,
            "traceId": str(uuid.uuid4()),
        }
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logging.exception(exc)
    return JSONResponse(
        status_code=500,
        content={
            "error":   "5000_INTERNAL_ERROR",
            "message": "Внутренняя ошибка сервера.",
            "details": {},
            "traceId": str(uuid.uuid4()),
        }
    )