from pydantic import BaseModel

class OfferItem(BaseModel):
    title: str
    normalized_title: str | None
    price_original: str | None
    discount_percent: str| None
    price_discount: str| None
    image_url: str
    released: str
    reviews_count: int
    positive_percent: str

    developer: str
    publisher: str
    description: str | None
    platforms: list[str]
    genres: list[str]
    link: str
