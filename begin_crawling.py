import sched
import time
from scrapy.crawler import CrawlerProcess
from finan.spiders.yobit_spider import YobitSpider
from scrapy.utils.project import get_project_settings

process= CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(YobitSpider)
process.start()
del process


scheduler= sched.scheduler(time.time, time.sleep)
waiting= 10
while True:
    repeated= CrawlerProcess({
      'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'    
    })
    repeated.crawl(YobitSpider)
    scheduler.enter(waiting, 2, repeated.start)
    scheduler.run()

    print("\n waiting for %d seconds before more action. Pres CTRL+Z to cancel\n"%(waiting))
    repeated.stop()
    del repeated