from __future__ import absolute_import
from bs4 import BeautifulSoup


import re

from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.selectorUtils import getElements
from crawling.spiders.redis_spider import RedisSpider


class GetCondoDetails(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "getCondoDetails"

    def __init__(self,  *args, **kwargs):
        super(GetCondoDetails, self).__init__(*args, **kwargs)

    def parse(self, response):
        try:
            self._logger.debug("Finding config")
            config = CrawlerConfig(**db["config"].find_one({"baseURL": re.search('^https?:\/\/[^#?\/]+', response.request.url)}))

            if config is None:
                self._logger.debug("No config found. Please add one")
                yield
            print(config.sourceSettings.selectors["condoList"])

            self._logger.debug("crawled url {}".format(response.request.url))
            soup = BeautifulSoup(response.text, 'lxml')
            self._logger.debug("WUT2")
            self._logger.debug(soup.find_all("div", class_="dev-item"))
            self._logger.debug("WUT")
            numb = getElements(soup, config.sourceSettings.selectors["condoList"])
            for ccc in range(1,2):
                # self._logger.debug(ccc.find_all("div", class_="title")[0].a["href"])
                c = getElements(soup, config.sourceSettings.selectors["condoElementLink"])
                self._logger.debug("asdasdHEY")
                self._logger.debug(c)
        except Exception as ex:
            print(ex)
        yield {}

