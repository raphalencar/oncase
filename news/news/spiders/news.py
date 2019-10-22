import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings
from news.items import TecmundoItem, TecnoblogItem
import re

class TecmundoSpider(scrapy.Spider):
	name = 'Tecmundo'
	allowed_domains = ['tecmundo.com.br']
	start_urls = ['http://tecmundo.com.br/novidades']

	def __init__(self, limit_pages=None, *args, **kwargs):
		super(TecmundoSpider, self).__init__(*args, **kwargs)
		if limit_pages is not None:
			self.limit_pages = int(limit_pages)
		else:
			self.limit_pages = 0

	def parse(self, response):
		for article in response.xpath('//*[@id="js-main"]//article//a[contains(@class, "tec--card__title__link")]/@href'):
			# Pegando dados de cada noticia específica
			link = article.get()

			yield response.follow(link, self.parse_article)

		# mais noticias    
		more = response.xpath('//*[@id="js-main"]//div[contains(@class, "tec--list tec--list--lg")]/a/@href')
		if more:
			next_page_url = more.get()

			# url de exemplo tecmundo.com.br/novidades?page=2
			match = re.match(r".*\/?page=(\d+)", next_page_url)
			next_page_number = int(match.groups()[0])

			if next_page_number <= self.limit_pages:
				yield response.follow(next_page_url)

	def parse_article(self, response):
		l = ItemLoader(item=TecmundoItem(), response=response)

		# utilizando xpath para retornar os campos 
		l.add_value('link', response.url)
		l.add_xpath('title', '//*[@id="js-article-title"]/text()')
		l.add_xpath('author', '//*[@id="js-author-bar"]//a[contains(@class, "tec--author__info__link")]/text()')
		l.add_xpath('date', '//*[@id="js-article-date"]/strong/text()')
		l.add_xpath('text', '//*[@id="js-main"]//div[contains(@class, "tec--article__body")]/p//text()') 
		l.add_xpath('tag', '//*[@id="js-categories"]/a/text()')

		return l.load_item()

class TecnoblogSpider(scrapy.Spider):
	name = 'Tecnoblog'
	allowed_domains = ['tecnoblog.net']
	start_urls = ['http://tecnoblog.net/categoria/news']

	def __init__(self, limit_pages=None, *args, **kwargs):
		super(TecnoblogSpider, self).__init__(*args, **kwargs)
		if limit_pages is not None:
			self.limit_pages = int(limit_pages)
		else:
			self.limit_pages = 0

	def parse(self, response):
		for article in response.xpath('//*[@id="categoria"]//article//div[contains(@class, "texts")]//h2/a/@href'):
	        # Pegando dados de cada noticia específica
			link = article.get()
			yield response.follow(link, self.parse_article)

		# mais noticias
		more = response.xpath('//*[@id="mais"]/@href')
		if more:
			next_page_url = more.get()

			# url de exemplo tecnoblog.net/categoria/news/page/2/
			match = re.match(r".*\/page\/(\d+)\/", next_page_url)
			next_page_number = int(match.groups()[0])

			if next_page_number <= self.limit_pages:
				yield response.follow(next_page_url)

	def parse_article(self, response):
		l = ItemLoader(item=TecnoblogItem(), response=response)

		# utilizando xpath para retornar os campos	
		l.add_value('link', response.url)
		l.add_xpath('title', '//*[@id="post"]/header/div/h1/a/text()')
		l.add_xpath('author', '//*[@id="author-single"]/a/text()')
		l.add_xpath('date', '//*[@id="post"]/header//span/text()[2]')
		l.add_xpath('text', '//*[@id="post"]//p//text()') 
		l.add_xpath('tag', '//*[@id="post"]//div[contains(@class, "tags")]/a[contains(@rel, "tag")]/text()')

		return l.load_item()

process = CrawlerProcess(get_project_settings())
process.crawl(TecmundoSpider, limit_pages=1)
process.crawl(TecnoblogSpider, limit_pages=2)
process.start()
