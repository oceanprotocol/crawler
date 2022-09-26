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


class SportisimoGetPagesSpider(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = Path(__file__).stem
    def __init__(self,  *args, **kwargs):
        super(SportisimoGetPagesSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        config = CrawlerConfig(
            **mongoClient["config"].find_one({"baseURL": re.findall('^https?:\/\/[^#?\/]+', response.request.url)[0]}))
        if config is None:
            self._logger.info("No config found. Please add one for url " + response.request.url)
            return
        soup = BeautifulSoup(response.text, 'lxml')
        page = int(soup.find_all("div", class_="page")[-1].a.text)
        urls = []
        for x in range(2, 4):
             urls.append(config.sourceSettings.paginationSettings.url % {'PAG_NUM': str(x)})

        return self.generateSpiders(response, NextSpidersInfo('spider_sportisimo_products', urls, config.flowTimeouts.get(self.name)))
