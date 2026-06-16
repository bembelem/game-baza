from scrapy.crawler import CrawlerProcess

from parsers.scrapy_parsers.spiders.gabestore_parser import GabestoreSpider
from scrapy_parsers.spiders.steam_spider import SteamSpider
from scrapy_parsers.spiders.steambuy_parser import SteamBuySpider

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "ITEM_PIPELINES": {
            "scrapy_parsers.pipelines.ParserPipeline": 300,
        },
        "TWISTED_REACTOR": "twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    })
    process.crawl(SteamSpider)
    process.crawl(GabestoreSpider)
    process.crawl(SteamBuySpider)
    process.start()  # запускает всех пауков параллельно