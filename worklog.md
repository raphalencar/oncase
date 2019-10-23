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