# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


import pymongo

class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db, batch_size=50):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.batch_size = batch_size
        self.buffer = []
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get("MONGO_DATABASE"),
            batch_size=crawler.settings.get("MONGO_BATCH_SIZE",50)
        )

    def open_spider(self, spider):
        # open connection when spider starts
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        # close connection when spider finishes
        if self.buffer:
            self.db[spider.collection_to_use].insert_many(self.buffer)
            self.buffer = []
        self.client.close()

    def process_item(self, item, spider):
        self.buffer.append(dict(item)) 
        if len(self.buffer) >= self.batch_size:
            self._insert_buffer(spider)
        return item
    def _insert_buffer(self, spider):
        collection_name = spider.collection_to_use
        self.db[collection_name].insert_many(self.buffer)
        self.buffer = []