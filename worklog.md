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

- Persistindo os dados no MongoDB. Criação da pipeline para armazenamento e update dos dados:
```python
# pipelines.py

class MongoPipeline(object):

	collection_name = 'tc_news'

	def __init__(self, mongo_uri, mongo_db):
	    self.mongo_uri = mongo_uri
	    self.mongo_db = mongo_db

	@classmethod
	def from_crawler(cls, crawler):
	    return cls(
	        mongo_uri=crawler.settings.get('MONGO_URI'),
	        mongo_db=crawler.settings.get('MONGO_DATABASE', 'news')
	    )

	def open_spider(self, spider):
	    self.client = pymongo.MongoClient(self.mongo_uri)
	    self.db = self.client[self.mongo_db]

	def close_spider(self, spider):
	    self.client.close()
    
    # update se o item ja existir
	def process_item(self, item, spider):
		self.db[self.collection_name].find_one_and_update(
		    {"link": item["link"]},
		    {"$set": dict(item)},
		    upsert=True
		)
		return item
        
# settings.py

# MongoDB Pipeline
ITEM_PIPELINES = {
   'news.pipelines.MongoPipeline': 300,
}
```

- Desativando COOKIES para não ser banido devido ao numero de requests
```python
# settings.py

# Disable cookies (enabled by default)
COOKIES_ENABLED = False
```

- Utilização da Core API do Scrapy para executar os dois spiders no mesmo processo simultaneamente
```python
process = CrawlerProcess(get_project_settings())
process.crawl(TecmundoSpider, limit_pages=60)
process.crawl(TecnoblogSpider, limit_pages=100)
process.start()
```

### Análise dos dados
Todas as análises estão presentes em [report.html](https://github.com/raphalencar/oncase/blob/master/report.html)

Exemplo de métrica utilizada:
O índices de **Flesch-Kincaid** pode ser usado como uma métrica de legibilidade de um artigo.

Formula Flesch-Kincaid: Reading Ease score = 206.835 - (1.015 × ASL) - (84.6 × ASW)

sendo: 
1) ASL = duração média de uma sentença (número de palavras dividido pelo número de senteças) 
2) ASW = comprimento médio das palavras em sílabas (número de sílabas dividido pelo número de palavras)

seguindo a seguinte tabela:

**Score Difficulty**
90-100 Very Easy
80-89 Easy
70-79 Fairly Easy
60-69 Standard
50-59 Fairly Difficult
30-49 Difficult
0-29 Very Confusing

- Utilizando essa métrica para comparar os artigos do Tecmundo e Tecnoblog com a tag **netflix**
```python
from textstat import flesch_reading_ease

tcm['fk_score'] = tcm['text'].map(lambda text: flesch_reading_ease(text)) 
tcb['fk_score'] = tcb['text'].map(lambda text: flesch_reading_ease(text))

print('Score médio Tecmundo: {0:.2f}'.format(tcm['fk_score'].mean()))
print('Score médio Tecnoblog: {0:.2f}'.format(tcb['fk_score'].mean()))
```
output: Score médio Tecmundo: 24.35
        Score médio Tecnoblog: 20.16

Tecnoblog aparenta ser um pouco mais confuso em média.

### Estratégias para escalar a solução
1. Utilizar [Google cache](http://www.googleguide.com/cached_pages.html) para buscar as páginas, ao invés de bater diretamente nelas
2. Utilizar um pool de IPs rotativos para não ser banido 

### Estratégias de deploy
1. Realizar o Deploy no [ScrapingHub](https://scrapinghub.com/) que permite agendar spiders diferentes a cada 5 minutos
2. Construir uma RESTful Flask API para deploy no Heroku