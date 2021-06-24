import scrapy
from datetime import datetime


class ArabaSpider(scrapy.Spider):
    name = 'araba'
    allowed_domains = ['sahibinden.com']
    adresler = [  'https://www.sahibinden.com/bmw-3-serisi-318i?pagingSize=50',
                    'https://www.sahibinden.com/bmw-3-serisi-320i?pagingSize=50',
		    'https://www.sahibinden.com/bmw?pagingSize=50',
                    'https://www.sahibinden.com/anadol?pagingSize=50',
                    'https://www.sahibinden.com/audi?pagingSize=50',
		    'https://www.sahibinden.com/honda?pagingSize=50',
		    'https://www.sahibinden.com/honda?pagingSize=50',
		    'https://www.sahibinden.com/fiat?pagingSize=50',
		    'https://www.sahibinden.com/mercedes-benz?pagingSize=50',
		    'https://www.sahibinden.com/peugeot?pagingSize=50']

    markamodel=[('bmw','3serisi'),
                ('bmw','3serisi'),
		('bmw',''),
                ('anadol',''),
		('audi',''),
		('honda',''),
		('fiat',''),
		('Mercedes - Benz',''),
                ('Peugeot ','')]

    custom_settings = {
        'FEED_URI':'{}.json'.format(datetime.today().strftime('%B_%d_%y__%H%M')),
                     'FEED_FORMAT':'json'
    }

    def start_requests(self):
        for marka_model,adres in zip(self.markamodel,self.adresler):
            yield scrapy.Request(adres,meta={'markamodel':marka_model})

    def parse(self, response):
        satirlarim=response.xpath('.//tr[@data-id]')
        for araba in satirlarim:
            iD=araba.xpath('.//@data-id').extract_first()

            marka,model=response.meta['markamodel']
            cekilenveri=araba.xpath('.//td[@class="searchResultsTagAttributeValue"]/text()').extract()
            if len(cekilenveri)==2:
                model=cekilenveri[0].strip()
            notes=cekilenveri[-1].strip().replace(' ','')

            bilgiler=araba.xpath('.//td[@class="searchResultsAttributeValue"]/text()').extract()
            year=bilgiler[0].strip()
            km=bilgiler[1].strip().replace('.','')
            renk=bilgiler[2].strip()
            fiyat=araba.xpath('.//td[@class="searchResultsPriceValue"]/div/text()').extract_first()
            fiyat=fiyat.replace('TL','').strip().replace('.','')

            adDate=araba.xpath('.//td[@class="searchResultsDateValue"]/span/text()').extract()

            yil=int(adDate[1])

            gun=int(adDate[0].split()[0])

            aylar=['bosay','Ocak','Şubat','Mart','Nisan','Mayıs','Haziran','Temmuz','Ağustos','Eylül','Ekim','Kasım','Aralık']
            ay=aylar.index(adDate[0].split()[1])

            adDate='{}-{}-{}'.format(yil,ay,gun)

            yield {'id':iD,
                    'brand':marka,
                    'model':model,
                    'notes':notes,
                    'proDate':year,
                    'km':km,
                    'renk':renk,
                    'price':fiyat,
                    'adDate':adDate}

        if response.xpath('.//a[@title="Sonraki"]'):
            yenisayfa=response.xpath('.//a[@title="Sonraki"]/@href').extract_first()
            yenisayfa = 'https://www.sahibinden.com' + yenisayfa
            yield scrapy.Request(yenisayfa,meta={'markamodel':response.meta['markamodel']}) #callback yok dolayisi ile tekrar parse calisir, yeni response ile birlikte!!!
