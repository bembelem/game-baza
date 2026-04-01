from fastapi import APIRouter, Body, Response

from app.api.controllers.examples.examples import register_examples, login_examples
from app.api.controllers.examples.responses import REGISTER_RESPONSES, LOGIN_RESPONSES
from app.api.schemas.auth import Token, UserRequestAdd, UserRequestLogin
from app.exceptions import UserAlreadyExistsException, UserEmailAlreadyExistsHTTPException, EmailNotRegisteredException, \
    EmailNotRegisteredHTTPException, IncorrectPasswordException, IncorrectPasswordHTTPException
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


@router.post(
    "/register",
    status_code=201,
    responses= REGISTER_RESPONSES
)
async def register_user(
        data: UserRequestAdd = Body(openapi_examples=register_examples)
):
    try:
        await auth_service.register_user(data)
    except UserAlreadyExistsException:
        raise UserEmailAlreadyExistsHTTPException()
    return {"status": "OK"}


@router.post(
    "/login",
    response_model=Token,
    responses=LOGIN_RESPONSES
)
async def login(
        response: Response,
        data: UserRequestLogin = Body(openapi_examples=login_examples),
):
    try:
        user = await auth_service.login_user(data)
    except EmailNotRegisteredException:
        raise EmailNotRegisteredHTTPException()
    except IncorrectPasswordException:
        raise IncorrectPasswordHTTPException()

    access_token = auth_service.create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}
