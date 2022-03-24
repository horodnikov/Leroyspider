import scrapy
from scrapy.http import HtmlResponse
from leroyparser.items import LeroyparserItem
from scrapy.loader import ItemLoader


class LeroymerlinSpider(scrapy.Spider):
    name = 'leroymerlin'
    allowed_domains = ['leroymerlin.co.za']

    def __init__(self, search):
        super(LeroymerlinSpider, self).__init__()
        self.start_urls = [
            f'https://leroymerlin.co.za/catalogsearch/result/?q={search}']

    def parse(self, response: HtmlResponse):
        items_links = response.xpath(
            "//a[contains(@class, 'product-item-photo')]/@href").getall()
        print()
        for link in items_links:
            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        loader = ItemLoader(item=LeroyparserItem(), response=response)
        loader.add_value("link", response.url)
        loader.add_xpath(
            "photos", "//img[contains(@class, 'pdp-img')]/@src")
        loader.add_xpath(
            "characteristics_keys",
            "//div[contains(@class, 'detail-info__attr')]/label/text()")
        loader.add_xpath(
            "characteristics_values",
            "//div[contains(@class, 'detail-info__attr')]/text()")
        loader.add_xpath("title", "//h1[@class = 'page-title']//text()")
        loader.add_xpath(
            "price",
            "//span[contains(@class, 'price-including-tax ')]//text()")
        print()
        yield loader.load_item()
