from __future__ import absolute_import

import json
from pathlib import Path
import hashlib

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
from crawling.spiders.redis_spider import RedisSpider

from crawling.db.repositories.repository import Repository


from crawling.db.models.ap_info import ApartmentInfo

from crawling.obj_utils import get_number_from_str


class BayoutCondoDetails(RedisSpider):
    """
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    """

    name = Path(__file__).stem

    def __init__(self, *args, **kwargs):
        super(BayoutCondoDetails, self).__init__(*args, **kwargs)

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

        ap_info = ApartmentInfo()
        ap_info.surface = get_number_from_str(
            select_soup_element(
                "surface",
                soup,
                SoupSearchObj("span", {"aria-label": "Area"}, True, 0),
                ["span", "span", "text"],
            )
        )

        ap_info.roomsNo = get_number_from_str(
            select_soup_element(
                "roomsNo",
                soup,
                SoupSearchObj("span", {"aria-label": "Beds"}, True, 0),
                ["span", "text"],
            )
        )

        ap_info.bathroomsNo = get_number_from_str(
            select_soup_element(
                "bathroomsNo",
                soup,
                SoupSearchObj("span", {"aria-label": "Baths"}, True, 0),
                ["span", "text"],
            )
        )

        ap_info.type = select_soup_element(
            "type",
            soup,
            SoupSearchObj("span", {"aria-label": "Type"}, True, 0),
            ["text"],
        )

        ap_info.createdOn = select_soup_element(
            "createdOn",
            soup,
            SoupSearchObj("span", {"aria-label": "Reactivated date"}, True, 0),
            ["text"],
        )
        ap_info.zone = select_soup_element(
            "zone",
            soup,
            SoupSearchObj("div", {"aria-label": "Property header"}, True, 0),
            ["text"],
        )

        ap_info.price = get_number_from_str(
            select_soup_element(
                "price",
                soup,
                SoupSearchObj("span", {"aria-label": "Price"}, True, 0),
                ["text"],
            )
        )

        ap_info.ccy = select_soup_element(
            "ccy",
            soup,
            SoupSearchObj("span", {"aria-label": "Currency"}, True, 0),
            ["text"],
        )

        ap_info.refNo = select_soup_element(
            "refNo",
            soup,
            SoupSearchObj("span", {"aria-label": "Reference"}, True, 0),
            ["text"],
        )

        ap_info.url = response.request.url
        target_repo = Repository(db_session, Target)
        data_repo = Repository(db_session, Data)

        target = target_repo.find_by_code(str(TargetEnum.BAYUT.value))

        data_repo.add(
            Data(
                info=ap_info.__dict__,
                target=target,
                url=response.request.url,
                sha=hashlib.sha256(
                    json.dumps(ap_info.__dict__).encode("utf-8")
                ).hexdigest(),
            )
        )

        # db_session.commit()
