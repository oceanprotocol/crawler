from __future__ import absolute_import

import re
import time
from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.spiders.redis_spider import RedisSpider

from crawling.flowUtils import generateNextSpider


class GetLoad(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "get_load"
    c = 0
    def __init__(self,  *args, **kwargs):
        super(GetLoad, self).__init__(*args, **kwargs)

    def parse(self, response):
        try:
            config = CrawlerConfig(
                **mongoClient["config"].find_one({"baseURL": re.findall('^https?:\/\/[^#?\/]+', response.request.url)[0]}))
            if config is None:
                yield
            for x in range(2, config.sourceSettings.paginationSettings.staticPagination):
                time.sleep(1)
                yield generateNextSpider(response, "https://www.evomag.ro/tv-multimedia-televizoare-led/allview/?page="+str(x), 'test_load')

        except Exception as ex:
            self._logger.info(ex)

