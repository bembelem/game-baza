import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.context import get_request_id
from app.exceptions import AppHTTPException

logger = logging.getLogger(__name__)


async def app_http_exception_handler(request: Request, exc: AppHTTPException) -> JSONResponse:
    logger.warning(
        "App error: %s | %s | %s",
        exc.error_code, exc.status_code, exc.details,
    )
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


async def request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    details = {}
    for error in exc.errors():
        field = error["loc"][-1]
        details[field] = error["msg"]

    trace_id = get_request_id()
    logger.warning("Validation error: %s", details)

    return JSONResponse(
        status_code=422,
        content={
            "error":   "2020_VALIDATION_ERROR",
            "message": "Данные не прошли валидацию.",
            "details": details,
            "traceId": trace_id,
        }
    )


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    trace_id = get_request_id()
    # exc_info=True → стектрейс попадает в лог. trace_id уже подмешан фильтром.
    logger.exception("Unhandled exception: %s", exc, exc_info=True)

    return JSONResponse(
        status_code=500,
        content={
            "error":   "5000_INTERNAL_ERROR",
            "message": "Внутренняя ошибка сервера.",
            "details": {},
            "traceId": trace_id,
        }
    )
