from __future__ import absolute_import

import hashlib
import json
from pathlib import Path
from bs4 import BeautifulSoup


import re

from crawling.db.jpa.data import Data
from crawling.db.jpa.target import Target
from crawling.db.models.target_enum import TargetEnum
from crawling.db.mysql_client import db_session
from crawling.models.soup_search import SoupSearchObj
from crawling.mongo.models.crawler_config import CrawlerConfig
from crawling.mongo.mongo_client import mongo_client
from crawling.selector_utils import select_soup_element

from crawling.db.repositories.repository import Repository

from crawling.db.models.shoe_info import ShoeInfo

from crawling.obj_utils import get_precise_number
from crawling.spiders.redis_spider import RedisSpider


class SportisimoProductDetailsSpider(RedisSpider):

    """
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    """

    name = Path(__file__).stem

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
        id = response.request.url.rsplit("/", 3)[-2]
        shoe_info = ShoeInfo()

        shoe_info.productCode = select_soup_element(
            "productCode",
            soup,
            SoupSearchObj("span", {"id": "product_code_p%s_spec" % id}),
            ["text"],
        )
        shoe_info.url = response.request.url
        shoe_info.supplierCode = select_soup_element(
            "supplierCode",
            soup,
            SoupSearchObj("span", {"id": "product_match_code_p%s" % id}),
            ["text"],
        )
        shoe_info.shoeName = select_soup_element(
            "shoeName",
            soup,
            SoupSearchObj("td", {"class": "p_title"}),
            ["h1", "span", "text"],
        )
        shoe_info.price = get_precise_number(
            select_soup_element(
                "price", soup, SoupSearchObj("p", {"class": "price"}), ["text"]
            )
        )

        target_repo = Repository(db_session, Target)
        data_repo = Repository(db_session, Data)

        target = target_repo.find_by_code(str(TargetEnum.SPORTISIMO.value))
        data_repo.add(
            Data(
                info=shoe_info.__dict__,
                target=target,
                url=response.request.url,
                sha=hashlib.sha256(
                    json.dumps(shoe_info.__dict__).encode("utf-8")
                ).hexdigest(),
            )
        )

        # db_session.commit()
