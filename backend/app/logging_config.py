"""Настройка логирования с автоподмешиванием trace_id."""
import logging

from app.context import _request_id_var


class RequestIdFilter(logging.Filter):
    """Добавляет атрибут request_id в каждый LogRecord."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = _request_id_var.get() or "-"
        return True


def setup_logging(level: str = "INFO") -> None:
    """Настраивает корневой логгер: формат с trace_id и фильтр."""
    log_format = (
        "%(asctime)s | %(levelname)-8s | %(request_id)s | "
        "%(name)s:%(funcName)s:%(lineno)d | %(message)s"
    )

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(log_format))
    handler.addFilter(RequestIdFilter())

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)

    # Чтобы uvicorn-логи (запросы, ошибки сервера) тоже шли через наш формат
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logger = logging.getLogger(name)
        logger.handlers.clear()
        logger.propagate = True
