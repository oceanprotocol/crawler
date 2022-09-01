from __future__ import absolute_import
from bs4 import BeautifulSoup


import re

from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.selectorUtils import getElements
from crawling.spiders.redis_spider import RedisSpider

from crawling.flowUtils import generateNextSpider


class BayutParseCondos(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "bayut_condos"

    def __init__(self,  *args, **kwargs):
        super(BayutParseCondos, self).__init__(*args, **kwargs)

    def parse(self, response):
        try:
            self._logger.info("Finding config for "+ response.request.url)
            config = CrawlerConfig(
                **mongoClient["config"].find_one({"baseURL": re.findall('^https?:\/\/[^#?\/]+', response.request.url)[0]}))

            if config is None:
                self._logger.info("No config found. Please add one")
                yield
            self._logger.info("Found config")
            soup = BeautifulSoup(response.text, 'lxml')
            condoLinks = soup.find_all("a", {"aria-label": "Listing link"})
            for x in condoLinks:
                yield generateNextSpider(response, str(config.baseURL)+str(x["href"]), 'bayut_condo_details')
        except Exception as ex:
            print(ex)

