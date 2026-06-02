from enum import Enum
from typing import Annotated, Optional

from fastapi import Query
from pydantic import BaseModel


class GameSort(str, Enum):
    """Варианты сортировки каталога игр."""
    CHEAP = "cheap"                # сначала дешёвые
    EXPENSIVE = "expensive"        # сначала дорогие
    DISCOUNT = "discount"          # сначала с большей скидкой
    TITLE_ASC = "title_asc"
    TITLE_DESC = "title_desc"
    POPULARITY = "popularity"       # больше всего отзывов
    RATING = "rating"              # выше % положительных
    RELEASE_NEW = "release_new"    # сначала новые
    RELEASE_OLD = "release_old"    # сначала старые
    PUBLISHER_ASC = "publisher_asc"
    PUBLISHER_DESC = "publisher_desc"


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

            publishers: Annotated[
                Optional[list[str]],
                Query(
                    description="Фильтр по издателям",
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
                Optional[GameSort],
                Query(description="Сортировка каталога"),
            ] = None,
    ):
        self.title = title
        self.stores = stores
        self.platforms = platforms
        self.genres = genres
        self.publishers = publishers
        self.price_min = price_min
        self.price_max = price_max
        self.sort = sort
