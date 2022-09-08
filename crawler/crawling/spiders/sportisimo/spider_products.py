from __future__ import absolute_import

import time

from bs4 import BeautifulSoup


import re

from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.spiders.redis_spider import RedisSpider

from crawling.flowUtils import generateNextSpider


class SportisimoProductsSpider(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "sportisimo_products"
    def __init__(self,  *args, **kwargs):
        super(SportisimoProductsSpider, self).__init__(*args, **kwargs)

    def parse(self, response):
        config = CrawlerConfig(
            **mongoClient["config"].find_one({"baseURL": re.findall('^https?:\/\/[^#?\/]+', response.request.url)[0]}))

        if config is None:
            self._logger.info("No config found. Please add one for url " + response.request.url)
            yield
        soup = BeautifulSoup(response.text, 'lxml')
        productLinks = soup.find_all("div", class_="product-box__name")

        for x in productLinks:
            if config.flowTimeouts[self.name]:
                time.sleep(config.flowTimeouts[self.name])
            yield generateNextSpider(response, x.a['href'], 'sportisimo_product_details')

