from typing import Annotated, Optional

from fastapi import Query
from fastapi.openapi.models import Example
from pydantic import BaseModel


class GameCard(BaseModel):
    """Карточка игры для списка (response для GET /games)."""
    id: int
    title: str
    image_url: str
    min_price_original: int
    min_price_discount: int
    discount_percent: int


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
