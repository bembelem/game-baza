custom_settings = {
    "CONCURRENT_REQUESTS": 32,
    "DOWNLOAD_DELAY": 0.1,
    "COOKIES_ENABLED": True,
    "ROBOTSTXT_OBEY": False,
    "LOG_LEVEL": "INFO",
    "FEED_EXPORT_ENCODING": "utf-8",
    "ITEM_PIPELINES": {
        "parsers.scrapy_parsers.pipelines.ParserPipeline": 300,
    },
}

