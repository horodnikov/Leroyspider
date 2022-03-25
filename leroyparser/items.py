# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, MapCompose


def get_values(value):
    return value.strip()


class LeroyparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    domains = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    currency = scrapy.Field()
    characteristics = scrapy.Field()
    characteristics_keys = scrapy.Field()
    characteristics_values = scrapy.Field(input_processor=MapCompose(get_values))
