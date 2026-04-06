from fastapi import APIRouter, Response, Request, Body
from markdown_it.common.html_re import open_tag

from app.api.controllers.examples.examples import REGISTER_EXAMPLES, LOGIN_EXAMPLES
from app.api.controllers.examples.responses import REGISTER_RESPONSES, LOGIN_RESPONSES
from app.api.schemas.auth import UserRequestAdd, Token, UserRequestLogin
from app.api.schemas.users import User
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


@router.post(
    path="/register",
    status_code=201,
    response_model=User,
    responses=REGISTER_RESPONSES,
)
async def register(
        response: Response,
        data: UserRequestAdd = Body(openapi_examples=REGISTER_EXAMPLES)
):
    user = await auth_service.register_user(data)
    access_token = auth_service.create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return user

@router.post(
    path="/login",
    status_code=200,
    responses=LOGIN_RESPONSES,
)
async def login(
        response: Response,
        data: UserRequestLogin = Body(openapi_examples=LOGIN_EXAMPLES)
):
    user = await auth_service.login_user(data)
    access_token = auth_service.create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"message": "Успешный вход"}
