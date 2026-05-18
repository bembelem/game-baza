from datetime import date
from typing import List, Optional, Annotated

from fastapi import Query
from fastapi.openapi.models import Example
from pydantic import BaseModel

from app.api.schemas.offers import Offer


class Game(BaseModel):
    id: int
    title: str
    image_url: str
    min_price_original: int
    min_price_discount: int
    discount_percent: int

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "id": 1,
                "title": "Cyberpunk 2077",
                "image_url": "https://example.com/cyberpunk.jpg",
                "min_price_original": 2999,
                "min_price_discount": 1499,
                "discount_percent": 50,
            }]
        }
    }


class GamesPage(BaseModel):
    total: int
    last_id: int | None
    per_page: int
    has_more: bool
    items: List[Game]


class GameFilters:

    def __init__(
            self,
            title: Annotated[
                Optional[str],
                Query(
                    description="Поиск по названию игры",
                    max_length=100,
                )
            ] = None,

            stores: Annotated[
                Optional[list[str]],
                Query(
                    description="Фильтр по магазинам",
                )
            ] = None,

            platforms: Annotated[
                Optional[list[str]],
                Query(
                    description="Фильтр по платформам",
                )
            ] = None,

            genres: Annotated[
                Optional[list[str]],
                Query(
                    description="Фильтр по жанрам",
                )
            ] = None,

            price_min: Annotated[
                Optional[int],
                Query(
                    ge=0,
                    le=999999,
                    description="Минимальная цена в рублях",
                )
            ] = None,

            price_max: Annotated[
                Optional[int],
                Query(
                    ge=0,
                    le=999999,
                    description="Максимальная цена в рублях",
                )
            ] = None,

            sort: Annotated[
                Optional[str],
                Query(
                    description="Сортировка: price_asc, price_desc, title_asc, title_desc",
                    openapi_examples={
                        "1": Example(summary="Сначала дешевле", value="price_asc"),
                        "2": Example(summary="Сначала дороже", value="price_desc"),
                        "3": Example(summary="По названию А-Я", value="title_asc"),
                        "4": Example(summary="По названию Я-А", value="title_desc"),
                    }
                )
            ] = None,
    ):
        self.title = title
        self.stores = stores
        self.platforms = platforms
        self.genres = genres
        self.price_min = price_min
        self.price_max = price_max
        self.sort = sort


class GameDetails(Game):
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