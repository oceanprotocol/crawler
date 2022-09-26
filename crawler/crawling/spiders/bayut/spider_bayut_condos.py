from __future__ import absolute_import

import time
from pathlib import Path

from bs4 import BeautifulSoup


import re

from crawling.models.nextSpidersInfo import NextSpidersInfo
from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.spiders.redis_spider import RedisSpider

from crawling.flowUtils import generateNextSpider


class BayutParseCondos(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = Path(__file__).stem
    def __init__(self,  *args, **kwargs):
        super(BayutParseCondos, self).__init__(*args, **kwargs)

    def parse(self, response):
        config = CrawlerConfig(
            **mongoClient["config"].find_one({"baseURL": re.findall('^https?:\/\/[^#?\/]+', response.request.url)[0]}))

        if config is None:
            self._logger.info("No config found. Please add one for url " + response.request.url)
            return

        soup = BeautifulSoup(response.text, 'lxml')
        condoLinks = soup.find_all("a", {"aria-label": "Listing link"})
        uniqueList = []
        for x in condoLinks:
            uniqueList.append(str(config.baseURL)+str(x["href"]))

        return self.generateSpiders(response, NextSpidersInfo('spider_bayut_condo_details',list(set(uniqueList)), config.flowTimeouts.get(self.name) ))


