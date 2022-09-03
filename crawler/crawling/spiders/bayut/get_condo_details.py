from __future__ import absolute_import

import json

from bs4 import BeautifulSoup


import re

from crawling.mongo.models.CrawlerConfig import CrawlerConfig
from crawling.mongo.mongoClient import mongoClient
from crawling.selectorUtils import getElements
from crawling.spiders.redis_spider import RedisSpider

from crawling.db.jpa.all_models import Data
from crawling.db.mysqlClient import db_session
from crawling.db.repository import Repository

from crawling.db.jpa.all_models import Client

from crawling.db.models.apInfo import ApartmentInfo

from crawling.objUtils import getValueIfNotNull, getNumberFromStr


class BayoutCondoDetails(RedisSpider):
    '''
    A spider that walks all links from the requested URL. This is
    the entrypoint for generic crawling.
    '''
    name = "bayut_condo_details"
    c = 1
    def __init__(self,  *args, **kwargs):
        super(BayoutCondoDetails, self).__init__(*args, **kwargs)

    def parse(self, response):
        try:
            self.c = self.c + 1
            self._logger.info("Finding config for req NO " + str(self.c) + " and url " + response.request.url)
            config = CrawlerConfig(
                **mongoClient["config"].find_one({"baseURL": re.findall('^https?:\/\/[^#?\/]+', response.request.url)[0]}))

            if config is None:
                self._logger.info("No config found. Please add one")
                yield
            self._logger.info("Found config")
            soup = BeautifulSoup(response.text, 'lxml')

            apInfo =  ApartmentInfo()
            apInfo.surface = getNumberFromStr(getValueIfNotNull(soup.find_all("span", {"aria-label": "Area"})[0], 'span', 'span', 'text'))
            apInfo.roomsNo = getNumberFromStr(
                getValueIfNotNull(soup.find_all("span", {"aria-label": "Beds"})[0], 'span', 'text'))
            apInfo.bathroomsNo = getNumberFromStr(
                getValueIfNotNull(soup.find_all("span", {"aria-label": "Baths"})[0], 'span', 'text'))
            apInfo.type = getValueIfNotNull(soup.find_all("span", {"aria-label": "Type"})[0], 'text')
            apInfo.createdOn =  getValueIfNotNull(soup.find_all("span", {"aria-label": "Reactivated date"})[0], 'text')
            apInfo.zone = getValueIfNotNull(soup.find_all("div", {"aria-label": "Property header"})[0], 'text')
            apInfo.price = getNumberFromStr(
                getValueIfNotNull(soup.find_all("span", {"aria-label": "Price"})[0], 'text'))
            apInfo.ccy = getValueIfNotNull(soup.find_all("span", {"aria-label": "Currency"})[0],  'text')
            apInfo.refNo = getValueIfNotNull(soup.find_all("span", {"aria-label": "Reference"})[0], 'text')
            apInfo.url = response.request.url
            repoClient = Repository(db_session, Client)
            repo = Repository(db_session, Data)

            client = repoClient.find_by_code('BAYUT')
            # print(json.dumps(apInfo.__dict__))
            repo.add(Data(info=apInfo.__dict__, client= client))

            db_session.commit()
        except Exception as ex:
            print(ex)

