import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.exceptions import AppHTTPException, ValidationHTTPException

logger = logging.getLogger(__name__)


def _to_response(exc: AppHTTPException) -> JSONResponse:
    """Превращает AppHTTPException в стандартный JSON-ответ."""
    return JSONResponse(status_code=exc.status_code, content=exc.detail)


async def app_http_exception_handler(request: Request, exc: AppHTTPException) -> JSONResponse:
    logger.warning(
        "App error: %s | %s | %s",
        exc.error_code, exc.status_code, exc.details,
    )
    return _to_response(exc)


async def request_validation_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Конвертирует FastAPI-валидацию в наш формат через ValidationHTTPException."""
    details = {error["loc"][-1]: error["msg"] for error in exc.errors()}
    logger.warning("Validation error: %s", details)
    return _to_response(ValidationHTTPException(details=details))


async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Любая неперехваченная ошибка — 500 в стандартном формате."""
    # exc_info=True → стектрейс попадает в лог. trace_id уже подмешан фильтром.
    logger.exception("Unhandled exception: %s", exc, exc_info=True)
    return _to_response(AppHTTPException())
