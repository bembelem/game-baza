from fastapi import APIRouter

from app.api.dependencies import GameFiltersDep, PaginationDep
from app.api.schemas.games import GameDetails, GamesPage, ReviewsResponse
from app.services.games import GamesService

router = APIRouter(prefix="/games", tags=["Games"])
games_service = GamesService()


@router.get(
    "",
    response_model=GamesPage,
    summary="Список игр",
    description="Возвращает постраничный список игр с минимальными ценами. "
                "Поддерживает фильтрацию и курсорную пагинацию.",
    responses={
        422: {"description": "Ошибка валидации параметров"},
    },
)
async def get_games(
    pagination: PaginationDep,
    filters: GameFiltersDep,
):
    return await games_service.get_games_page(filters=filters, pagination=pagination)


@router.get(
    "/{game_id}",
    response_model=GameDetails,
    summary="Информация об игре",
    description="Возвращает детальную информацию об игре: описание, жанры, "
                "разработчика, издателя и офферы по магазинам.",
    responses={
        404: {"description": "Игра не найдена"},
        422: {"description": "Ошибка валидации"},
    },
)
async def get_game(game_id: int):
    return await games_service.get_game_details(game_id)


@router.get(
    "/{game_id}/reviews",
    response_model=ReviewsResponse,
    summary="Отзывы об игре",
    description="Возвращает отзывы пользователей об игре.",
    responses={
        404: {"description": "Игра не найдена"},
    },
)
async def get_reviews(game_id: int):
    return await games_service.get_reviews(game_id)
