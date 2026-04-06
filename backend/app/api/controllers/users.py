from typing import Any

from fastapi import APIRouter, Request

from app.api.controllers.examples.responses import ME_RESPONSES
from app.api.dependencies import UserIdDep
from app.api.schemas.auth import UserAdd
from app.api.schemas.users import UserPatch, Wishlist, UserPublic
from app.database import async_session_maker
from app.repositories.users import UsersRepository
from app.services.auth import AuthService

router = APIRouter(prefix="/users", tags=["Users"])

UNAUTHORIZED: dict[int | str, dict[str, Any]] = {401: {"description": "Не авторизован, токен отсутствует или недействителен"}}
NOT_FOUND: dict[int | str, dict[str, Any]] = {404: {"description": "Пользователь не найден"}}

@router.get(
    path="/me",
    responses=ME_RESPONSES,
    status_code=200,
)
async def me(
        user_id: UserIdDep
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_one_or_none(id=user_id)
    return user

@router.get(
    "/{user_id}",
    response_model=UserPublic,
    summary="Публичный профиль пользователя",
    description="Возвращает публичный профиль пользователя по его ID.",
    responses={**NOT_FOUND}
)
async def get_user(user_id: int):
    ...


@router.get(
    "/{user_id}/wishlist",
    response_model=Wishlist,
    summary="Вишлист пользователя",
    description="Возвращает список игр в вишлисте пользователя по его ID.",
    responses={**NOT_FOUND}
)
async def get_user_wishlist(user_id: int):
    ...

@router.post(
    "/me/wishlist/{game_id}",
    summary="Добавить игру в вишлист",
    description="Добавляет игру по её ID в вишлист авторизованного пользователя.",
    responses={
        **UNAUTHORIZED,
        404: {"description": "Игра не найдена"},
        409: {"description": "Игра уже в вишлисте"},
    }
)
async def add_to_wishlist(game_id: int):
    ...


@router.delete(
    "/me/wishlist/{game_id}",
    summary="Убрать игру из вишлиста",
    description="Удаляет игру по её ID из вишлиста авторизованного пользователя.",
    responses={
        **UNAUTHORIZED,
        404: {"description": "Игра не найдена в вишлисте"},
    }
)
async def remove_from_wishlist(game_id: int):
    ...


@router.patch(
    "/me",
    response_model=UserAdd,
    summary="Изменить профиль",
    description="Изменяет профиль авторизованного пользователя и возвращает обновлённые данные.",
    responses={**UNAUTHORIZED}
)
async def patch_me(body: UserPatch):
    ...


@router.delete(
    "/me",
    summary="Удалить свой профиль",
    description="Удаляет профиль авторизованного пользователя.",
    responses={**UNAUTHORIZED}
)
async def delete_me():
    ...
