from __future__ import absolute_import

import time

from bs4 import BeautifulSoup


import re

from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.selectorUtils import getElements
from crawling.spiders.redis_spider import RedisSpider

from crawling.flowUtils import generateNextSpider


class BayutGetPages(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "bayut_pages"
    c = 0
    def __init__(self,  *args, **kwargs):
        super(BayutGetPages, self).__init__(*args, **kwargs)

    def parse(self, response):
        try:
            self._logger.info("Finding config")
            config = CrawlerConfig(
                **mongoClient["config"].find_one({"baseURL": re.findall('^https?:\/\/[^#?\/]+', response.request.url)[0]}))
            self._logger.info("No config found. Please add one")
            if config is None:
                self._logger.info("No config found. Please add one")
                yield
            self._logger.info("Found config")
            for x in range(2, config.sourceSettings.paginationSettings.staticPagination):
                url = config.sourceSettings.paginationSettings.url % {'PAG_NUM': str(x)}
                time.sleep(15)
                self.c =  self.c+1
                self._logger.info("Generated "+ str(self.c)+" with url " + url)
                yield generateNextSpider(response, url, 'bayut_condos')

        except Exception as ex:
            self._logger.info(ex)

