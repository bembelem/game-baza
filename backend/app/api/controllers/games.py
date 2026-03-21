from fastapi import APIRouter
from typing import Annotated
from fastapi import Depends

from backend.app.api.dependencies import PaginationDep, GameFiltersDep
from backend.app.api.schemas.games import GamesPage, GameDetails, GameFilters, Game
from backend.app.api.schemas.games import ReviewsResponse, Review

router = APIRouter(prefix="/games", tags=["Games"])

@router.get(
    "/",
    response_model=GamesPage,
    summary="Список игр",
    description="Возвращает постраничный список игр с минимальными ценами. Поддерживает фильтрацию и пагинацию.",
    responses={
        422: {"description": "Ошибка валидации параметров"},
    }
)
async def get_games(
    pagination: PaginationDep,
    filters: GameFiltersDep,
):
    ...

@router.get(
    "/{game_id}",
    response_model=GameDetails,
    summary="Информация об игре",
    description="Возвращает детальную информацию об игре: описание, жанры, платформы и офферы по магазинам.",
    responses={
        404: {"description": "Игра не найдена"},
        422: {"description": "Ошибка валидации"},
    }
)
async def get_game(game_id: int):
    ...

@router.get(
    "/{game_id}/reviews",
    response_model=ReviewsResponse,
    summary="Отзывы о игре",
    description="Возвращает отзывы о игре.",
)

async def get_reviews(game_id: int):
    ...
