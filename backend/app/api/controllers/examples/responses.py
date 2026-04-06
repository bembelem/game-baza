from pydantic import BaseModel


class ErrorDetailResponse(BaseModel):
    error: str
    message: str
    details: dict
    traceId: str


REGISTER_RESPONSES = {
    409: {
        "description": "Пользователь уже существует",
        "model": ErrorDetailResponse,
        "content": {
            "application/json": {
                "examples": {
                    "email_exists": {
                        "summary": "Email уже занят",
                        "value": {
                            "error": "2020_VALIDATION_ERROR",
                            "message": "Данные не прошли валидацию.",
                            "details": {"email": "Пользователь с таким email уже существует."},
                            "traceId": "9696004a-6866-4a79-bc53-f4383040cba1",
                        },
                    },
                    "username_exists": {
                        "summary": "Username уже занят",
                        "value": {
                            "error": "2020_VALIDATION_ERROR",
                            "message": "Данные не прошли валидацию.",
                            "details": {"username": "Пользователь с таким username уже существует."},
                            "traceId": "9696004a-6866-4a79-bc53-f4383040cba1",
                        },
                    },
                }
            }
        },
    },
    422: {
        "description": "Ошибка валидации",
        "model": ErrorDetailResponse,
        "content": {
            "application/json": {
                "example": {
                    "error": "2020_VALIDATION_ERROR",
                    "message": "Данные не прошли валидацию.",
                    "details": {
                        "username": "Value error, Username must be at least 3 characters",
                        "email": "value is not a valid email address: An email address must have an @-sign.",
                        "password": "Value error, Password must contain at least one uppercase letter",
                    },
                    "traceId": "12e797e6-bdfa-466b-99c8-dbb4122e7c9b",
                }
            }
        },
    },
}

LOGIN_RESPONSES = {
    401: {
        "description": "Ошибка авторизации",
        "model": ErrorDetailResponse,
        "content": {
            "application/json": {
                "examples": {
                    "email_not_registered": {
                        "summary": "Email не зарегистрирован",
                        "value": {
                            "error": "2010_AUTHENTICATION_ERROR",
                            "message": "Ошибка авторизации.",
                            "details": {"email": "Пользователь с таким email не зарегистрирован."},
                            "traceId": "9696004a-6866-4a79-bc53-f4383040cba1",
                        },
                    },
                    "incorrect_password": {
                        "summary": "Неверный пароль",
                        "value": {
                            "error": "2010_AUTHENTICATION_ERROR",
                            "message": "Ошибка авторизации.",
                            "details": {"password": "Неверный пароль."},
                            "traceId": "9696004a-6866-4a79-bc53-f4383040cba1",
                        },
                    },
                }
            }
        },
    },
    422: {
        "description": "Ошибка валидации",
        "model": ErrorDetailResponse,
        "content": {
            "application/json": {
                "example": {
                    "error": "2020_VALIDATION_ERROR",
                    "message": "Данные не прошли валидацию.",
                    "details": {
                        "email": "value is not a valid email address: An email address must have an @-sign.",
                    },
                    "traceId": "12e797e6-bdfa-466b-99c8-dbb4122e7c9b",
                }
            }
        },
    },
}