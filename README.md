# oncase
Crawler e Scraper de notícias

### Descrição
Processo de web crawling para estruturar dados das últimas notícias dos portais [Tecmundo](http://tecmundo.com.br/novidades) e [Tecnoblog](http://tecnoblog.net/categoria/news),
utilizando a lib [Scrapy](https://scrapy.org/) e [MongoDB](https://www.mongodb.com/) para persistência de dados.

**Autor**: Raphael Brito Alencar<br>
**Linguagem**: Python 3.7

### Build e execução

**MacOs**
1. Iniciar o servidor do Mongo
```

brew services start mongodb

```
2. Acessar o diretório **news** na pasta raíz do projeto
```

cd news/

```
3. Disparar os spiders
```

scrapy crawl

```

**Linux**
1. Iniciar o servidor do Mongo
```

sudo service mongod start

```
2. Acessar o diretório **news** na pasta raíz do projeto
```

cd news/

```
3. Disparar os spiders
```

scrapy crawl

```

### Resultados e análise dos dados
Os dados coletados dos dois websites foram utilizados em um Jupyter Notebook integrado a base de dados MongoDB. 
Todas as análises realizadas estão disponíveis no arquivo [report.html](https://github.com/raphalencar/oncase/blob/master/report.html)
de forma detalhada.
