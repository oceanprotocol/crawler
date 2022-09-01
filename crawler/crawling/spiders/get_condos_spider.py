from __future__ import absolute_import
from bs4 import BeautifulSoup


import re

from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.selectorUtils import getElements
from crawling.spiders.redis_spider import RedisSpider


class GetCondos(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "getCondos"

    def __init__(self,  *args, **kwargs):
        super(GetCondos, self).__init__(*args, **kwargs)

    def parse(self, response):
        try:
            self._logger.info("Finding config")
            config = CrawlerConfig(
                **mongoClient["config"].find_one({"baseURL": re.search('^https?:\/\/[^#?\/]+', response.request.url)}))

            if config is None:
                self._logger.info("No config found. Please add one")
                yield
            self._logger.info("Found config")
            print(config.sourceSettings.selectors["condoList"])
            self._logger.info("crawled url {}".format(response.request.url))
            soup = BeautifulSoup(response.text, 'lxml')
            self._logger.info(soup)
            self._logger.info("WUT2")
            self._logger.info(soup.find_all("div", class_="dev_item"))
            self._logger.info("WUT")
            numb = getElements(soup, config.sourceSettings.selectors["condoList"])
            self._logger.info(numb)
            for ccc in range(1,2):
                # self._logger.info(ccc.find_all("div", class_="title")[0].a["href"])
                c = getElements(soup, config.sourceSettings.selectors["condoElementLink"])
                self._logger.info("asdasdHEY")
                self._logger.info(c)
        except Exception as ex:
            print(ex)
        yield {}

