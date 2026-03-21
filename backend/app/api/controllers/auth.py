from fastapi import APIRouter, Body
from backend.app.api.schemas.auth import UserRegisterRequest, Token, UserLoginRequest
from backend.app.api.schemas.users import User
from backend.app.api.controllers.examples.examples import register_examples, login_examples

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/register",
    response_model=User,
    status_code=201,
    summary="Регистрация пользователя",
    description="Создаёт нового пользователя. Возвращает профиль.",
    responses={
        409: {"description": "Пользователь с таким email/username уже существует"},
        422: {"description": "Ошибка валидации"},
    }
)
async def register(
    body: UserRegisterRequest = Body(openapi_examples=register_examples)
):
    ...


@router.post(
    "/login",
    response_model=Token,
    summary="Вход в аккаунт",
    description="Возвращает JWT токен доступа.",
    responses={
        401: {"description": "Неверный email или пароль"},
        422: {"description": "Ошибка валидации"},
    }
)
async def login(
    body: UserLoginRequest = Body(openapi_examples=login_examples)
):
    ...
