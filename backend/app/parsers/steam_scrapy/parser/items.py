# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from dataclasses import dataclass

@dataclass
class SteamGameItem:
    title: str
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
