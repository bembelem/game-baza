from pydantic import BaseModel

from app.exceptions import EmailNotRegisteredHTTPException, IncorrectPasswordHTTPException, \
    UserEmailAlreadyExistsHTTPException


class ErrorResponse(BaseModel):
    detail: str


class ValidationErrorResponse(BaseModel):
    detail: str


REGISTER_RESPONSES = {
    409: {
        "description": "Пользователь уже существует",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": UserEmailAlreadyExistsHTTPException.detail}
            }
        }
    },
    422: {
        "description": "Ошибка валидации",
        "model": ValidationErrorResponse,
        "content": {
            "application/json": {
                "examples": {
                    "invalid_email": {
                        "summary": "Невалидный email",
                        "value": {"detail": "email: value is not a valid email address"}
                    },
                    "invalid_birthdate": {
                        "summary": "Дата рождения в будущем",
                        "value": {"detail": "birthdate: Birthdate must be in the past"}
                    },
                }
            }
        }
    },
}

LOGIN_RESPONSES = {
    401: {
        "description": "Неверный email или пароль",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "examples": {
                    "email_not_registered": {
                        "summary": "Email не зарегистрирован",
                        "value": {"detail": EmailNotRegisteredHTTPException.detail}
                    },
                    "incorrect_password": {
                        "summary": "Неверный пароль",
                        "value": {"detail": IncorrectPasswordHTTPException.detail}
                    },
                }
            }
        }
    },
    422: {
        "description": "Ошибка валидации",
        "model": ValidationErrorResponse,
        "content": {
            "application/json": {
                "examples": {
                    "invalid_email": {
                        "summary": "Невалидный email",
                        "value": {"detail": "email: value is not a valid email address"}
                    },
                }
            }
        }
    },
}