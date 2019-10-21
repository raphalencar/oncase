import scrapy
from scrapy.loader.processors import Join


def strip_processor(values):
	for v in values:
		return v.strip()

class TecmundoItem(scrapy.Item):
    # definindo os campos
	link = scrapy.Field()
	title = scrapy.Field()
	author = scrapy.Field(
		input_processor=strip_processor,
		output_processor=Join()
	)
	date = scrapy.Field()
	text = scrapy.Field(
		output_processor=Join("")
	)
	tag = scrapy.Field()
