from __future__ import absolute_import

import re
from pathlib import Path

from crawling.models.nextSpidersInfo import NextSpidersInfo
from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.spiders.redis_spider import RedisSpider


from scrapy.exceptions import CloseSpider


class GetLoad(RedisSpider):
    """
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    """

    name = Path(__file__).stem

    def __init__(self, *args, **kwargs):
        super(GetLoad, self).__init__(*args, **kwargs)

    def parse(self, response):
        if self.close_down:
            raise CloseSpider(reason="API usage exceeded")
        config = CrawlerConfig(
            **mongoClient["config"].find_one(
                {"baseURL": re.findall("^https?:\/\/[^#?\/]+", response.request.url)[0]}
            )
        )
        if config is None:
            return
        urls = []
        for x in range(2, config.sourceSettings.paginationSettings.staticPagination):
            urls.append(
                "https://www.evomag.ro/tv-multimedia-televizoare-led/allview/?page="
                + str(x)
            )

        return self.generateNextSpider(
            response, NextSpidersInfo("spider_load_test", list(urls), 0)
        )
