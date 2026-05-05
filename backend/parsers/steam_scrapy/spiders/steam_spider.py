import logging

import scrapy
import json
import re
from urllib.parse import urlencode
from scrapy.exceptions import CloseSpider

class SteamSpider(scrapy.Spider):
    name = "steam_spider"

    def __init__(self, *args, **kwargs):
        logging.getLogger("scrapy").setLevel(logging.DEBUG)
        logging.getLogger("twisted").setLevel(logging.DEBUG)
        self.seen_links = set()
        super().__init__(*args, **kwargs)

    base_url = "https://store.steampowered.com/search/results/?"

    cookies = {
        "birthtime": "568022401",
        "lastagecheckage": "1-January-1988",
        "mature_content": "1",
        "Steam_Language": "russian",
    }

    def start_requests(self):
        self.start = 0
        self.page_size = 100
        self.total_games = None

        yield scrapy.Request(
            self.build_url(self.start),
            callback=self.parse_json,
            cookies=self.cookies,
        )

    def build_url(self, start: int) -> str:
        params = {
            "start": start,
            "count": self.page_size,
            "cc": "RU",
            "l": "russian",
            "format": "json",
            "infinite": 1,
        }
        return self.base_url + urlencode(params)

    def parse_json(self, response):
        data = json.loads(response.text)
        if not data.get("success"):
            raise CloseSpider("Steam API returned no data")

        if self.total_games is None:
            self.total_games = data.get("total_count", 0)
            self.logger.info(f"Всего игр: {self.total_games}")

        html_block = data.get("results_html", "")
        if not html_block.strip():
            raise CloseSpider("Больше страниц нет")

        games = scrapy.Selector(text=html_block).css("a.search_result_row")

        for game in games:
            item = self.parse_search_result(game)
            if item and item["link"] not in self.seen_links:
                self.seen_links.add(item["link"])
                yield scrapy.Request(
                    url=item["link"],
                    callback=self.parse_game_page,
                    meta={"item": item},
                    cookies=self.cookies,
                )

        # Следующая страница
        self.start += self.page_size
        if self.start < self.total_games:
            yield scrapy.Request(
                self.build_url(self.start),
                callback=self.parse_json,
                cookies=self.cookies,
            )

    def parse_search_result(self, game):
        reviews_data = self.parse_reviews_data(game)
        prices_data = self.parse_prices(game)

        return {
            "title": game.css(".title::text").get(),
            "price_original": prices_data["price_original"],
            "discount_percent": prices_data["discount_percent"],
            "price_discount": prices_data["price_discount"],
            "image_url": game.css("div.search_capsule img::attr(src)").get(),
            "released": game.css(".search_released::text").get(default="").strip(),
            "reviews_count": reviews_data["reviews_count"],
            "positive_percent": reviews_data["positive_percent"],
            "link": game.attrib.get("href"),
        }

    def parse_game_page(self, response):
        item = response.meta["item"]
        details_block = response.css("#genresAndManufacturer")

        item["developer"] = details_block.xpath('.//div[b="Разработчик:"]/a/text()').get()
        item["publisher"] = details_block.xpath('.//div[b[contains(text(), "Издатель:")]]/a/text()').get()
        item["genres"] = details_block.xpath('.//span[@data-panel]/a/text()').getall()

        desc = response.xpath('//div[@id="game_area_description"]//text()').getall()[2:]
        desc = [t.strip() for t in desc if t.strip()]
        item["description"] = "\n".join(desc)

        yield item

    # Вспомогательные функции
    def parse_reviews_data(self, game):
        reviews_score = game.css('span.search_review_summary::attr(data-tooltip-html)').get()
        if not reviews_score:
            return {"positive_percent": None, "reviews_count": None}

        numbers = re.findall(r"[\d,]+", reviews_score)
        if len(numbers) >= 2:
            positive_percent = int(numbers[0])
            reviews_count = int(numbers[1].replace(",", ""))
        else:
            positive_percent, reviews_count = None, None

        return {"positive_percent": positive_percent, "reviews_count": reviews_count}

    def parse_prices(self, game):
        discount_block = game.css(".discount_block")
        price_discount = discount_block.css(".discount_final_price::text").get()
        price_original = discount_block.css(".discount_original_price::text").get()
        discount = discount_block.css(".discount_pct::text").get()

        if discount:
            discount = discount.replace("-", "")

        if not price_original:
            price_original = price_discount
            discount = None

        return {
            "price_original": price_original,
            "discount_percent": discount,
            "price_discount": price_discount,
        }