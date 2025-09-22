# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from transformation.normalization.cars import normalize_name
import pymongo
from datetime import datetime


class MongoDBPipeline:
    def __init__(self, mongo_uri, mongo_db, batch_size=50):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.batch_size = batch_size
        self.buffers = {}
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
        # Flush remaining items per collection
        for collection_name, buffer in self.buffers.items():
            if buffer:
                self.db[collection_name].insert_many(buffer)
        # close connection when spider finishes
        self.client.close()

    def process_item(self, item, spider):
        collection_name = item.get("collection") or spider.collection_to_use
        collection_to_item = {}
        #copy item without "collection" field
        items_to_store = dict(item)
        items_to_store.pop("collection",None)
        
        if collection_name == "manufacturers":
            if self.db[collection_name].find_one({"name":normalize_name(items_to_store["name"])}):
                return item
            else:
                collection_to_item[collection_name] = items_to_store
        else:
            result = self.db[collection_name].find_one({"url":items_to_store["url"]},{"_id":1})
            if result:
                items_to_store = {"url":items_to_store["url"],"price":items_to_store["price"],"car_id":result["_id"],"timestamp":datetime.utcnow()}
                collection_to_item["price_history"]=items_to_store
            else:
                items_to_store_in_price_history = {"url":items_to_store["url"],"price":items_to_store["price"],"timestamp":datetime.utcnow()}
                collection_to_item["price_history"]=items_to_store_in_price_history
                items_to_store.pop("price",None)
                collection_to_item[collection_name] = items_to_store
                
        for collection , data in collection_to_item.items():
            if collection not in self.buffers:
                self.buffers[collection] = []

            self.buffers[collection].append(dict(data))
            
        for collection in self.buffers:
            if len(self.buffers[collection]) >= self.batch_size:
                self.db[collection].insert_many(self.buffers[collection])
                self.buffers[collection] = []
        return item
