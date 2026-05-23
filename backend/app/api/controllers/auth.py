from fastapi import APIRouter, Body, Response

from app.api.controllers.examples.examples import LOGIN_EXAMPLES, REGISTER_EXAMPLES
from app.api.controllers.examples.responses import LOGIN_RESPONSES, MessageResponse, REGISTER_RESPONSES
from app.api.schemas.auth import UserLoginRequest, UserRegisterRequest
from app.services.auth import AuthService
from app.services.schemas.users import UserPrivate

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


@router.post(
    path="/register",
    status_code=201,
    response_model=UserPrivate,
    summary="Регистрация",
    description="Создаёт нового пользователя и устанавливает JWT-cookie с access_token.",
    responses=REGISTER_RESPONSES,
)
async def register(
    response: Response,
    data: UserRegisterRequest = Body(openapi_examples=REGISTER_EXAMPLES),
):
    user = await auth_service.register_user(data)
    access_token = auth_service.create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return user


@router.post(
    path="/login",
    status_code=200,
    response_model=UserPrivate,
    summary="Вход",
    description="Аутентифицирует пользователя по email или username, устанавливает JWT-cookie.",
    responses=LOGIN_RESPONSES,
)
async def login(
    response: Response,
    data: UserLoginRequest = Body(openapi_examples=LOGIN_EXAMPLES),
):
    user = await auth_service.login_user(data)
    access_token = auth_service.create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return user


@router.post(
    "/logout",
    response_model=MessageResponse,
    status_code=200,
    summary="Выход",
    description="Удаляет JWT-cookie и завершает сессию пользователя.",
)
async def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Logged out"}
