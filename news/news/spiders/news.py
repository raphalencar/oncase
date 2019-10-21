import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings
from news.items import TecmundoItem
from news.mongo_provider import MongoProvider

class TecmundoSpider(scrapy.Spider):
    name = 'Tecmundo'
    allowed_domains = ['tecmundo.com.br']
    start_urls = ['http://tecmundo.com.br/novidades']

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        kwargs['mongo_uri'] = crawler.settings.get('MONGO_URI')
        kwargs['mongo_database'] = crawler.settings.get('MONGO_DATABASE')
        return super(TecmundoSpider, cls).from_crawler(crawler, *args, **kwargs)

    def __init__(self, limit_pages=None, mongo_uri=None, mongo_database=None, *args, **kwargs):
        super(TecmundoSpider, self).__init__(*args, **kwargs)
        self.mongo_provider = MongoProvider(mongo_uri, mongo_database)
        self.collection = self.mongo_provider.get_collection()
        last_items = self.collection.find().sort("date", -1).limit(1)
        self.last_scraped_url = last_items[0]["link"] if last_items.count() else None

    def parse(self, response):
        for article in response.xpath('//*[@id="js-main"]//article//a[contains(@class, "tec--card__title__link")]/@href'):
            # Pegando dados de cada noticia específica
            link = article.get()
            if link == self.last_scraped_url:
                print("reached last item scraped, breaking loop")
                return

            yield response.follow(link, self.parse_article)

    def parse_article(self, response):
        l = ItemLoader(item=TecmundoItem(), response=response)

        # utilizando xpath para retornar os campos 
        l.add_value('link', response.url)
        l.add_xpath('title', '//*[@id="js-article-title"]/text()')
        l.add_xpath('author', '//*[@id="js-author-bar"]//a[contains(@class, "tec--author__info__link")]/text()')
        l.add_xpath('date', '//*[@id="js-article-date"]/strong/text()')
        l.add_xpath('text', '//*[@id="js-main"]//div[contains(@class, "tec--article__body ")]/p//text()') 
        l.add_xpath('tag', '//*[@id="js-categories"]/a/text()')

        return l.load_item()

process = CrawlerProcess(get_project_settings())
process.crawl(TecmundoSpider)
process.start()