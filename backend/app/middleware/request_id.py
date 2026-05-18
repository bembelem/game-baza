"""Middleware, выдающий каждому запросу уникальный trace_id."""
import uuid
from typing import Callable

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.context import set_request_id

REQUEST_ID_HEADER = "X-Request-ID"


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Генерирует trace_id, кладёт в ContextVar и в заголовок ответа.

    Если клиент прислал X-Request-ID — используем его (полезно для
    распределённой трассировки между сервисами). Иначе генерим UUID4.
    """

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        request_id = request.headers.get(REQUEST_ID_HEADER) or str(uuid.uuid4())
        set_request_id(request_id)

        response = await call_next(request)
        response.headers[REQUEST_ID_HEADER] = request_id
        return response
