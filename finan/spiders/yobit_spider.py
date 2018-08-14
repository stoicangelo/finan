from scrapy import Spider
from scrapy import Request
from scrapy.exporters import CsvItemExporter
from os import path
import datetime
import csv

CURRENCY_DEACRONYM={
    'ETH':'Ethereum', 'BCH':'Bitcoin cash', 'ETC':'Ethereum classic',
    'BTC':'Bitcoin', 'DGB':'DigiByte', 'BCN':'Bytecoin',
    'XRP':'Ripple', 'REP':'Augur', 'DOGE':'Dogecoin',
    'LTC':'Litecoin', 'ZEC':'ZCash', 'BTS':'Bitshares',
    'XMR':'Monero', 'ZRX':'0x', 'NXT':'NXT', 'GAS':'Gas',
    'STR':'Stellar', 'DCR':'Decred', 'USD':'USA Dollar',
    'AUD':'Australia Dollar', 'GBP':'Great Britain Pound',
    'CHF':'Switzerland Franc', 'IRR':'Iran Rial', 'JPY':'Japan Yen',
    'CNY':'China Yen/Renmibi', 'RUB':'Russia Rouble', 'DMK':'Germany Mark'
}

def export_to_csv(spyder_name, dic):
    csv_name= "data-%s.csv"%(spyder_name)
    if not path.exists(csv_name):
        with open(csv_name,'a+') as csvf:
            writer=csv.writer(csvf)
            writer.writerow(list(dic.keys()))
    with open(csv_name,'a+') as csvf:
        writer=csv.writer(csvf)
        writer.writerow(list(dic.values()))


class YobitSpider(Spider):
    name = "yobit"

    def start_requests(self):
        urls = [
            'https://yobit.net/en/',
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)


    def parse(self, response):
        
        #yobit
        with open("%s_web.html"%(self.name),'wb')as f:
            f.write(response.body)

        data= dict()
        data['Datetime']=datetime.datetime.now()
        data['Last Current Price']=response.css('li.c_2 span::text').extract_first()
        data['24 Hr High Price']=response.css('li.c_3 span::text').extract_first()
        data['24 Hr Low Price']= response.css('li.c_4 span::text').extract_first()
        data['24 Hr Volume']= response.css('li.c_5 span::text').extract_first()
        
        market= response.css('li.c_1::text').extract()
        try:
            data['Coins']= CURRENCY_DEACRONYM[market[1].strip()]
        except:
            data['Coins']= market[1].strip()
        try:
            data['Base Currency']= CURRENCY_DEACRONYM[market[0].strip()]
        except:
            data['Base Currency']= market[0].strip()

        data['URL']= response.url
        
        export_to_csv(self.name, data)
        
        yield data  # no real reason to do this apart from making findings appear on log
