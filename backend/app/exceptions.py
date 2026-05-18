from fastapi import HTTPException

from app.context import get_request_id


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
        self.details  = details if details is not None else dict(self.details)
        super().__init__(status_code=self.status_code, detail=self._build_detail())

    def _build_detail(self) -> dict:
        return {
            "error":   self.error_code,
            "message": self.message,
            "details": self.details,
            "traceId": self.trace_id,
        }


class ValidationHTTPException(AppHTTPException):
    status_code = 422
    error_code  = "2020_VALIDATION_ERROR"
    message     = "Данные не прошли валидацию."

class AuthenticationHTTPException(AppHTTPException):
    status_code = 401
    error_code  = "2010_AUTHENTICATION_ERROR"
    message     = "Ошибка авторизации."

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

class NotFoundHTTPException(AppHTTPException):
    status_code = 404
    error_code = "4040_NOT_FOUND"
    message = "Ресурс не найден."

class GameNotFoundHTTPException(NotFoundHTTPException):
    message = "Игра не найдена."
    details = {"game_id": "Игра с таким ID не существует."}

class GenreNotFoundHTTPException(NotFoundHTTPException):
    message = "Жанр не найден."
    details = {"genre_id": "Жанр с таким ID не существует."}

class StoreNotFoundHTTPException(NotFoundHTTPException):
    message = "Магазин не найден."
    details = {"store_id": "Магазин с таким ID не существует."}

class PlatformNotFoundHTTPException(NotFoundHTTPException):
    message = "Платформа не найдена."
    details = {"platform_id": "Платформа с таким ID не существует."}

class PublisherNotFoundHTTPException(NotFoundHTTPException):
    message = "Издатель не найден."
    details = {"publisher_id": "Издатель с таким ID не существует."}

class DeveloperNotFoundHTTPException(NotFoundHTTPException):
    message = "Разработчик не найден."
    details = {"developer_id": "Разработчик с таким ID не существует."}

# Доменные ошибки
class ObjectAlreadyExistsError(Exception):
    def __init__(self, constraint: str | None = None):
        self.constraint = constraint
        super().__init__()

class ObjectNotFoundError(Exception):
    pass

class AuthenticationError(Exception):
    pass
