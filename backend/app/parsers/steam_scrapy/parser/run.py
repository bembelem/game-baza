from scrapy.crawler import CrawlerProcess
from spiders.steam_spider import SteamSpider

if __name__ == "__main__":

    process = CrawlerProcess()
    process.crawl(SteamSpider)
    process.start()
