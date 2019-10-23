Esse arquivo tem a função de documentar o log de trabalho para desenvolvimento do crawler.

### Construção do Crawler com Scrapy

- Criação dos dois spiders para consumir os dados de cada blog:
```python
class TecmundoSpider(scrapy.Spider):
	name = 'Tecmundo'
	allowed_domains = ['tecmundo.com.br']
	start_urls = ['http://tecmundo.com.br/novidades']
        ...
        
class TecnoblogSpider(scrapy.Spider):
	name = 'Tecnoblog'
	allowed_domains = ['tecnoblog.net']
	start_urls = ['http://tecnoblog.net/categoria/news']
        ...
```

- Adicionando o argumento de limite de páginas a serem buscadas
```python
def __init__(self, limit_pages=None, *args, **kwargs):
		super(TecmundoSpider, self).__init__(*args, **kwargs)
		if limit_pages is not None:
			self.limit_pages = int(limit_pages)
		else:
			self.limit_pages = 0

def parse(self, response):
        ...

		# mais noticias    
		more = response.xpath('//*[@id="js-main"]//div[contains(@class, "tec--list tec--list--lg")]/a/@href')
		if more:
			next_page_url = more.get()

			# url de exemplo tecmundo.com.br/novidades?page=2
			match = re.match(r".*\/?page=(\d+)", next_page_url)
			next_page_number = int(match.groups()[0])

			if next_page_number <= self.limit_pages:
				yield response.follow(next_page_url)

```

- Realizando o parse dos dados, utilizando ItemLoader, para serem armazenados de forma estruturada
```python
def parse_article(self, response):
		l = ItemLoader(item=TecmundoItem(), response=response)

		# utilizando xpath para retornar os campos 
		l.add_value('link', response.url)
		l.add_xpath('title', '//*[@id="js-article-title"]/text()')
		l.add_xpath('author', '//*[@id="js-author-bar"]//a[contains(@class, "tec--author__info__link")]/text()')
		l.add_xpath('date', '//*[@id="js-article-date"]/strong/text()')
		l.add_xpath('text', '//*[@id="js-main"]//div[contains(@class, "tec--article__body")]/p//text()') 
		l.add_xpath('tag', '//*[@id="js-categories"]/a/text()')
		l.add_value('blog', 'Tecmundo')

		return l.load_item()
        
def parse_article(self, response):
		l = ItemLoader(item=TecnoblogItem(), response=response)

		# utilizando xpath para retornar os campos	
		l.add_value('link', response.url)
		l.add_xpath('title', '//*[@id="post"]/header/div/h1/a/text()')
		l.add_xpath('author', '//*[@id="author-single"]/a/text()')
		l.add_xpath('date', '//*[@id="post"]/header//span/text()[2]')
		l.add_xpath('text', '//*[@id="post"]//p//text()') 
		l.add_xpath('tag', '//*[@id="post"]//div[contains(@class, "tags")]/a[contains(@rel, "tag")]/text()')
		l.add_value('blog', 'Tecnoblog')

		return l.load_item()
```