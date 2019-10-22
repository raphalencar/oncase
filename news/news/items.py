import scrapy
from scrapy.loader.processors import Join
import re


def strip_processor(values):
	for v in values:
		return v.strip()

def get_correct_date_value(values):
	for v in values:
		match = re.search(r'(\d+/\d+/\d+)', v)
		if match is not None:
			return match[0]

class TecmundoItem(scrapy.Item):
    # definindo os campos
	link = scrapy.Field(
		output_processor=Join()
	)
	title = scrapy.Field(
		output_processor=Join()
	)
	author = scrapy.Field(
		input_processor=strip_processor,
		output_processor=Join()
	)
	date = scrapy.Field(
		output_processor=Join()
	)
	text = scrapy.Field(
		output_processor=Join("")
	)
	tag = scrapy.Field()

class TecnoblogItem(scrapy.Item):
	 # definindo os campos
	link = scrapy.Field(
		output_processor=Join()
	)
	title = scrapy.Field(
		output_processor=Join()
	)
	author = scrapy.Field(
		input_processor=strip_processor,
		output_processor=Join()
	)
	date = scrapy.Field(
		input_processor=get_correct_date_value,
		output_processor=Join()
	)
	text = scrapy.Field(
		output_processor=Join("")
	)

