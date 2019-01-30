# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request


class UrlteamSpider(scrapy.Spider):
    name = 'urlteam'
    allowed_domains = ['www.transfermarkt.fr']
    start_urls = ['https://www.transfermarkt.fr/wettbewerbe/asien']

    def delextrachar(self,str):
        delr = str.replace("\r", "")
        delt = delr.replace("\t", "")
        delv = delt.replace(",", "")
        final = delv.replace("\n", "")
        return final

    def parse(self, response):
        urls = response.xpath('//*[@class="inline-table"]/tr/td/a/@href').extract()
        urls_cleaned = []
        for i in range (0, len(urls)):
            if i%2 == 0:
                urls_cleaned.append(urls[i])

        for url in urls:
            url = response.urljoin(url)
            yield Request(url, callback=self.parse_club)

    def parse_club(self, response):
        urls = response.xpath('//*[@class="hauptlink no-border-links show-for-small show-for-pad"]/a/@href').extract()
        for url in urls:
            urlcomplet = response.urljoin(url)
            yield Request(urlcomplet, callback=self.parse_joueurs)

    def parse_joueurs(self, response):
        urls = response.xpath('//*[@class="hide-for-small"]/a/@href').extract()
        for url in urls:
            urlcomplet = response.urljoin(url)
            yield Request(urlcomplet, callback=self.parse_data)

    def parse_data(self, response):
        prenom = response.xpath('//*[@itemprop="name"]/text()').extract()
        nom = response.xpath('//*[@itemprop="name"]/b/text()').extract()
        age = response.xpath('//*[@itemprop="birthDate"]/text()').extract_first()
        nationalite = response.xpath('//*[@itemprop="nationality"]/text()').extract()
        team = response.xpath('//*[@itemprop="affiliation"]/a/text()').extract()
        dataItem = response.xpath('//*[@class="dataValue"]/text()').extract()
        competitions = response.xpath('//*[@class="hauptlink no-border-links hide-for-small"]/a/@title').extract()
        stats = response.xpath('//*[@class="zentriert"]/text()').extract()[0:(len(competitions)+1)*4+1]
        club = response.xpath('//*[@itemprop="affiliation"]/a/text()').extract()
        ligue = response.xpath('//*[@class="mediumpunkt"]/a/text()').extract()

        try :
            poste1 = response.xpath('//*[@class="hauptposition-center"]/text()[2]').extract()
            poste2 = response.xpath('//*[@class="hauptposition-left"]/text()[2]').extract()
        except:
            poste1 = "NaN"
            poste2 = "NaN"

        try:
            buts_selection = response.xpath('//*[@class="dataValue"]/a/text()').extract()[-1]
            selections_nation = response.xpath('//*[@class="dataValue"]/a/text()').extract()[-2]
        except:
            buts_selection = 0
            selections_nation = 0

        finContrat = self.delextrachar(dataItem[len(dataItem)-1])
        price = response.xpath('//*[@class="dataMarktwert"]/a/text()').extract_first()
        price_range = response.xpath('//*[@class="waehrung"]/text()').extract_first()


        yield {"nom": nom,
               "prenom": prenom,
               'age': self.delextrachar(age),
               'club' : club,
               'nationalite' : nationalite,
               'poste1':  self.delextrachar(str(poste1)),
               'poste2':  self.delextrachar(str(poste2)),
               'ligue':  self.delextrachar(ligue[1]),
               'equipe' : team,
               'price' : price,
               'price_range' : price_range,
               'fin_contrat' : finContrat,
               'competitions' : competitions,
               'stats' : stats,
               'buts_selection' : buts_selection,
               'selections_nation' : selections_nation
               }


# https://www.transfermarkt.fr/moussa-doumbia/profil/spieler/316137
# https://www.transfermarkt.fr/gianluigi-buffon/leistungsdaten/spieler/5023/saison/2018/plus/1#gesamt
