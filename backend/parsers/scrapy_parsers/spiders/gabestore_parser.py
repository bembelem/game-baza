import scrapy
import json
import logging
import re
from urllib.parse import urlencode


class GabestoreSpider(scrapy.Spider):
    name = "gabestore_spider"
    store_name = "gabestore"

    def __init__(self, *args, **kwargs):
        logging.getLogger("scrapy_parsers").setLevel(logging.INFO)
        logging.getLogger("twisted").setLevel(logging.INFO)
        super().__init__(*args, **kwargs)

    custom_settings = {
        "CONCURRENT_REQUESTS": 8,
        "DOWNLOAD_DELAY": 0.5,
        "AUTOTHROTTLE_ENABLED": True,
        "COOKIES_ENABLED": True,
        "ROBOTSTXT_OBEY": False,
        "LOG_LEVEL": "INFO",
        "FEED_EXPORT_ENCODING": "utf-8",
        }

    catalog_url = "https://gabestore.ru/catalog?" + urlencode({
        "series": "",
        "ProductFilter[sortName]": "views",
        "ProductFilter[priceRange]": "",
        "ProductFilter[priceFrom]": "",
        "ProductFilter[priceTo]": "",
        "ProductFilter[available]": "1",
    })

    next_url = "https://gabestore.ru/search/next"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "ru-RU,ru;q=0.9",
    }

    def start_requests(self):
        yield scrapy.Request(
            self.catalog_url,
            callback=self.parse_catalog_html,
            headers=self.headers,
        )

    def parse_catalog_html(self, response):
        yield from self.parse_items(response)

        next_page = response.css("button.js-load-more::attr(data-page)").get()
        if next_page:
            yield self._next_page_request(int(next_page))

    def parse_next_json(self, response):
        data = json.loads(response.text)
        html_block = data.get("html", "")

        if not html_block or not html_block.strip():
            return

        selector = scrapy.Selector(text=html_block)
        yield from self.parse_items(selector)

        # Если карточки есть — запрашиваем следующую страницу
        if selector.css("div.shop-item"):
            page = response.meta["page"]
            yield self._next_page_request(page + 1)

    def _next_page_request(self, page: int):
        params = urlencode({
            "series": "",
            "ProductFilter[available]": "1",
            "ProductFilter[sortName]": "views",
            "page": page,
        })
        return scrapy.Request(
            f"{self.next_url}?{params}",
            callback=self.parse_next_json,
            headers={**self.headers, "X-Requested-With": "XMLHttpRequest"},
            meta={"page": page},
        )

    def parse_items(self, selector):
        for card in selector.css("div.shop-item"):
            link = card.css("a.shop-item__image::attr(href)").get()
            if not link:
                continue

            item = self.parse_card(card, link)
            yield scrapy.Request(
                f"https://gabestore.ru{link}",
                callback=self.parse_game_page,
                meta={"item": item},
                headers=self.headers,
            )

    def parse_card(self, card, link: str) -> dict:
        # С карточки берём только то, что не дублируется на странице игры.
        # Цена/жанры/издатель/дата — со страницы игры (там разметка полнее
        # и корректнее: на карточке нет «старой» цены и реальных жанров).
        return {
            "title": card.css("a.shop-item__name::text").get("").strip(),
            "link": f"https://gabestore.ru{link}",
            "image_url": card.css("a.shop-item__image img::attr(src)").get(),
        }

    def parse_game_page(self, response):
        item = response.meta["item"]

        # Характеристики: таблица label → value (.b-card__table-item).
        table: dict[str, list[str]] = {}
        for row in response.css(".b-card__table-item"):
            label = row.css(".b-card__table-title::text").get("").strip()
            values = [
                t.strip()
                for t in row.css(
                    ".b-card__table-value a::text, "
                    ".b-card__table-value span::text, "
                    ".b-card__table-value::text"
                ).getall()
                if t.strip()
            ]
            if label:
                table[label] = values

        # Жанры берём ИЗ таблицы карточки, а не из a[href*=genre] —
        # иначе в выдачу попадало всё меню навигации (Экшен…Гонки).
        item["genres"] = table.get("Жанр", [])
        item["platforms"] = table.get("Платформа", [])
        item["publisher"] = self._first(table.get("Издатель"))
        item["developer"] = self._first(table.get("Разработчик"))
        item["released"] = self._first(table.get("Дата выхода"))  # "15 февраля 2019"

        # Цены: oldprice — «до скидки», currentprice — к оплате.
        # Если скидки нет, oldprice отсутствует → original = discount.
        current = (response.css(".b-card__price-currentprice::text").get() or "").strip()
        old = (response.css(".b-card__price-oldprice::text").get() or "").strip()
        item["price_discount"] = current or None
        item["price_original"] = old or current or None
        disc = response.css(".b-card__price-discount::text").get("")
        item["discount_percent"] = re.sub(r"\D", "", disc) or None  # "-78%" → "78"

        desc_parts = response.css(".b-card__tabdescription ::text").getall()
        item["description"] = "\n".join(t.strip() for t in desc_parts if t.strip()) or None

        yield item

    @staticmethod
    def _first(values: list[str] | None) -> str | None:
        return values[0] if values else None