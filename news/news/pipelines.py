import pymongo
from news.mongo_provider import MongoProvider


class MongoPipeline(object):

	def __init__(self, settings):
		self.mongo_provider = MongoProvider(
			settings.get('MONGO_URI'),
			settings.get('MONGO_DATABSE')
		)

	@classmethod
	def from_crawler(cls, crawler):
		return cls(crawler.settings)

	def open_spider(self, spider):
		self.collection = self.mongo_provider.get_collection()

	def close_spider(self, spider):
		self.mongo_provider.close_connection()

	def process_item(self, item, spider):
		self.collection.find_one_and_update(
			{"link": item["link"]},
			{"$set": dict(item)},
			upsert=True
		)
		return item