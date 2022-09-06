from __future__ import absolute_import
from bs4 import BeautifulSoup


import re

from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.spiders.redis_spider import RedisSpider

from crawling.flowUtils import generateNextSpider


class SportisimoGetPagesSpider(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "sportisimo_pages"
    def __init__(self,  *args, **kwargs):
        super(SportisimoGetPagesSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        try:
            self._logger.info("Finding config")
            config = CrawlerConfig(
                **mongoClient["config"].find_one({"baseURL": re.findall('^https?:\/\/[^#?\/]+', response.request.url)[0]}))
            if config is None:
                self._logger.info("No config found. Please add one")
                yield
            self._logger.info("Found config")
            soup = BeautifulSoup(response.text, 'lxml')
            page = int(soup.find_all("div", class_="page")[-1].a.text)

            for x in range(2, page):
                url = config.sourceSettings.paginationSettings.url % {'PAG_NUM': str(x)}
                yield generateNextSpider(response, url, 'sportisimo_products')

        except Exception as ex:
            self._logger.info("ERROR")
            self._logger.info(ex)

