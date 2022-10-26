# By NS
import scrapy
from scrapy import Request
from WebCrawler.items import ReviewsBoursoramaItem
from datetime import datetime
import mysql.connector as mc

class BoursoramaSpider(scrapy.Spider):
    name = 'boursorama'
    allowed_domains = ['www.boursorama.com']
    start_urls = [f'https://www.boursorama.com/bourse/actions/palmares/france/page-{n}/?france_filter[market]=1rPCAC' for n in range(1,3)]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url, callback=self.parse)
    
    def parse(self, response):
        liste_indices = response.css('tr.c-table__row')
        
        db = mc.connect(
            host='localhost',
            database='scraping',
            user='root',
            password=''
        )

        cursor = db.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS boursorama (id INT NOT NULL AUTO_INCREMENT, indice varchar(255), cours varchar(255), var varchar(255), hight varchar(255) , low varchar(255), open_ varchar(255), time varchar(255), PRIMARY KEY (id))")
        
        # Boucle qui parcours l'ensemble des éléments de la liste des indices sans le premier
        for indices in liste_indices[1:]:
            item = ReviewsBoursoramaItem()
            print(indices)
            # Indice boursier
            try:
                item['indice'] = indices.css('a.c-link::text').extract()[0]
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
              item['time'] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            except:
              item['time'] = 'None'

            sql = "INSERT INTO boursorama (indice, cours, var, hight, low, open_, time) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (item['indice'], item['cours'], item['var'], item['hight'], item['low'], item['open_'], item['time'])
            cursor.execute(sql, val)
            db.commit()

            yield item