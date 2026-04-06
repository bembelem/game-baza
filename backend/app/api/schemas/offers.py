from datetime import date

from pydantic import BaseModel


class Offer(BaseModel):
    id: int
    game_id: int
    store_id: int
    store_game_link: str
    price_original: int
    price_discount: int
    discount_percent: int
    positive_percent: int

class OfferPrice(BaseModel):
    id: int
    offer_id: int
    price: int
    recorded_at: date

class OfferPrices(BaseModel):
    offer_id: int
    prices_list: list[OfferPrice] = []
