from __future__ import absolute_import

import time

import re

from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.spiders.redis_spider import RedisSpider

from crawling.flowUtils import generateNextSpider


class BayutGetPages(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "bayut_pages"
    def __init__(self,  *args, **kwargs):
        super(BayutGetPages, self).__init__(*args, **kwargs)

    def parse(self, response):
        config = CrawlerConfig(
            **mongoClient["config"].find_one({"baseURL": re.findall('^https?:\/\/[^#?\/]+', response.request.url)[0]}))
        if config is None:
            self._logger.info("No config found. Please add one for url " + response.request.url)
            yield
        for x in range(2, config.sourceSettings.paginationSettings.staticPagination):
            url = config.sourceSettings.paginationSettings.url % {'PAG_NUM': str(x)}
            if config.flowTimeouts[self.name]:
                time.sleep(config.flowTimeouts[self.name])
            yield generateNextSpider(response, url, 'bayut_condos')
