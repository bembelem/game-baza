"""Реализованные эндпоинты пользователя."""
from fastapi import APIRouter, Response

from app.api.controllers.examples.responses import ME_RESPONSES, MessageResponse
from app.api.dependencies import UserIdDep
from app.api.schemas.users import User, UserPatch
from app.repositories.users import UserRepository
from app.services.auth import AuthService
from database.database import async_session_maker

router = APIRouter(prefix="/users", tags=["Users"])
auth_service = AuthService()


@router.get(
    "/me",
    response_model=User,
    status_code=200,
    summary="Мой профиль",
    responses=ME_RESPONSES,
)
async def me(user_id: UserIdDep):
    async with async_session_maker() as session:
        user = await UserRepository(session).get_one_or_none(id=user_id)
    return user


@router.patch(
    "/me",
    response_model=User,
    status_code=200,
    summary="Изменить профиль",
    description="Частично обновляет профиль авторизованного пользователя. "
                "Поля передаются опционально, пустые игнорируются. ",
    responses={
        **ME_RESPONSES,
        409: {"description": "Email или username уже занят"},
    },
)
async def patch_me(body: UserPatch, user_id: UserIdDep):
    return await auth_service.update_user(user_id, body)


@router.delete(
    "/me",
    response_model=MessageResponse,
    status_code=200,
    summary="Удалить профиль",
    description="Удаляет профиль авторизованного пользователя и сбрасывает cookie.",
    responses=ME_RESPONSES,
)
async def delete_me(response: Response, user_id: UserIdDep):
    await auth_service.delete_user(user_id)
    response.delete_cookie("access_token")
    return MessageResponse(message="Профиль удалён")
