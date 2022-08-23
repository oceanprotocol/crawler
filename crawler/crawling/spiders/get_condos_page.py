from __future__ import absolute_import

import json
import importlib
from bs4 import BeautifulSoup

from scrapy.http import Request
from redis_spider import RedisSpider


# from ..db.mysqlClient import dbM
import db.mysqlClient

# from crawler.crawling.db.models.CrawlerConfig import CrawlerConfig

# from crawling.selectorUtils import getElements

# from crawler.crawling.flowUtils import getNextSpider

# from crawler.crawling.db.models.CrawlerConfig import PaginationType

import re

# from crawler.crawling.db.models.CrawlerConfig import Spider
from scrapy_splash import SplashRequest

# from crawler.crawling.db.jpa.all_models import Role


class GetCondosPage(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "getCondosPage"
    # mongoClient: MongoClient
    def __init__(self, *args, **kwargs):
        super(GetCondosPage, self).__init__(*args, **kwargs)

    def parseSec(self, response):
        self._logger.info("ASDASD4")
        soup = BeautifulSoup(response.body, 'lxml')
        self._logger.info(soup)
    def parse(self,  response):
        self._logger.info("ASDASD3")
        splash_args = {
            'html': 1,
            'png': 1,
            'width': 600,
            'render_all': 1,
            'wait': 5
        }
        # yield SplashRequest(response.request.url, self.parseSec, args=splash_args)
        soup = BeautifulSoup(response.text, 'lxml')
        self._logger.info("ASDASD2")
        dbM.session.query(Role)
        self._logger.info(soup)
        config = CrawlerConfig(
            **db["config"].find_one({"baseURL": re.findall("^https?:\/\/[^#?\/]+", str(response.request.url))[0]}))
        # try:
        #     self._logger.info("Finding config for " + response.request.url)
        #     config = CrawlerConfig(**db["config"].find_one({"baseURL": re.findall("^https?:\/\/[^#?\/]+", str(response.request.url))[0]}))
        #
        #     if config is None:
        #         self._logger.info("No config found. Please add one")
        #         yield
        #
        #     self._logger.info("crawled url {}".format(response.request.url))
        #
        #     self._logger.info(config.sourceSettings.paginationSettings.type)
        #
        #     if config.sourceSettings.paginationSettings.type == PaginationType.replaceInURL:
        #         self._logger.info("NO")
        #         numb = getElements(soup, config.selectors.pagination)
        #         for i in  range(1, int(numb)+1):
        #             url = config.sourceSettings.paginationSettings.url % {'PAG_NUM':  str(i) }
        #             req = Request(url)
        #
        #             for key in response.meta.keys():
        #                 req.meta[key] = response.meta[key]
        #             req.meta['spiderid'] = getNextSpider(config.sourceSettings.flow)
        #             yield req
        #
        #     if config.sourceSettings.paginationSettings.type == PaginationType.getUrlFromSelector:
        #         self._logger.info(config.sourceSettings.selectors)
        #
        #         nextPageUrl = getElements(soup, config.sourceSettings.selectors["pagination"])
        #         self._logger.info(nextPageUrl)
        #         if nextPageUrl:
        #             print("TEST1")
        #             req = Request(config.baseURL + nextPageUrl)
        #             for key in response.meta.keys():
        #                 req.meta[key] = response.meta[key]
        #             req.meta['spiderid'] = self.name
        #             print(req.meta['spiderid'])
        #             yield req
        #             print("TEST2")
        #             req2 = Request(config.baseURL+nextPageUrl)
        #             for key in response.meta.keys():
        #                 req2.meta[key] = response.meta[key]
        #             req2.meta['spiderid'] = getNextSpider(Spider.getCondosPage, config.sourceSettings.flow)
        #             print("TEST3")
        #             print(req2.meta['spiderid'] )
        #             yield req2
        #
        # except Exception as e:
        #     self._logger.info(e)
        # yield req

# https://emirates.estate/property/?tab=complex&n=8#objects
# https://emirates.estate/property/?tab=complex&n=8#objects