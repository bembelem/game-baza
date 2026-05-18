"""Контекст текущего запроса (request-scoped storage)."""
import uuid
from contextvars import ContextVar

# Хранит trace_id текущего HTTP-запроса.
# Заполняется RequestIdMiddleware на входе, читается отовсюду:
# логгером, exception handlers, бизнес-кодом.
_request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)


def set_request_id(request_id: str) -> None:
    _request_id_var.set(request_id)


def get_request_id() -> str:
    """Возвращает trace_id текущего запроса.

    Если запрос отсутствует (фоновая задача, тест) — генерит новый UUID,
    чтобы вызывающему коду не надо было думать о None.
    """
    rid = _request_id_var.get()
    if rid is None:
        rid = str(uuid.uuid4())
        _request_id_var.set(rid)
    return rid
