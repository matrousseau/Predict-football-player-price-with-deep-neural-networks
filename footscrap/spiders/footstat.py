# -*- coding: utf-8 -*-
import scrapy


class FootstatSpider(scrapy.Spider):
    name = 'footstat'
    allowed_domains = ['https://www.transfermarkt.fr/kylian-mbappe/leistungsdaten/spieler/342229']
    start_urls = ['https://www.transfermarkt.fr/kylian-mbappe/leistungsdaten/spieler/342229/']

    def parse(self, response):

        age = response.xpath('//*[@itemprop="birthDate"]/text()').extract()
        table = response.xpath('//*[@class="zentriert"]/text()').extract()
        listeposte = response.xpath('//*[@class="dataValue"]/text()').extract()
        prenom = response.xpath('//*[@itemprop="name"]/text()').extract()
        nom = response.xpath('//*[@itemprop="name"]/b/text()').extract()
        poste = listeposte[6]
        totalbut = table[0]

        yield {"nom": nom, "prenom": prenom, 'age': age, 'totalbut': totalbut, 'poste': poste}
