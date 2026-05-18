from datetime import date

from pydantic import BaseModel


class OfferCreate(BaseModel):
    title: str
    normalized_title: str
    description: str | None = None
    released: date | None = None
    image_url: str | None = None
    link: str | None = None
    reviews_count: int | None = None
    positive_percent: int | None = None
    game_id: int
    store_id: int | None = None
    developer: str | None = None
    publisher: str | None = None
    platforms: str | None = None
    genres: str | None = None
    store_game_link: str | None = None
    price_original: int | None = None
    price_discount: int | None = None
    discount_percent: str | None = None