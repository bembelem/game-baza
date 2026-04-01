from fastapi import HTTPException


class GameBazaException(Exception):
    detail = "Неожиданная ошибка"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectAlreadyExistsException(GameBazaException):
    detail = "Похожий объект уже существует"

class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "Пользователь уже существует"

class EmailNotRegisteredException(GameBazaException):
    detail = "Пользователь с таким email не зарегистрирован"

class IncorrectPasswordException(GameBazaException):
    detail = "Пароль неверный"

class IncorrectTokenException(GameBazaException):
    detail = "Некорректный токен"


class AppHTTPException(HTTPException):
    status_code = 500
    detail: str

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserEmailAlreadyExistsHTTPException(AppHTTPException):
    status_code = 409
    detail = "Пользователь с такой почтой уже существует"

class EmailNotRegisteredHTTPException(AppHTTPException):
    status_code = 401
    detail = "Пользователь с таким email не зарегистрирован"

class IncorrectPasswordHTTPException(AppHTTPException):
    status_code = 401
    detail = "Пароль неверный"

class IncorrectTokenHTTPException(AppHTTPException):
    status_code = 401
    detail = "Некорректный токен"