from __future__ import absolute_import

from pathlib import Path

from bs4 import BeautifulSoup


import re

from crawling.models.next_spiders_info import NextSpidersInfo
from crawling.mongo.models.crawler_config import CrawlerConfig
from crawling.mongo.mongo_client import mongo_client
from crawling.spiders.redis_spider import RedisSpider


class BayutParseCondos(RedisSpider):
    """
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    """

    name = Path(__file__).stem

    def __init__(self, *args, **kwargs):
        super(BayutParseCondos, self).__init__(*args, **kwargs)

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
        condo_links = soup.find_all("a", {"aria-label": "Listing link"})
        unique_list = []
        for link in condo_links:
            unique_list.append(str(config.baseURL) + str(link["href"]))

        return self.generate_spiders(
            response,
            NextSpidersInfo(
                "spider_bayut_condo_details",
                list(set(unique_list)),
                config.flowTimeouts.get(self.name),
            ),
        )
