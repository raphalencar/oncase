import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.utils.project import get_project_settings
from news.items import TecmundoItem

class TecmundoSpider(scrapy.Spider):
    name = 'Tecmundo'
    allowed_domains = ['tecmundo.com.br']
    start_urls = ['http://tecmundo.com.br/novidades']

    def parse(self, response):
        for article in response.xpath('//*[@id="js-main"]//article//a[contains(@class, "tec--card__title__link")]/@href'):
            # Pegando dados de cada noticia específica
            link = article.get()
           
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

# class TecnoblogSpider(scrapy.Spider):
# 	name = 'Tecnoblog'
#     allowed_domains = ['tecnoblog.net']
#     start_urls = ['http://tecnoblog.net/categoria/news']

# process = CrawlerProcess(get_project_settings())
# process.crawl(TecmundoSpider)
# process.start()