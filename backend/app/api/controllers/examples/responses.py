from pydantic import BaseModel

from app.exceptions import EmailNotRegisteredHTTPException, IncorrectPasswordHTTPException, \
    UserEmailAlreadyExistsHTTPException


class ErrorResponse(BaseModel):
    detail: str


class ValidationErrorResponse(BaseModel):
    detail: str


REGISTER_RESPONSES = {
    409: {
        "description": "User already exists",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "example": {"detail": UserEmailAlreadyExistsHTTPException.detail}
            }
        }
    },
    422: {
        "description": "Validation error",
        "model": ValidationErrorResponse,
        "content": {
            "application/json": {
                "examples": {
                    "invalid_email": {
                        "summary": "Invalid email",
                        "value": {"detail": "email: value is not a valid email address"}
                    },
                    "invalid_birthdate": {
                        "summary": "Birthdate is in the future",
                        "value": {"detail": "birthdate: Birthdate must be in the past"}
                    },
                }
            }
        }
    },
}

LOGIN_RESPONSES = {
    401: {
        "description": "Invalid email or password",
        "model": ErrorResponse,
        "content": {
            "application/json": {
                "examples": {
                    "email_not_registered": {
                        "summary": "Email is not registered",
                        "value": {"detail": EmailNotRegisteredHTTPException.detail}
                    },
                    "incorrect_password": {
                        "summary": "Incorrect password",
                        "value": {"detail": IncorrectPasswordHTTPException.detail}
                    },
                }
            }
        }
    },
    422: {
        "description": "Validation error",
        "model": ValidationErrorResponse,
        "content": {
            "application/json": {
                "examples": {
                    "invalid_email": {
                        "summary": "Invalid email",
                        "value": {"detail": "email: value is not a valid email address"}
                    },
                }
            }
        }
    },
}