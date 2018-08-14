from scrapy import Spider
from scrapy import Request
from scrapy.exporters import CsvItemExporter
import datetime


class LiquiSpider(Spider):
    name = "liqui"


    def start_requests(self):
        urls = [
            'https://liqui.io/',
        ]
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        
        #poloniex
        with open("%s_web.html"%(self.name),'wb')as f:
            f.write(response.body)
        data= dict()

        website= response.url
        data['website']=website

        date_and_time= datetime.now
        data['Datetime']= date_and_time

        last= response.css("div.market-panel div.row")[1].extract().css("p::text").extract_first()
        data['Last Current Price']=last
        
        ch= response.css("div.stat-change p::text").extract_first()
        data['24 Hr Price Change']=ch

        high= response.css("div.stat-highest p::text").extract_first()
        data['24 Hr High Price']=high
        
        low= response.css("div.stat-lowest p::text").extract_first()
        data['24 Hr Low Price']=low

        vol= response.css("div.stat-volume p::text").extract_first()
        data['24 Hr Volume']=vol

        last= response.css("div.row p::text").extract()
        data['Last Current Price']=last

        #[data['coins'], data['Base Currency']]=
        data['testing']= response.css("div.row p.market-name::text").extract_first()

        yield data
