import uuid
from fastapi import HTTPException

class AppHTTPException(HTTPException):
    status_code: int = 500
    error_code:  str = "5000_INTERNAL_ERROR"
    message:     str = "Внутренняя ошибка сервера."
    details:     dict = {}

    def __init__(self, details: dict | None = None, trace_id: str | None = None):
        self.details  = details or self.details
        self.trace_id = trace_id or str(uuid.uuid4())
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
    error_code = "2011_IncorrectToken_ERROR"
    status_code = 401
    message = "Токен не передан или не действителен."

# Доменные ошибки
class ObjectAlreadyExistsError(Exception):
    def __init__(self, constraint: str | None = None):
        self.constraint = constraint
        super().__init__()

class ObjectNotFoundError(Exception):
    pass

class AuthenticationError(Exception):
    pass