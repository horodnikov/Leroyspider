# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import re


MONGO_HOST = 'localhost'
MONGO_PORT = 27017
DB_NAME = 'leroy'


class LeroyparserImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        if item["photos"]:
            for photo_url in item['photos']:
                try:
                    yield scrapy.Request(photo_url)
                except Exception as exception:
                    print(exception)

    def item_completed(self, results, item, info):
        if results:
            item["photos"] = [itm[1] for itm in results]
        print()
        return item


class LeroyparserPipeline:
    def __init__(self):
        self.client = MongoClient(host=MONGO_HOST, port=MONGO_PORT)
        self.db = self.client[DB_NAME]

    def process_item(self, item, spider):
        if spider.name == 'leroymerlin':
            match = re.fullmatch(r'(\D)\s*(\d+\S+\d+)', item['price'])
            if match:
                item['currency'] = match[1]
                item['price'] = float(match[2].replace(',', ''))
            item['characteristics'] = {}
            for key, value in zip(item['characteristics_keys'],
                                  item['characteristics_values']):
                item['characteristics'][key] = value.strip()
            del item['characteristics_keys']
            del item['characteristics_values']
            collection = self.db[spider.name]
            collection.update_one(
                {'link': item['link']}, {"$set": item}, upsert=True)
        print()
        return item
