# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class MoncrawlerSpider(scrapy.Spider):

    name = 'monCrawler'
    allowed_domains = ['www.transfermarkt.fr']
    start_urls = ['https://www.transfermarkt.fr/fc-paris-saint-germain/startseite/verein/583/']

    def parse(self, response):

        # On va chercher les urls des joueurs
        urls = response.xpath('//*[@class="hide-for-small"]/a/@href').extract()

        # On transforme les morceaux d'urls récupérés pour qu'ils correspondent à ceux des joueurs

        for url in urls:
            urlcomplet = response.urljoin(url)
            urlcomplet = urlcomplet.replace("profil", "leistungsdaten")
            urlcomplet += "/saison/2018/plus/1#gesamt"

        # On renvoie les urls récupérés vers une nouvelle fonction : parse_data
            yield Request(urlcomplet, callback=self.parse_data)

    def parse_data(self, response):
        age = response.xpath('//*[@itemprop="birthDate"]/text()').extract_first()
        prenom = response.xpath('//*[@itemprop="name"]/text()').extract()
        nom = response.xpath('//*[@itemprop="name"]/b/text()').extract()


        yield {"nom": nom,
               "prenom": prenom,
               'age': age}
