import scrapy
from scrapy import Request
from WebCrawler.items import ReviewsBoursoramaItem
from datetime import datetime
import mysql.connector as mc

class BoursoramaSpider(scrapy.Spider):
    name = 'boursorama'
    allowed_domains = ['www.boursorama.com']
    start_urls = [f'https://www.boursorama.com/bourse/actions/palmares/france/page-{n}/?france_filter[market]=1rPCAC' for n in range(1,4)]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)
    
    def parse(self, response):
        liste_indices = response.css('tr.c-table__row')
        
        # Boucle qui parcours l'ensemble des éléments de la liste des indices sans le premier
        for indices in liste_indices[1:]:
            item = ReviewsBoursoramaItem()
            print(indices)
            # Indice boursier
            try:
                item['indice'] = indices.css('a.c-link::text').extract()
            except:
                item['indice'] = 'None'
            # Indice cours de l'action
            try:
                item['cours'] = indices.css('span.c-instrument::text').extract()[0]
            except:
                item['cours'] = 'None'
            # Variation de l'action
            try:
                item['var'] = indices.css('span.c-instrument::text').extract()[1]
            except:
                item['var'] = 'None'
            # Valeur la plus haute
            try:
                item['hight'] = indices.css('span.c-instrument::text').extract()[3]
            except:
                item['hight'] = 'None'
            # Valeur la plus basse
            try:
                item['low'] = indices.css('span.c-instrument::text').extract()[4]
            except:
                item['low'] = 'None'
            # Valeur d'ouverture
            try:
                item['open_'] = indices.css('span.c-instrument::text').extract()[2]
            except:
                item['open_'] = 'None'
            
            # Date de la collecte
            try: 
              item['time'] = datetime.now()
            except:
              item['time'] = 'None'



            yield item