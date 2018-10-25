# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

class MoncrawlerSpider(scrapy.Spider):

    name = 'monCrawler'
    allowed_domains = ['www.transfermarkt.fr']
    start_urls = ['https://www.transfermarkt.fr/ligue-1/startseite/wettbewerb/FR1/saison_id/2018']

    def delextrachar(self, str):

        delr = str.replace("\r", "")
        delt = delr.replace("\t", "")
        final = delt.replace("\n", "")
        return final

    def parse(self, response):
        urls = response.xpath('//*[@class="hauptlink no-border-links show-for-small show-for-pad"]/a/@href').extract()
        for url in urls:
            urlcomplet = response.urljoin(url)
            yield Request(urlcomplet, callback=self.parse_joueurs)

    def parse_joueurs(self, response):
        urls = response.xpath('//*[@class="hide-for-small"]/a/@href').extract()
        for url in urls:
            urlcomplet = response.urljoin(url)
            urlcomplet = urlcomplet.replace("profil", "leistungsdaten")
            urlcomplet += "/saison/2018/plus/1#gesamt"

            yield Request(urlcomplet, callback=self.parse_data)

    def parse_data(self, response):
        age = response.xpath('//*[@itemprop="birthDate"]/text()').extract_first()
        table = response.xpath('//*[@class="zentriert"]/text()').extract()
        listeposte = response.xpath('//*[@class="dataValue"]/text()').extract()
        prenom = response.xpath('//*[@itemprop="name"]/text()').extract()
        nom = response.xpath('//*[@itemprop="name"]/b/text()').extract()
        team = response.xpath('//*[@itemprop="affiliation"]/a/text()').extract()
        poste = self.delextrachar(listeposte[6])
        totalbut = table[0]

        yield {"nom": nom,
               "prenom": prenom,
               'age': self.delextrachar(age),
               'totalbut': totalbut,
               'poste': poste,
               'equipe': team}
