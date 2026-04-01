from fastapi import HTTPException


class GameBazaException(Exception):
    detail = "Unexpected error"

    def __init__(self, *args, **kwargs):
        super().__init__(self.detail, *args, **kwargs)


class ObjectAlreadyExistsException(GameBazaException):
    detail = "Similar object already exists"

class UserAlreadyExistsException(ObjectAlreadyExistsException):
    detail = "User already exists"

class EmailNotRegisteredException(GameBazaException):
    detail = "User with this email is not registered"

class IncorrectPasswordException(GameBazaException):
    detail = "Incorrect password"

class IncorrectTokenException(GameBazaException):
    detail = "Invalid token"


class AppHTTPException(HTTPException):
    status_code = 500
    detail: str

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserEmailAlreadyExistsHTTPException(AppHTTPException):
    status_code = 409
    detail = "User with this email already exists"

class EmailNotRegisteredHTTPException(AppHTTPException):
    status_code = 401
    detail = "User with this email is not registered"

class IncorrectPasswordHTTPException(AppHTTPException):
    status_code = 401
    detail = "Incorrect password"

class IncorrectTokenHTTPException(AppHTTPException):
    status_code = 401
    detail = "Invalid token"