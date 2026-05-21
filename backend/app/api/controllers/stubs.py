"""Эндпоинты-заглушки"""
from typing import Any

from fastapi import APIRouter, Path

from app.services.schemas.offers import Offer, OfferPrices
from app.services.schemas.users import UserPublic, Wishlist

UNAUTHORIZED: dict[int | str, dict[str, Any]] = {
    401: {"description": "Не авторизован, токен отсутствует или недействителен"}
}
NOT_FOUND_USER: dict[int | str, dict[str, Any]] = {
    404: {"description": "Пользователь не найден"}
}


# Offers

router_offers = APIRouter(prefix="/offers", tags=["Offers"])


@router_offers.get(
    "/{offer_id}",
    response_model=Offer,
    summary="Оффер магазина",
    description="Возвращает информацию о конкретном оффере по его ID.",
)
def get_offer(offer_id: int = Path(description="ID оффера")):
    ...


@router_offers.get(
    "/{offer_id}/price-history",
    response_model=OfferPrices,
    summary="История цен оффера",
    description="Возвращает историю изменения цены для конкретного оффера.",
)
def get_offer_price_history(offer_id: int = Path(description="ID оффера")):
    ...


# Users

router_users = APIRouter(prefix="/users", tags=["Users"])


@router_users.get(
    "/{user_id}",
    response_model=UserPublic,
    summary="Публичный профиль пользователя",
    description="Возвращает публичный профиль пользователя по его ID.",
    responses={**NOT_FOUND_USER},
)
async def get_user(user_id: int = Path(description="ID пользователя")):
    ...


@router_users.get(
    "/{user_id}/wishlist",
    response_model=Wishlist,
    summary="Вишлист пользователя",
    description="Возвращает список игр в вишлисте пользователя по его ID.",
    responses={**NOT_FOUND_USER},
)
async def get_user_wishlist(user_id: int = Path(description="ID пользователя")):
    ...


@router_users.post(
    "/me/wishlist/{game_id}",
    summary="Добавить игру в вишлист",
    description="Добавляет игру по её ID в вишлист авторизованного пользователя.",
    responses={
        **UNAUTHORIZED,
        404: {"description": "Игра не найдена"},
        409: {"description": "Игра уже в вишлисте"},
    },
)
async def add_to_wishlist(game_id: int = Path(description="ID игры")):
    ...


@router_users.delete(
    "/me/wishlist/{game_id}",
    summary="Убрать игру из вишлиста",
    description="Удаляет игру по её ID из вишлиста авторизованного пользователя.",
    responses={
        **UNAUTHORIZED,
        404: {"description": "Игра не найдена в вишлисте"},
    },
)
async def remove_from_wishlist(game_id: int = Path(description="ID игры")):
    ...
