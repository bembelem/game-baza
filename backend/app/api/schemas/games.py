from datetime import date
from typing import List

from pydantic import BaseModel

from app.services.schemas.games import GameCard
from app.services.schemas.offers import Offer


class GamesResponse(BaseModel):
    """Постраничный ответ каталога — список карточек + метаданные."""
    total: int
    last_id: int | None
    per_page: int
    has_more: bool
    items: List[GameCard]


class GameDetails(BaseModel):
    """Подробная страница игры (response для GET /games/{id})."""
    id: int
    title: str
    image_url: str
    min_price_original: int
    min_price_discount: int
    discount_percent: int
    description: str | None = None
    release_date: date | None = None
    developer: str | None = None
    publisher: str | None = None
    genres: List[str] = []
    offers: List[Offer] = []


class Review(BaseModel):
    id: int
    user_id: int
    game_id: int
    rating: int
    text: str
    created_at: str


class ReviewsResponse(BaseModel):
    reviews: list[Review] = []
