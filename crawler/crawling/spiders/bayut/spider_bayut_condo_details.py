from __future__ import absolute_import

from pathlib import Path

from bs4 import BeautifulSoup


import re

from crawling.models.selectorModels import SoupSearchObj
from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.selectorUtils import selectSoupElement
from crawling.spiders.redis_spider import RedisSpider

from crawling.db.jpa.all_models import Data
from crawling.db.mysqlClient import db_session
from crawling.db.repository import Repository

from crawling.db.jpa.all_models import Client

from crawling.db.models.apInfo import ApartmentInfo

from crawling.objUtils import getChainValue, getNumberFromStr


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

        apInfo = ApartmentInfo()
        apInfo.surface = getNumberFromStr(
            selectSoupElement(
                "surface",
                soup,
                SoupSearchObj("span", {"aria-label": "Area"}, True, 0),
                ["span", "span", "text"],
            )
        )

        apInfo.roomsNo = getNumberFromStr(
            selectSoupElement(
                "roomsNo",
                soup,
                SoupSearchObj("span", {"aria-label": "Beds"}, True, 0),
                ["span", "text"],
            )
        )

        apInfo.bathroomsNo = getNumberFromStr(
            selectSoupElement(
                "bathroomsNo",
                soup,
                SoupSearchObj("span", {"aria-label": "Baths"}, True, 0),
                ["span", "text"],
            )
        )

        apInfo.type = selectSoupElement(
            "type",
            soup,
            SoupSearchObj("span", {"aria-label": "Type"}, True, 0),
            ["text"],
        )

        apInfo.createdOn = selectSoupElement(
            "createdOn",
            soup,
            SoupSearchObj("span", {"aria-label": "Reactivated date"}, True, 0),
            ["text"],
        )
        apInfo.zone = selectSoupElement(
            "zone",
            soup,
            SoupSearchObj("div", {"aria-label": "Property header"}, True, 0),
            ["text"],
        )

        apInfo.price = getNumberFromStr(
            selectSoupElement(
                "price",
                soup,
                SoupSearchObj("span", {"aria-label": "Price"}, True, 0),
                ["text"],
            )
        )

        apInfo.ccy = selectSoupElement(
            "ccy",
            soup,
            SoupSearchObj("span", {"aria-label": "Currency"}, True, 0),
            ["text"],
        )

        apInfo.refNo = selectSoupElement(
            "refNo",
            soup,
            SoupSearchObj("span", {"aria-label": "Reference"}, True, 0),
            ["text"],
        )

        apInfo.url = response.request.url
        repoClient = Repository(db_session, Client)
        repo = Repository(db_session, Data)

        client = repoClient.find_by_code("BAYUT")

        repo.add(Data(info=apInfo.__dict__, client=client))

        db_session.commit()
