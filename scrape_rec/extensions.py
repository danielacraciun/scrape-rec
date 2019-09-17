from datetime import datetime
from scrapy import signals

from scrape_rec.bot import send_listing_notifications


class SpiderBotCallback(object):

    def __init__(self):
        self.started_scraping_at = None

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls()
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        return ext

    def spider_opened(self, spider):
        self.started_scraping_at = datetime.now()

    def spider_closed(self, spider):
        send_listing_notifications(self.started_scraping_at)
