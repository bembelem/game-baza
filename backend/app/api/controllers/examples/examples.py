from fastapi.openapi.models import Example

register_examples = {
    "1": Example(
        summary="Обычный пользователь",
        value={
            "username": "john doe",
            "email": "john@example.com",
            "password": "SecurePass123!",
        },
    ),
    "2": Example(
        summary="Администратор",
        value={
            "username": "admin",
            "email": "admin@example.com",
            "password": "AdminPass456!",
        },
    ),
}

login_examples = {
    "1": Example(
        summary="Успешный вход",
        value={
            "email": "john@example.com",
            "password": "SecurePass123!",
        },
    ),
}
