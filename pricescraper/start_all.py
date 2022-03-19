from scraper.spiders.paknsave import PaknsaveSpider
from scraper.spiders.newworld import NewWorldSpider

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
process = CrawlerProcess(settings)
process.crawl(NewWorldSpider)
process.crawl(PaknsaveSpider)
process.start()
