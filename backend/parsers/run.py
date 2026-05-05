from scrapy.crawler import CrawlerProcess
from steam_scrapy.spiders.steam_spider import SteamSpider

if __name__ == "__main__":
    process = CrawlerProcess(settings={
        "ITEM_PIPELINES": {
            "steam_scrapy.pipelines.ParserPipeline": 300,
        }
    })
    process.crawl(SteamSpider)
    process.start()