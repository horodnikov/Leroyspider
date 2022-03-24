from scrapy.settings import Settings
from scrapy.crawler import CrawlerProcess

from leroyparser import settings
from leroyparser.spiders.leroymerlin import LeroymerlinSpider


if __name__ == "__main__":
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    search = 'office'
    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LeroymerlinSpider, search=search)
    process.start()
