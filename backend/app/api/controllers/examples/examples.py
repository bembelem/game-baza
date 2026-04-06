from fastapi.openapi.models import Example

REGISTER_EXAMPLES = {
    "1": Example(
        summary="Обычный пользователь",
        value={
            "username": "john doe",
            "email": "john@example.com",
            "password": "SecurePass123!",
            "birthdate": "2026-03-30"
        },
    )
}

LOGIN_EXAMPLES = {
    "1": Example(
        summary="Вход по email",
        value={
            "email": "john@example.com",
            "password": "SecurePass123!",
        },
    ),
    "2": Example(
            summary="Вход по username",
            value={
                "username": "john doe",
                "password": "SecurePass123!",
            },
        ),
}
