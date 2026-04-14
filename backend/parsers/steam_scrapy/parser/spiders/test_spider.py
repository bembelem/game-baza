import scrapy


class TestSpider(scrapy.Spider):
    name = "parse_quotes"
    start_urls = ["https://quotes.toscrape.com/tag/books/"]

    def parse(self, response, **kwargs):
        quotes: list[scrapy.Selector] = response.css('div.quote')
        for quote in quotes:
            yield {
                "author": quote.css("span.author::text").get(),
                'text': quote.css("span.text::text").get()
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

