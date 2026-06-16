import json
import logging

import scrapy
from scrapy.exceptions import CloseSpider


class SteamBuySpider(scrapy.Spider):
    name = "steambuy_spider"
    store_name = "steambuy"

    api_url = "https://steambuy.com/sb/api/catalog"
    # og:image на странице игры = https://steammachine.ru/slider/{id_good}-339x194.jpg
    image_tmpl = "https://steammachine.ru/slider/{id}-339x194.jpg"
    page_size = 72  # столько отдаёт API на страницу

    custom_settings = {
        "CONCURRENT_REQUESTS": 8,
        "DOWNLOAD_DELAY": 0.5,
        "AUTOTHROTTLE_ENABLED": True,
        "ROBOTSTXT_OBEY": False,
        "LOG_LEVEL": "INFO",
        "FEED_EXPORT_ENCODING": "utf-8",
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "application/json",
        "Accept-Language": "ru-RU,ru;q=0.9",
        "X-Requested-With": "XMLHttpRequest",
    }

    def __init__(self, *args, **kwargs):
        logging.getLogger("scrapy_parsers").setLevel(logging.INFO)
        logging.getLogger("twisted").setLevel(logging.INFO)
        self.total = None
        super().__init__(*args, **kwargs)

    def start_requests(self):
        yield self._page_request(page=1)

    def _page_request(self, page: int):
        return scrapy.Request(
            f"{self.api_url}?q=&page={page}&sort=top_sales",
            callback=self.parse_api,
            headers=self.headers,
            meta={"page": page},
        )

    def parse_api(self, response):
        data = json.loads(response.text)
        items = data.get("items") or []

        if self.total is None:
            self.total = data.get("total", 0)
            self.logger.info(f"Всего игр: {self.total}")

        if not items:
            raise CloseSpider("Больше страниц нет")

        for raw in items:
            parsed = self.parse_item(raw)
            if parsed:
                yield parsed

        # Следующая страница: пока пришла полная пачка.
        if len(items) >= self.page_size:
            page = response.meta["page"] + 1
            yield self._page_request(page)

    def parse_item(self, raw: dict) -> dict | None:
        title = raw.get("title") or raw.get("name_good")
        if not title:
            return None

        url = raw.get("url") or ""
        link = f"https://steambuy.com{url}" if url.startswith("/") else url

        price = raw.get("price")            # текущая цена
        price_rrc = raw.get("price_rrc")    # РРЦ (как «до скидки»)
        price_original, price_discount, discount = self._prices(price, price_rrc)

        good_id = raw.get("id_good") or raw.get("id")

        return {
            "title": title,
            "link": link,
            "image_url": self.image_tmpl.format(id=good_id) if good_id else None,
            "price_original": price_original,
            "price_discount": price_discount,
            "discount_percent": discount,
            "genres": raw.get("tags") or [],
            "platforms": raw.get("platforms") or [],
            "publisher": raw.get("publisher"),
            # developer/description/отзывы API не отдаёт — оставляем пустыми,
            # дозаполнятся из других магазинов на этапе ETL (по normalized_title).
            "developer": None,
            "description": None,
            "reviews_count": None,
            "positive_percent": None,
            "released": raw.get("release_date"),  # ISO; normalize_date в пайплайне разберёт
        }

    @staticmethod
    def _prices(price, price_rrc) -> tuple[str | None, str | None, str | None]:
        """Возвращает (price_original, price_discount, discount_percent) строками.

        price_to_int в пайплайне ждёт строку, поэтому приводим к str.
        Скидку считаем только если РРЦ реально выше текущей цены.
        """
        cur = price if isinstance(price, (int, float)) and price > 0 else None
        rrc = price_rrc if isinstance(price_rrc, (int, float)) and price_rrc > 0 else None

        if cur is None:
            # цены нет — пусть будет 0/0 (price_to_int отдаст 0)
            return "0", "0", None

        if rrc and rrc > cur:
            discount = str(round((1 - cur / rrc) * 100))
            return str(rrc), str(cur), discount

        # скидки нет: original == discount
        return str(cur), str(cur), None
