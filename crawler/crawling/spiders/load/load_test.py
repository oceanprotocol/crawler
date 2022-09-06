from __future__ import absolute_import
from bs4 import BeautifulSoup


import re

from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.spiders.redis_spider import RedisSpider


class LoadTest(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "test_load"
    c = 0
    def __init__(self,  *args, **kwargs):
        super(LoadTest, self).__init__(*args, **kwargs)

    def parse(self, response):
        try:
            self._logger.info("Finding config for url "+ response.request.url)
            config = CrawlerConfig(
                **mongoClient["config"].find_one({"baseURL": re.findall('^https?:\/\/[^#?\/]+', response.request.url)[0]}))

            if config is None:
                self._logger.info("No config found. Please add one")
                yield
            self._logger.info("Found config")
            soup = BeautifulSoup(response.text, 'lxml')
            self.c = self.c + 1
            self._logger.info("Generate req no  " + str(self.c) + " with url " + str(config.baseURL))

        except Exception as ex:
            print(ex)

