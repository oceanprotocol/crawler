from __future__ import absolute_import

from pathlib import Path

from bs4 import BeautifulSoup


import re
from crawling.models.next_spiders_info import NextSpidersInfo
from crawling.mongo.models.crawler_config import CrawlerConfig
from crawling.mongo.mongo_client import mongo_client
from crawling.spiders.redis_spider import RedisSpider


class SportisimoProductsSpider(RedisSpider):
    """
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    """

    name = Path(__file__).stem

    def __init__(self, *args, **kwargs):
        super(SportisimoProductsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        config = CrawlerConfig(
            **mongo_client["config"].find_one(
                {"baseURL": re.findall("^https?:\/\/[^#?\/]+", response.request.url)[0]}
            )
        )

        if config is None:
            self._logger.info(
                "No config found. Please add one for url " + response.request.url
            )
            return
        soup = BeautifulSoup(response.text, "lxml")
        urls = map(
            lambda url: url.a["href"], soup.find_all("div", class_="product-box__name")
        )
        return self.generate_spiders(
            response,
            NextSpidersInfo(
                "spider_sportisimo_product_details",
                list(urls),
                config.flowTimeouts.get(self.name),
            ),
        )
