from fastapi import APIRouter, Response
from mypyc.ir.ops import Register

from app.api.controllers.examples.responses import REGISTER_RESPONSES, LOGIN_RESPONSES
from app.api.schemas.auth import UserRequestAdd, Token, UserRequestLogin
from app.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()


@router.post(
    path="/register",
    status_code=201,
    response_model=Token,
    responses=REGISTER_RESPONSES,
)
async def register_user(response: Response, data: UserRequestAdd):
    user = await auth_service.register_user(data)
    access_token = auth_service.create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}

@router.post(
    path="/login",
    status_code=201,
    response_model=Token,
    responses=LOGIN_RESPONSES,
)
async def login(response: Response, data: UserRequestLogin):
    user = await auth_service.login_user(data)
    access_token = auth_service.create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}