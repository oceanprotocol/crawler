from __future__ import absolute_import

from pathlib import Path
from scrapy.exceptions import DontCloseSpider
from bs4 import BeautifulSoup


import re

from crawling.models.selectorModels import SoupSearchObj
from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.selectorUtils import selectSoupElement

from crawling.db.jpa.all_models import Data
from crawling.db.mysqlClient import db_session
from crawling.db.repository import Repository
from scrapy import signals
from crawling.db.jpa.all_models import Client

from scrapy.spiders import Spider
from crawling.db.models.shoeInfo import ShoeInfo

from crawling.objUtils import getPreciseNumber
from crawling.spiders.redis_spider import RedisSpider


class SportisimoProductDetailsSpider(RedisSpider):

    """
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    """

    name = Path(__file__).stem

    def parse(self, response):
        config = CrawlerConfig(
            **mongoClient["config"].find_one(
                {"baseURL": re.findall("^https?:\/\/[^#?\/]+", response.request.url)[0]}
            )
        )

        if config is None:
            self._logger.info(
                "No config found. Please add one for url " + response.request.url
            )
            return
        soup = BeautifulSoup(response.text, "lxml")
        id = response.request.url.rsplit("/", 3)[-2]
        shoeInfo = ShoeInfo()

        shoeInfo.productCode = selectSoupElement(
            "productCode",
            soup,
            SoupSearchObj("span", {"id": "product_code_p%s_spec" % id}),
            ["text"],
        )
        shoeInfo.url = response.request.url
        shoeInfo.supplierCode = selectSoupElement(
            "supplierCode",
            soup,
            SoupSearchObj("span", {"id": "product_match_code_p%s" % id}),
            ["text"],
        )
        shoeInfo.shoeName = selectSoupElement(
            "shoeName",
            soup,
            SoupSearchObj("td", {"class": "p_title"}),
            ["h1", "span", "text"],
        )
        shoeInfo.price = getPreciseNumber(
            selectSoupElement(
                "price", soup, SoupSearchObj("p", {"class": "price"}), ["text"]
            )
        )
        repoClient = Repository(db_session, Client)
        repo = Repository(db_session, Data)

        client = repoClient.find_by_code("SPORTISIMO")
        repo.add(Data(info=shoeInfo.__dict__, client=client))

        db_session.commit()
