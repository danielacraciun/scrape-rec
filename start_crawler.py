import os

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from scrape_rec import spiders

if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())

    process.crawl(spiders.storia.StoriaSpider)
    process.crawl(spiders.olx.OlxSpider)

    process.start()
