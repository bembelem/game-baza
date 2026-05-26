from fastapi import HTTPException

from app.context import get_request_id


# Base

class AppHTTPException(HTTPException):
    status_code: int = 500
    error_code:  str = "5000_INTERNAL_ERROR"
    message:     str = "Внутренняя ошибка сервера."
    details:     dict = {}  # class-level default — НЕ мутировать, только переопределять в наследниках

    def __init__(self, details: dict | None = None):
        # Берём готовый trace_id из контекста запроса (поставлен RequestIdMiddleware).
        # Никогда не генерим тут — иначе client и логи получат разные UUID.
        self.trace_id = get_request_id()
        # Копируем class-level details, чтобы случайная мутация не задела соседей
        self.details = details if details is not None else dict(self.details)
        super().__init__(status_code=self.status_code, detail=self._build_detail())

    def _build_detail(self) -> dict:
        return {
            "error":   self.error_code,
            "message": self.message,
            "details": self.details,
            "traceId": self.trace_id,
        }


# Validation / Auth

class ValidationHTTPException(AppHTTPException):
    status_code = 422
    error_code  = "2020_VALIDATION_ERROR"
    message     = "Данные не прошли валидацию."


class AuthenticationHTTPException(AppHTTPException):
    status_code = 401
    error_code  = "2010_AUTHENTICATION_ERROR"
    message     = "Ошибка аутентификации."


class EmailAlreadyExistsHTTPException(ValidationHTTPException):
    status_code = 409
    details = {"email": "Пользователь с таким email уже существует."}


class UsernameAlreadyExistsHTTPException(ValidationHTTPException):
    status_code = 409
    details = {"username": "Пользователь с таким username уже существует."}


class EmailNotRegisteredHTTPException(AuthenticationHTTPException):
    details = {"email": "Пользователь с таким email не зарегистрирован."}


class UsernameNotRegisteredHTTPException(AuthenticationHTTPException):
    details = {"username": "Пользователь с таким username не зарегистрирован."}


class IncorrectPasswordHTTPException(AuthenticationHTTPException):
    details = {"password": "Неверный пароль."}


class IncorrectTokenHTTPException(AuthenticationHTTPException):
    error_code = "2011_INCORRECT_TOKEN_ERROR"
    status_code = 401
    message = "Токен не передан или не действителен."


# Not Found

class NotFoundHTTPException(AppHTTPException):
    status_code = 404
    error_code = "4040_NOT_FOUND"
    message = "Ресурс не найден."

class UserNotFoundHTTPException(NotFoundHTTPException):
    message = "Пользователь не найден."

def _make_not_found(resource: str, field: str) -> type[NotFoundHTTPException]:
    """Создаёт подкласс NotFoundHTTPException с готовым message и details."""
    return type(
        f"{field.split('_')[0].capitalize()}NotFoundHTTPException",
        (NotFoundHTTPException,),
        {
            "message": f"{resource} не найден.",
            "details": {field: f"{resource} с таким ID не существует."},
        },
    )


GameNotFoundHTTPException      = _make_not_found("Игра",          "game_id")
GenreNotFoundHTTPException     = _make_not_found("Жанр",          "genre_id")
StoreNotFoundHTTPException     = _make_not_found("Магазин",       "store_id")
PlatformNotFoundHTTPException  = _make_not_found("Платформа",     "platform_id")
PublisherNotFoundHTTPException = _make_not_found("Издатель",      "publisher_id")
DeveloperNotFoundHTTPException = _make_not_found("Разработчик",   "developer_id")

# Domain

class ObjectAlreadyExistsError(Exception):
    def __init__(self, constraint: str | None = None):
        self.constraint = constraint
        super().__init__()

class ObjectNotFoundError(Exception):
    pass

class AuthenticationError(Exception):
    pass
